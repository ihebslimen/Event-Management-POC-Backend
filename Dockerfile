# Builder stage
FROM python:3.11.8-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install system build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages into the user directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11.8-slim

WORKDIR /app

# Install runtime dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from the builder's user directory
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Ensure the user's local bin directory is in PATH
ENV PATH=/root/.local/bin:$PATH

# Command to run the application
CMD ["python3", "app.py"]