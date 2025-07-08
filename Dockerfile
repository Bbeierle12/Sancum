FROM python:3.11-slim
WORKDIR /app

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and scripts
COPY src/ src/
COPY scripts/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Create data directory for SQLite
RUN mkdir -p /app/data

ENTRYPOINT ["docker-entrypoint.sh"]
