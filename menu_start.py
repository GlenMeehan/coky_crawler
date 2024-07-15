#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PyQt5 import uic
import subprocess

class CokyCrawlerControl(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coky_crawler_control.ui', self)

        # Initialize the buttons and line edit
        self.resetIndex = self.findChild(QPushButton, 'resetIndex')
        self.startButton = self.findChild(QPushButton, 'start')
        self.stopButton = self.findChild(QPushButton, 'stop')
        self.seedUrl = self.findChild(QLineEdit, 'seedUrl')

        # Connect buttons to their respective methods
        self.resetIndex.clicked.connect(self.reset_index)
        self.startButton.clicked.connect(self.start_crawler)
        self.stopButton.clicked.connect(self.stop_crawler)

    def reset_index(self):
        seed_url = self.seedUrl.text().strip()
        if seed_url:
            initialize_crawl_state(seed_url)
        else:
            print("Seed URL is empty")

    def start_crawler(self):
        # Set stop flag to 0
        with open('stop_flag.txt', 'w') as f:
            f.write('0')

        # Run coky2.py in a subprocess
        self.process = subprocess.Popen(['python3', 'coky2.py'])
        print("Crawler started")

    def stop_crawler(self):
        # Set stop flag to 1
        with open('stop_flag.txt', 'w') as f:
            f.write('1')

        # Wait for the process to finish
        if hasattr(self, 'process'):
            self.process.terminate()
            self.process.wait()
            print("Crawler stopped")

def initialize_crawl_state(seed_url):
    conn = sqlite3.connect('/home/glen/webbrowse/web_index.db')  # Replace with your actual database path
    cursor = conn.cursor()

    # Clear the index and crawl_state tables
    cursor.execute("DELETE FROM web_index")
    cursor.execute("DELETE FROM crawl_state")

    # Insert the seed URL into the crawl_state table with depth 0
    cursor.execute("INSERT INTO crawl_state (url, depth) VALUES (?, ?)", (seed_url, 0))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CokyCrawlerControl()
    window.show()
    sys.exit(app.exec_())
