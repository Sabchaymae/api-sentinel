![CI/CD](https://github.com/Sabchaymae/api-sentinel/actions/workflows/ci-cd.yml/badge.svg)

# API Sentinel — API Monitoring & Incident Detection

API Sentinel is a Python project I built to monitor API availability, track response times, and detect potential incidents.

The idea behind this project is simple: when an API becomes unavailable or starts returning errors, it is important to identify the problem quickly and keep a record of what happened.

Through this project, I wanted to practice backend development with Python, work with a relational database, and explore how automated testing and CI/CD pipelines are used in real-world projects.

## What does it do?

- Checks whether an API is responding correctly.
- Measures response times and records HTTP status codes.
- Detects API failures and creates incidents when a service is unavailable.
- Stores monitoring results and incidents in PostgreSQL.
- Provides REST endpoints to access monitoring history and incident records.
- Validates URLs to block common unsafe targets, including localhost and private IP addresses.
- Uses Docker to simplify application setup and execution.
- Runs automated tests through GitHub Actions.

## Technologies

- **Python & FastAPI** — Backend development and REST API endpoints.
- **HTTPX** — Sending HTTP requests and handling API responses.
- **PostgreSQL & SQLAlchemy** — Storing monitoring results and incidents.
- **Pytest** — Automated testing and code coverage.
- **Docker** — Containerizing the application.
- **GitHub Actions** — Automating tests and building the Docker image.
- **GitHub Container Registry (GHCR)** — Publishing the Docker image.

## How it works

The application follows a straightforward workflow:

1. A user submits the URL of an API to check.
2. API Sentinel validates the URL and sends an HTTP request.
3. The application records the response status and response time.
4. If the API is unavailable, an incident is created.
5. The monitoring history and incidents can be retrieved through dedicated endpoints.

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /health` | Checks whether the application is running. |
| `GET /monitor/check?url=...` | Checks a target API and records the result. |
| `GET /monitor/history` | Retrieves previous monitoring checks. |
| `GET /incidents` | Retrieves detected incidents. |
| `GET /docs` | Opens the interactive API documentation. |

## Run the project with Docker

Make sure Docker Desktop is running, then execute:

```bash
git clone https://github.com/Sabchaymae/api-sentinel.git
cd api-sentinel
```

Configure the required database connection in a local `.env` file, then start the application:

```bash
docker compose up --build
```

The API will be available at:

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Incidents: http://localhost:8000/incidents

The database must be running and accessible using the connection settings in `.env`.

## Testing

Automated tests cover the main application endpoints, monitoring behavior, incident detection, and URL validation.

Run the test suite with:

```bash
python -m pytest -v --cov=. --cov-report=term-missing
```

**Current results:** 28 tests passed, with 98% code coverage.

## CI/CD pipeline

I also configured a GitHub Actions workflow to automate the main quality checks.

Whenever changes are pushed to `main`, or a pull request targets that branch, the workflow runs the automated tests using Python 3.11 and PostgreSQL 16.

After the tests pass on `main`, the pipeline builds the Docker image and publishes it to GitHub Container Registry.

This helps catch problems earlier and keeps the application ready to be packaged consistently.

## Security considerations

API Sentinel includes basic URL validation to prevent requests to common unsafe destinations, such as localhost and private IP addresses.

This is an initial security layer, not a complete production-ready solution. Additional protections are needed, particularly against DNS rebinding, unsafe redirects, and access to internal network resources.

## Possible next steps

There are several features I would like to explore next:

- Scheduling checks to monitor APIs automatically.
- Configuring thresholds for repeated failures.
- Adding incident severity and status management.
- Sending notifications when an API becomes unavailable.
- Introducing authentication and authorization.
- Automating deployment to a server.
- Strengthening network security for production use.

## Project goal

This project is part of my practical learning journey in Python backend development and DevOps fundamentals. It gave me the opportunity to work with databases, automated testing, containerization, and CI/CD in one application.

The project is still evolving, and there is room to improve it as I explore more advanced monitoring and deployment practices.