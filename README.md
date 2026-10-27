\# API Sentinel — API Monitoring \& Incident Detection



A Python backend project for monitoring API availability, tracking response times, and detecting incidents.



\## Features



\- Monitor HTTP/HTTPS endpoints

\- Measure response times and HTTP status codes

\- Detect unavailable APIs and record incidents

\- Persist monitoring history in PostgreSQL

\- Expose REST endpoints using FastAPI

\- Validate URLs to reduce SSRF risks

\- Automated tests with pytest

\- Docker-based application deployment



\## Tech Stack



\- \*\*Language:\*\* Python 3.11

\- \*\*API:\*\* FastAPI, HTTPX

\- \*\*Database:\*\* PostgreSQL, SQLAlchemy

\- \*\*Testing:\*\* pytest, pytest-cov

\- \*\*Containers:\*\* Docker, Docker Compose



\## Architecture



```text

Client

&#x20; |

&#x20; v

FastAPI

&#x20; |

&#x20; +--> URL Validation

&#x20; |

&#x20; +--> HTTPX Monitoring

&#x20; |         |

&#x20; |         v

&#x20; |    Incident Detection

&#x20; |

&#x20; v

SQLAlchemy

&#x20; |

&#x20; v

PostgreSQL

&#x20; |

&#x20; +--> Monitoring History

&#x20; +--> Incident Records

```



\## API Endpoints



| Method | Endpoint | Description |

|---|---|---|

| GET | `/health` | Check application health |

| GET | `/monitor/check?url=...` | Monitor an API |

| GET | `/monitor/history` | Retrieve monitoring history |

| GET | `/incidents` | Retrieve detected incidents |

| GET | `/docs` | Interactive API documentation |



\### Example requests



Monitor a successful endpoint:



```text

http://127.0.0.1:8000/monitor/check?url=https://httpbin.org/status/200

```



Simulate an API failure:



```text

http://127.0.0.1:8000/monitor/check?url=https://httpbin.org/status/500

```



View recorded incidents:



```text

http://127.0.0.1:8000/incidents

```



\## Run with Docker



Prerequisites: Docker Desktop and Docker Compose.



Start the application:



```bash

docker compose up --build -d

```



Open the interactive documentation:



http://127.0.0.1:8000/docs



Check application health:



http://127.0.0.1:8000/health



Stop the application:



```bash

docker compose down

```



The current Compose configuration uses an existing PostgreSQL container. Configure the database connection in your local `.env` file before starting the application.



\## Run Tests



Activate the virtual environment and install dependencies:



```bash

python -m pip install -r requirements.txt

python -m pip install pytest pytest-cov

```



Run the tests:



```bash

python -m pytest -v

```



Generate a coverage report:



```bash

python -m pytest --cov=. --cov-report=term-missing

```



\*\*Current test results:\*\* 28 tests passed, with 98% code coverage.



\## Security



The application rejects unsupported URL schemes and common local or private network destinations.



This validation is a first layer of SSRF protection, not a complete production-grade defense. A production deployment should additionally address redirects, DNS rebinding, outbound network restrictions, authentication, and rate limiting.



\## Future Improvements



\- Scheduled monitoring

\- Configurable failure thresholds

\- Incident severity and lifecycle management

\- Notifications and alerting

\- Authentication and authorization

\- CI/CD integration

\- Production-grade network security



\## Project Objective



This project demonstrates practical skills in Python backend development, REST API design, relational database integration, automated testing, URL validation, and Docker-based deployment.



