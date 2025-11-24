# Use an official lightweight Python image
FROM python:3.12-slim

# Ensure Python output is not buffered and no .pyc files are written
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for geoip2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose the application port
EXPOSE 5000

# Start the app with a production-ready WSGI server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
