# Docker image used to execute API integration tests.
# Provides an isolated environment for running pytest inside CI.
FROM python:3.12-slim

WORKDIR /tests

# Install minimal system dependencies (used mainly for optional NetFree CA setup)
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Optional NetFree CA installation, controlled via build argument
ARG USE_NETFREE=true
RUN if [ "$USE_NETFREE" = "true" ]; then \
      wget -qO /home/netfree-unix-ca.sh https://netfree.link/dl/unix-ca.sh && \
      sh /home/netfree-unix-ca.sh && \
      echo "NetFree CA installed"; \
    else \
      echo "Skipping NetFree CA install"; \
    fi

# Ensure Python HTTP clients trust the updated CA certificates
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test code and fixtures into the container
COPY . .

# Default command executes the test suite
CMD ["python", "-m", "pytest", "-q"]
