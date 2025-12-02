import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AIRFLOW_URL = os.getenv("AIRFLOW_URL", "http://localhost:8080")
    AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "admin")
    AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "admin")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
