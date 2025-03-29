# Use an official Python image
FROM python:3.11-slim-buster

# Set working directory inside the container
WORKDIR /app

# Copy ONLY requirements.txt first (better caching)
COPY ../requirements.txt ./

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev default-libmysqlclient-dev libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN python -m pip install --no-cache --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY ../ /app/

# Expose the port (assuming Flask runs on 5000)
EXPOSE 5000

# Load environment variables from the .env file at runtime
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Command to run the application
CMD ["python", "app.py"]
