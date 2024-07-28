import sqlite3

def fetch_data_from_db(query, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_crawl_state():
    query = "SELECT * FROM crawl_state"
    db_path = '/home/glen/webbrowse/web_index.db'
    return fetch_data_from_db(query, db_path)

def fetch_index():
    query = "SELECT * FROM web_index"
    db_path = '/home/glen/webbrowse/web_index.db'
    return fetch_data_from_db(query, db_path)
