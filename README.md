# AI Data Pipeline Troubleshooter

An AI-powered agent that monitors Airflow DAGs, detects failures, analyzes logs using Google Gemini, and automatically triggers fixes or retries.

## Features
- **Monitor**: Polls Airflow API for failed tasks.
- **Analyze**: Fetches logs from GCP Cloud Logging and uses Gemini LLM to identify root causes.
- **Act**: Triggers retries for transient errors or notifies admins for code/data issues.
- **CI/CD**: GitHub Actions to deploy DAGs to GCS.

## Prerequisites
- Docker & Docker Compose
- Google Cloud Platform Account
- Gemini API Key

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd agentic_ai
    ```

2.  **Configure Environment**:
    Create a `.env` file (or use the provided `setup_env.sh` to generate one) with:
    ```env
    AIRFLOW_URL=http://localhost:8080
    AIRFLOW_USERNAME=admin
    AIRFLOW_PASSWORD=admin
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
    GEMINI_API_KEY=your_api_key
    GCP_PROJECT_ID=your_project_id
    ```

3.  **Run Locally (Docker)**:
    ```bash
    ./scripts/start_docker.sh
    ```
    - Airflow UI: http://localhost:8080 (admin/admin)
    - Agent Logs: `docker-compose logs -f ai-agent`

4.  **Run Locally (Python)**:
    ```bash
    ./scripts/setup_env.sh
    source venv/bin/activate
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    python agent/main.py
    ```

## Architecture
See [implementation_plan.md](implementation_plan.md) for details.
