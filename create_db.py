#!/usr/bin/env python3

import sqlite3

def create_table():
    conn = sqlite3.connect('/home/glen/webbrowse/web_index.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_index (
            id INTEGER PRIMARY KEY,
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
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
