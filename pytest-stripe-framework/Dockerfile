FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Default command to run tests
CMD ["pytest", "--alluredir=reports"]
