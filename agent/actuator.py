import logging
import requests
import json
from agent.config import Config

logger = logging.getLogger(__name__)

class Actuator:
    def __init__(self):
        self.airflow_url = Config.AIRFLOW_URL.rstrip('/')
        self.auth = (Config.AIRFLOW_USERNAME, Config.AIRFLOW_PASSWORD)

    def take_action(self, task_info, analysis):
        """
        Triggers an action based on the analysis.
        """
        action = analysis.get("action")
        confidence = analysis.get("confidence", 0.0)
        
        logger.info(f"Analysis suggests: {action} with confidence {confidence}")
        
        if action == "RETRY" and confidence > 0.7:
            self.restart_task(task_info)
        else:
            self.notify_admin(task_info, analysis)

    def restart_task(self, task_info):
        """
        Clears the task instance in Airflow to trigger a retry.
        """
        dag_id = task_info['dag_id']
        task_id = task_info['task_id']
        execution_date = task_info['execution_date']
        
        url = f"{self.airflow_url}/api/v1/dags/{dag_id}/clearTaskInstances"
        
        payload = {
            "dry_run": False,
            "task_ids": [task_id],
            "start_date": execution_date,
            "end_date": execution_date,
            "only_failed": True
        }
        
        try:
            response = requests.post(url, auth=self.auth, json=payload)
            if response.status_code == 200:
                logger.info(f"Successfully cleared task {dag_id}.{task_id}")
            else:
                logger.error(f"Failed to clear task: {response.text}")
        except Exception as e:
            logger.error(f"Error calling Airflow API: {e}")

    def notify_admin(self, task_info, analysis):
        """
        Logs the notification. In a real app, this would send Slack/Email.
        """
        logger.info("==================================================")
        logger.info(f"ALERT: Manual Intervention Required for {task_info['dag_id']}.{task_info['task_id']}")
        logger.info(f"Cause: {analysis.get('cause')}")
        logger.info(f"Classification: {analysis.get('classification')}")
        logger.info("==================================================")
