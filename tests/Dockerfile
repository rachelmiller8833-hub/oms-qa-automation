FROM python:3.12-slim

WORKDIR /tests

# Install tools needed during build (wget + CA certs)
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# --- NETFREE CERT INSTALL (optional) ---
ARG USE_NETFREE=true
RUN if [ "$USE_NETFREE" = "true" ]; then \
      wget -qO /home/netfree-unix-ca.sh https://netfree.link/dl/unix-ca.sh && \
      sh /home/netfree-unix-ca.sh && \
      echo "NetFree CA installed"; \
    else \
      echo "Skipping NetFree CA install"; \
    fi
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INSTALL ---

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "pytest", "-q"]
