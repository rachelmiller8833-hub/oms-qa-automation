# Docker image used to execute API integration tests.
# Provides an isolated environment for running pytest inside CI.
FROM python:3.12-slim

WORKDIR /tests

# Install minimal system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test code and fixtures into the container
COPY . .

# Default command executes the test suite
CMD ["python", "-m", "pytest", "-q"]
