import psycopg2
from contextlib import contextmanager
from config.settings import settings

@contextmanager
def get_connection():
    connection = psycopg2.connect(host="db", user=settings.postgres_user, password=settings.postgres_password, dbname=settings.postgres_db, port=5432)
    try:
        yield connection
    finally:
        connection.close()