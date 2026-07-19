# Django + MySQL Sample App — Full CI/CD Pipeline

A minimal Django app (a "Notes" CRUD app) backed by MySQL, containerized with
Docker, and wired into a Jenkins pipeline that builds, tests, pushes an image,
and deploys it. A GitHub Actions workflow is also included as a lightweight
CI check that runs on every push/PR.

```
GitHub (push) ──► Jenkins (webhook) ──► Build & Test ──► Docker Build
                                                            │
                                                            ▼
                                                     Push to Registry
                                                            │
                                                            ▼
                                                    Deploy (docker compose)
```

## Project layout

```
config/          Django project settings, urls, wsgi/asgi
notes/           Sample app: model, views, urls, tests, migrations
templates/       HTML templates
Dockerfile       Container image for the Django app
docker-compose.yml   App + MySQL for local dev/testing
Jenkinsfile      Declarative Jenkins pipeline (build/test/push/deploy)
.github/workflows/ci.yml   GitHub Actions CI (test + docker build)
requirements.txt
.env.example
```

## 1. Run locally with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Then visit:
- App: http://localhost:8000/
- Health check: http://localhost:8000/health/

Create a superuser (optional):
```bash
docker compose exec web python manage.py createsuperuser
```

## 2. Run locally without Docker

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export MYSQL_HOST=localhost   # point at a MySQL instance you control
python manage.py migrate
python manage.py runserver
```

## 3. Push this project to GitHub

This code was generated locally, so you'll push it from your own machine
(Claude's sandbox has no network access to GitHub). Steps:

```bash
cd django-mysql-cicd
git init
git add .
git commit -m "Initial commit: Django + MySQL sample app with CI/CD pipeline"

# Create a new empty repo on GitHub first (github.com/new), then:
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

If you use SSH instead of HTTPS:
```bash
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

## 4. Wire up Jenkins

1. Install plugins: **Docker Pipeline**, **Git**, **SSH Agent**, **Credentials Binding**.
2. Add credentials in *Manage Jenkins → Credentials*:
   - `dockerhub-creds` — Username/Password for Docker Hub (or your registry).
   - `deploy-server-ssh` — SSH private key for your deploy target.
3. Create a new **Pipeline** job → *Pipeline script from SCM* → point it at
   this GitHub repo → script path `Jenkinsfile`.
4. On GitHub: repo **Settings → Webhooks → Add webhook**
   → Payload URL: `http://<your-jenkins-url>/github-webhook/`
   → Content type: `application/json` → event: *Just the push event*.
5. Edit the `IMAGE_NAME` and `DEPLOY_HOST` variables at the top of the
   `Jenkinsfile` to match your Docker Hub username and deploy server.
6. Push to `main` — Jenkins will checkout, test, build the image, push it,
   and deploy via `docker compose up -d` on the target host.

## 5. Notes

- `notes/tests.py` has basic model/view/health-check tests exercised by both
  the Jenkinsfile and the GitHub Actions workflow.
- `/health/` returns JSON with DB connectivity status — useful for load
  balancers, Docker `HEALTHCHECK`, and post-deploy smoke tests.
- Swap MySQL container image / credentials as needed for production
  (managed RDS, Cloud SQL, etc.) by changing the `MYSQL_*` env vars only —
  no code changes required.
