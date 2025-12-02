import logging
import requests
from datetime import datetime, timedelta
from agent.config import Config

logger = logging.getLogger(__name__)

class Monitor:
    def __init__(self):
        self.airflow_url = Config.AIRFLOW_URL.rstrip('/')
        self.auth = (Config.AIRFLOW_USERNAME, Config.AIRFLOW_PASSWORD)
        self.seen_failures = set()

    def check_airflow_failures(self):
        """
        Polls Airflow for failed task instances.
        Returns a list of dictionaries containing task info.
        """
        failed_tasks = []
        try:
            # 1. Get list of DAGs
            dags_url = f"{self.airflow_url}/api/v1/dags"
            response = requests.get(dags_url, auth=self.auth)
            response.raise_for_status()
            dags = response.json().get('dags', [])

            for dag in dags:
                dag_id = dag['dag_id']
                if dag['is_paused']:
                    continue

                # 2. Get failed task instances for this DAG
                # Since /dags/{dag_id}/taskInstances is returning 404, we iterate over dagRuns
                runs_url = f"{self.airflow_url}/api/v1/dags/{dag_id}/dagRuns"
                runs_params = {
                    'state': ['failed', 'running'], # Check running too as they might have failed tasks
                    'limit': 5, # Check last 5 runs
                    'order_by': '-execution_date'
                }
                runs_resp = requests.get(runs_url, auth=self.auth, params=runs_params)
                
                if runs_resp.status_code == 200:
                    dag_runs = runs_resp.json().get('dag_runs', [])
                    for run in dag_runs:
                        dag_run_id = run['dag_run_id']
                        
                        # Get task instances for this run
                        ti_url = f"{self.airflow_url}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
                        ti_params = {'state': ['failed']}
                        
                        ti_resp = requests.get(ti_url, auth=self.auth, params=ti_params)
                        
                        if ti_resp.status_code == 200:
                            task_instances = ti_resp.json().get('task_instances', [])
                            for ti in task_instances:
                                task_id = ti['task_id']
                                execution_date = ti['execution_date']
                                
                                failure_key = f"{dag_id}:{task_id}:{execution_date}"
                                
                                if failure_key not in self.seen_failures:
                                    logger.info(f"Found new failure: {failure_key}")
                                    failed_tasks.append({
                                        'dag_id': dag_id,
                                        'task_id': task_id,
                                        'execution_date': execution_date,
                                        'dag_run_id': dag_run_id,
                                        'try_number': ti['try_number']
                                    })
                                    self.seen_failures.add(failure_key)
                        else:
                             logger.warning(f"Failed to fetch TIs for run {dag_run_id}: {ti_resp.status_code}")
                else:
                    logger.warning(f"Failed to fetch DAG runs for {dag_id}: {runs_resp.status_code} - {runs_resp.text}")
        except Exception as e:
            logger.error(f"Error polling Airflow: {e}")
            
        return failed_tasks
