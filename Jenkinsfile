pipeline {
    agent { label 'Shubh' }

    stages {
        stage('Clone Code') {
            steps {
                echo 'This is a cloning a code'
                git url: 'https://github.com/Shubh1220/Django-Mysql-CICD.git', branch: 'main'
                echo 'Cloning Code Successfully'
            }
        }
        stage('Build Code') {
            steps {
                echo 'This is a building a code'
                sh 'docker build -t cicd-app:latest .'
                echo 'Building Code Successfully'
            }
        }
        stage('Push to DockerHub') {
            steps {
                echo 'This is a pushing a code'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerHubCreds',
                    usernameVariable: 'dockerHubUser',
                    passwordVariable: 'dockerHubPass'
                )]) {
                    sh '''
                        echo "$dockerHubPass" | docker login -u "$dockerHubUser" --password-stdin
                        docker tag cicd-app:latest $dockerHubUser/cicd-app:latest
                        docker push $dockerHubUser/cicd-app:latest
                    '''
                }
                echo 'Pushing Code Successfully'
            }
        }
        stage('Deploy Code') {
            steps {
                echo 'This is a deploying a code'
                sh 'docker compose down && docker compose up -d'
                echo 'Deploying Code Successfully'
            }
        }
    }
    post {
        success {
            echo '✅ CI/CD Pipeline completed successfully.'
        }

        failure {
            echo '❌ CI/CD Pipeline failed.'
        }

        always {
            sh 'docker image prune -f || true'
        }
    }
}
}
