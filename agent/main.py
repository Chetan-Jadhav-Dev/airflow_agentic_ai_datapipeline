import time
import logging
from agent.config import Config
from agent.monitor import Monitor
from agent.analyzer import Analyzer
from agent.actuator import Actuator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting AI Data Pipeline Troubleshooter Agent...")
    
    monitor = Monitor()
    analyzer = Analyzer()
    actuator = Actuator()

    while True:
        try:
            logger.info("Checking for failed tasks...")
            failed_tasks = monitor.check_airflow_failures()
            
            for task in failed_tasks:
                logger.info(f"Processing failed task: {task}")
                logs = analyzer.fetch_logs(task)
                analysis = analyzer.analyze_error(logs)
                logger.info(f"Analysis result: {analysis}")
                
                actuator.take_action(task, analysis)
                
            time.sleep(60) # Poll every minute
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
