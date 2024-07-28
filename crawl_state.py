# crawl_state.py

import sqlite3

def save_crawl_state(conn, urls_to_crawl):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM crawl_state")
    for url, depth in urls_to_crawl:
        cursor.execute("INSERT INTO crawl_state (url, depth) VALUES (?, ?)", (url, depth))
    conn.commit()

def load_crawl_state(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT url, depth FROM crawl_state")
    return cursor.fetchall()

def get_next_url_from_crawl_state():
    conn = sqlite3.connect('/home/glen/webbrowse/web_index.db')  # Replace with your actual database path
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM crawl_state ORDER BY depth LIMIT 1")
    result = cursor.fetchone()
    if result:
        next_url = result[0]
        cursor.execute("DELETE FROM crawl_state WHERE url=?", (next_url,))
        conn.commit()
        conn.close()
        return next_url
    else:
        conn.close()
        return None

