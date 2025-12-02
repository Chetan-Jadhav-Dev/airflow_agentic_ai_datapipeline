#!/bin/bash

echo "Starting Docker Compose..."
echo "Ensure you have set GOOGLE_APPLICATION_CREDENTIALS, GEMINI_API_KEY, and GCP_PROJECT_ID in your .env file or environment."

# Load .env if it exists
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

# Set AIRFLOW_UID to current user ID
export AIRFLOW_UID=$(id -u)
echo "Running as AIRFLOW_UID=$AIRFLOW_UID"

# Create necessary directories
mkdir -p dags logs plugins

docker-compose up --build -d
echo "Airflow running at http://localhost:8081 (admin/admin)"
echo "Agent is running in the background."
