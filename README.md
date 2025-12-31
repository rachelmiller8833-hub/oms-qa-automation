# OMS – QA Automation Assignment

Order Management System (OMS) implemented with FastAPI, MongoDB and full end-to-end API tests using pytest.

The project demonstrates clean backend architecture, async API design, proper lifecycle management, and isolated integration tests running in Docker.

---

## Tech Stack

- Python 3.11
- FastAPI (async)
- MongoDB
- Motor (async MongoDB driver)
- pytest
- pytest-xdist
- Docker & docker-compose

## Project Structure

```
├── api
│ ├── main.py        # FastAPI application & routes
│ ├── db.py          # MongoDB connection & lifecycle
│ ├── orders_repo.py # Repository layer (DB access only)
│ ├── schemas.py     # Pydantic request/response models
│ └── requirements.txt
│
├── tests
│ ├── conftest.py    # pytest fixtures
│ └── test_orders.py # API integration tests
│
└── docker-compose.yml
```

## Architecture Overview

- **FastAPI** handles request routing and validation.
- **Repository layer** (`orders_repo.py`) is responsible only for database access.
- **MongoDB** is accessed asynchronously via Motor.
- **Dependency Injection** (`Depends(get_db)`) is used to provide DB handles to endpoints.
- **Application lifecycle** is managed with startup/shutdown hooks.
- **Tests** run against a real MongoDB instance but use a separate database for isolation.

---

## Data Model (Order)

```json
{
  "_id": "65fd8a1b1234567890abcd12",
  "user_id": "u12345",
  "items": [
    { "product_id": "p001", "name": "Laptop", "price": 1200, "quantity": 1 },
    { "product_id": "p002", "name": "Mouse", "price": 25, "quantity": 2 }
  ],
  "total_price": 1250,
  "status": "Pending"
}
```

## API Endpoints

### Create Order

POST /orders

**Request body**

{
  "user_id": "u12345",
  "items": [...],
  "total_price": 1250,
  "status": "Pending"
}


**Response**

{
  "_id": "generated_id"
}

### Get Order

GET /orders/{order_id}

**Response**

{
  "_id": "generated_id",
  "user_id": "u12345",
  "items": [...],
  "total_price": 1250,
  "status": "Pending"
}

### Update Order Status

PUT /orders/{order_id}

**Request body**

{
  "status": "Shipped"
}


**Response**

{
  "_id": "generated_id",
  "user_id": "u12345",
  "items": [...],
  "total_price": 1250,
  "status": "Shipped"
}

### Delete Order

DELETE /orders/{order_id}

**Response**

{
  "status": "deleted"
}

## Database Indexes

Indexes are created on application startup for:

- status
- user_id

This improves performance for filtering and querying orders.

## Running the Project

### Prerequisites

-Docker Desktop
-docker-compose

## Run API and Tests
docker compose up --build --abort-on-container-exit

This command:
- Builds all images
- Starts MongoDB and API
- Runs pytest container
- Stops automatically when tests finish

## Testing Strategy
- Tests run inside Docker.
- A dedicated MongoDB database is used for tests.
- Collections are cleaned before and after each test.

## CI/CD – GitHub Actions (Task 2)

This project includes a GitHub Actions workflow that runs the API integration tests in a fully dockerized environment (API + MongoDB + tests).

### What runs on each PR / push

The workflow:
1. Checks out the repository.
2. Builds Docker images (API + tests).
3. Starts MongoDB and the API services.
4. Waits for the API healthcheck to pass.
5. Runs pytest from the tests container.
6. Exports the JUnit XML report and uploads it as a GitHub Actions artifact.

### Parallel Test Execution

Parallel test execution is enabled using pytest-xdist (`-n auto`) to reduce CI runtime.
Each worker uses an isolated MongoDB database to avoid data collisions.

### Triggers

Tests run automatically on:
- Pull Requests targeting `main`
- Pushes to `main` (and `develop` if configured)

### Test Report (JUnit)

A JUnit report is generated at:
- `test-results/junit.xml`

This file is intentionally ignored by Git (`.gitignore`), but is uploaded by the CI pipeline as an artifact, so it can be downloaded from the GitHub Actions run.

### Release Tagging

The project includes automated release tagging as part of the CI pipeline.

After every successful CI run on the `main` branch, a Git tag is automatically
created. This ensures that each release tag corresponds to a commit that has
passed all automated tests, providing clear traceability between tested code
and released versions.

This setup simulates a production-ready release flow, even without an actual
deployment stage.


## Notes

- The POST endpoint intentionally returns only _id to keep the API contract minimal.
- All responses are validated using Pydantic response models.
- The system is designed to be easily extended with filtering, pagination, and real-time notifications.
- Additional QA documentation is available under the `docs/` directory:
Test Plan (`docs/test-plan.md`)




