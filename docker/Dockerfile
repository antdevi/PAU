# Use an official Python image
FROM python:3.11-slim-buster

# Set working directory inside the container
WORKDIR /app

# Copy ONLY requirements.txt first (for better caching)
COPY ../requirements.txt /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev default-libmysqlclient-dev libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python -m pip install --no-cache --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY .. //app

ENV LM_STUDIO_URL="http://host.docker.internal:1234/v1/chat/completions"

# Expose the port (assuming Flask runs on 5000)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
