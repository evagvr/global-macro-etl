from src.pipeline import Pipeline
from src.config.database import create_tables
from src.utils.logger import get_logger
import time
import psycopg2

if __name__ == "__main__":
    logger = get_logger("main")
    max_retries = 10
    for _ in range(max_retries):
        try:
            create_tables()
            break
        except psycopg2.OperationalError:
            logger.warning("Database is not ready yet. Retrying..")
            time.sleep(5)
    else:
        logger.error("Tables could not be created.")
        exit(1)
    pipeline = Pipeline()
    pipeline.run()