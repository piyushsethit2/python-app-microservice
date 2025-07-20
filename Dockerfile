FROM python:3.9.18-slim

WORKDIR /app

# Install only essential packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables for logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_LEVEL=INFO

EXPOSE 5003

# Health check with shorter timeout
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5003/health || exit 1

# Use gunicorn with optimized settings for Render and proper logging
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "--workers", "1", "--timeout", "30", "--keep-alive", "2", "--max-requests", "1000", "--max-requests-jitter", "100", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "app:app"] 