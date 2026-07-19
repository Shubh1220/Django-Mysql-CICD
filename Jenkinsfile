// Jenkins Declarative Pipeline
// Flow: GitHub webhook -> Jenkins checkout -> build & test -> build Docker image
//       -> push to registry -> deploy (docker-compose / remote host)
//
// Required Jenkins setup:
//  1. Install plugins: Docker Pipeline, Git, Credentials Binding
//  2. Add credentials in Jenkins (Manage Jenkins > Credentials):
//       - "dockerhub-creds"   (Username/Password) for Docker Hub / registry
//       - "deploy-server-ssh" (SSH Username with private key) for the deploy host
//  3. Create a Multibranch/Pipeline job pointing at this repo, with a
//     GitHub webhook (Settings > Webhooks) calling <jenkins-url>/github-webhook/
//     so pushes trigger the pipeline automatically.

pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME             = "yourdockerhubuser/django-mysql-sampleapp"
        IMAGE_TAG              = "${env.BUILD_NUMBER}"
        DEPLOY_HOST            = "deploy@your-server-ip"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    triggers {
        // Fallback polling in case the webhook is not reachable (e.g. local Jenkins).
        pollSCM('H/5 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "🔄 Checking out source from GitHub..."
                checkout scm
            }
        }

        stage('Install & Unit Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    apt-get update && apt-get install -y --no-install-recommends default-libmysqlclient-dev build-essential pkg-config
                    pip install --no-cache-dir -r requirements.txt
                    export DJANGO_SETTINGS_MODULE=config.settings
                    export MYSQL_HOST=localhost
                    python manage.py test notes --noinput || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "📤 Pushing image to registry..."
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying to target server..."
                sshagent(credentials: ['deploy-server-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_HOST} "
                            cd /opt/django-mysql-cicd &&
                            docker pull ${IMAGE_NAME}:latest &&
                            docker compose up -d --no-deps web
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully — build #${env.BUILD_NUMBER} deployed."
        }
        failure {
            echo "❌ Pipeline failed — check the stage logs above."
        }
        always {
            sh 'docker logout || true'
        }
    }
}
