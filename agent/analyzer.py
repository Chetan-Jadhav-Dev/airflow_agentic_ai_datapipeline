import logging
import requests
import google.generativeai as genai
from agent.config import Config

logger = logging.getLogger(__name__)

class Analyzer:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.airflow_url = Config.AIRFLOW_URL.rstrip('/')
        self.auth = (Config.AIRFLOW_USERNAME, Config.AIRFLOW_PASSWORD)
        
        # Initialize Gemini
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')
        else:
            logger.warning("GEMINI_API_KEY not set. LLM analysis will fail.")

    def fetch_logs(self, task_info):
        """
        Fetches logs from Airflow API for the given task.
        """
        dag_id = task_info['dag_id']
        task_id = task_info['task_id']
        dag_run_id = task_info['dag_run_id']
        try_number = task_info['try_number']

        logger.info(f"Fetching logs for {dag_id}.{task_id} from Airflow API")

        # Airflow API endpoint for logs
        # /api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{task_try_number}
        url = f"{self.airflow_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}"
        
        try:
            response = requests.get(url, auth=self.auth)
            
            if response.status_code == 200:
                # Airflow returns logs in JSON or text depending on config.
                # Usually it's a string content or a list of logs from different sources.
                # For local executor, it's usually just the content.
                return response.text
            else:
                logger.warning(f"Failed to fetch logs: {response.status_code} - {response.text}")
                return f"Failed to fetch logs: {response.status_code}"
            
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
            return f"Error fetching logs: {e}"

    def analyze_error(self, logs):
        """
        Sends logs to LLM to identify root cause and suggest action.
        """
        if not self.model:
            return {"cause": "LLM Not Configured", "action": "NOTIFY", "confidence": 0.0}

        prompt = f"""
        You are an expert Airflow Troubleshooter. Analyze the following Airflow task failure logs and determine the root cause.
        
        Logs:
        {logs[:10000]}  # Truncate to avoid token limits
        
        Determine:
        1. Root Cause (Brief explanation)
        2. Classification: "Transient" (network blip, timeout), "Code" (syntax error, logic bug), "Data" (missing file, bad format), or "Dependency" (upstream failure).
        3. Recommended Action: "RETRY" (if transient), "NOTIFY" (if code/data issue requires human fix).
        
        Output JSON format:
        {{
            "cause": "...",
            "classification": "...",
            "action": "RETRY" or "NOTIFY",
            "confidence": 0.0 to 1.0
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean up response to ensure it's valid JSON (sometimes LLMs add backticks)
            text = response.text.replace('```json', '').replace('```', '').strip()
            import json
            return json.loads(text)
        except Exception as e:
            logger.error(f"LLM Analysis failed: {e}")
            return {"cause": f"Analysis Failed: {e}", "action": "NOTIFY", "confidence": 0.0}
