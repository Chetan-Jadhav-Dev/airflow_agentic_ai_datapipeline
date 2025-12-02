#!/bin/bash

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
    echo "AIRFLOW_URL=http://localhost:8081" >> .env
    echo "AIRFLOW_USERNAME=admin" >> .env
    echo "AIRFLOW_PASSWORD=admin" >> .env
    echo "GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json" >> .env
    echo "GEMINI_API_KEY=your_gemini_api_key" >> .env
    echo "GCP_PROJECT_ID=your_project_id" >> .env
    echo ".env file created. Please update it with your actual credentials."
else
    echo ".env file already exists."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Upgrade pip
echo "Upgrading pip..."
venv/bin/pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
venv/bin/pip install -r requirements.txt

echo "Setup complete. To run the agent:"
echo "source venv/bin/activate"
echo "export PYTHONPATH=\$PYTHONPATH:\$(pwd)"
echo "python agent/main.py"
