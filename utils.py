import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("Database connection successful!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
