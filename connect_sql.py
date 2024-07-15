import sqlite3

def connect_to_database():
    conn = sqlite3.connect('/home/glen/webbrowse/web_index.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            content TEXT,
            meta_keywords TEXT,
            author TEXT,
            publish_date TIMESTAMP,
            headers TEXT,
            links TEXT,
            word_count INTEGER,
            keywords TEXT,
            language TEXT,
            page_rank INTEGER,
            backlinks INTEGER,
            internal_links INTEGER,
            outbound_links INTEGER,
            ctr FLOAT,
            last_crawled TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            depth INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    return conn, cursor
