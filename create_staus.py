#!/usr/bin/env python3

import sqlite3

def create_table():
    conn = sqlite3.connect('/home/glen/webbrowse/web_index.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE crawl_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            depth INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
