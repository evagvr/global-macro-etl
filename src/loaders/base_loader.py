import logging
from psycopg2.extras import execute_values
from src.config.database import get_connection

class BaseLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _execute_bulk_insert(self, query: str, data_list: list):
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    execute_values(cur=cursor, sql=query, argslist=data_list)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    self.logger.error(f"Bulk insert failed: {e}")
                    raise e