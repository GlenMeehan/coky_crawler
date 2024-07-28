import sqlite3

def fetch_data_from_db(query, db_path):
    """Fetches data from the database based on a given query."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_crawl_state(db_path):
    """Fetches all records from the crawl_state table."""
    query = "SELECT * FROM crawl_state"
    return fetch_data_from_db(query, db_path)

def fetch_index(db_path):
    """Fetches all records from the web_index table."""
    query = "SELECT * FROM web_index"
    return fetch_data_from_db(query, db_path)

def get_record_count(table_name, db_path):
    """Gets the record count for a given table."""
    query = f"SELECT COUNT(*) FROM {table_name}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def reset_database(db_path):
    """Resets the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM web_index")
    cursor.execute("DELETE FROM crawl_state")
    conn.commit()
    conn.close()
