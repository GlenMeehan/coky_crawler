import sqlite3

def connect_to_database():
    db_path = "/home/glen/webbrowse/web_index.db"  # Update this path to your database location
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the index table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "index" (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT,
        content TEXT,
        last_crawled TIMESTAMP
    )
    ''')
    conn.commit()
    return conn, cursor
