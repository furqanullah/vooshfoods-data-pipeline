import sqlite3

DB_NAME = "products.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Main data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title TEXT,
        price_usd REAL,
        price_inr REAL,
        category TEXT,
        rating REAL,
        updated_at TEXT
    )
    """)

    # Monitoring table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_run TEXT,
        status TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()
