FROM python:3.12-slim

WORKDIR /app

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

# Ensure Python and other tools trust the updated CA certificates
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
