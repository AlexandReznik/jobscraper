This is a Job Scraper and Alert System

Stack: Scrapy, FastAPI, Pandas

## Description

System that scrapes job postings from various websites, stores them, and sends alerts to users based on their preferences.
Features: Scrapy spiders for job sites, FastAPI for user interaction and alerts, Pandas for data processing and filtering

## Getting Started

First, install requirements from requirements.txt:

```bash
pip install -r requirements.txt
```

Then make migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "some_description_of_migration"
```

To start app locally, use:

```bash
uvicorn app.main:app --reload
```

## Endpoints

Users:
- POST docs/users/create/ - to create new a user
- POST docs/users/me/ - to get authorized user
- POST docs/users/token/ - to login and get token if successfully
- PUT docs/users/preferences/ - to change preferences of logged user

Jobs:
- GET docs/jobs/all/ - to get list of jobs((doesn't availible for not authorized users))
- GET docs/jobs/alert/ - to get list of jobs on email based on preferences of logged user

