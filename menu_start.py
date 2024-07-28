#!/usr/bin/env python3

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QTableView, QLabel, QProgressBar
from PyQt5 import uic
from database_utils import fetch_crawl_state, fetch_index, get_record_count, reset_database
from table_model import TableModel
import sqlite3
from PyQt5.QtCore import QTimer
from database_utils import get_record_count


class CokyCrawlerControl(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('coky_crawler_control.ui', self)

        # Initialize the buttons, line edits, and labels
        self.resetIndex = self.findChild(QPushButton, 'resetIndex')
        self.startButton = self.findChild(QPushButton, 'start')
        self.stopButton = self.findChild(QPushButton, 'stop')
        self.seedUrl = self.findChild(QLineEdit, 'seedUrl')
        self.searchTerm = self.findChild(QLineEdit, 'searchTerm')
        self.crawlStateButton = self.findChild(QPushButton, 'crawlState')
        self.indexButton = self.findChild(QPushButton, 'index')
        self.crawlDepth = self.findChild(QLineEdit, 'crawlDepth')
        self.statusLabel = self.findChild(QLabel, 'statusLabel')
        self.stateURLs = self.findChild(QLineEdit, 'stateURLs')  # To show crawl_state record count
        self.indexURLs = self.findChild(QLineEdit, 'indexURLs')  # To show web_index record count
        self.pageRankProgress = self.findChild(QProgressBar, 'pageRankProgress')  # To show progress of page ranking

        # Initialize the table views
        self.crawlStateTable = self.findChild(QTableView, 'crawlStateTable')
        self.indexTable = self.findChild(QTableView, 'indexTable')

        # Connect buttons to their respective methods
        self.resetIndex.clicked.connect(self.reset_index)
        self.startButton.clicked.connect(self.start_crawler)
        self.stopButton.clicked.connect(self.stop_crawler)
        self.crawlStateButton.clicked.connect(self.show_crawl_state)
        self.indexButton.clicked.connect(self.show_index)

        # Initialize the UI with current counts
        self.update_ui_counts()

        # Set up a QTimer to periodically check for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.count_urls_update)
        self.timer.timeout.connect(self.update_page_rank_progress)
        self.timer.start(1000)  # Update every second

    def count_urls_update(self):
        state_urls_count = get_record_count('crawl_state', '/home/glen/webbrowse/web_index.db')
        self.stateURLs.setText(f"{state_urls_count}")
        state_urls_count = get_record_count('web_index', '/home/glen/webbrowse/web_index.db')
        self.indexURLs.setText(f"{state_urls_count}")

    def update_page_rank_progress(self):
        try:
            with open('page_rank_progress_value.txt', 'r') as f:
                progress = float(f.read().strip())
                self.pageRankProgress.setValue(int(progress))
                #print('Progress:', progress)
        except Exception as e:
            print(f"Error reading progress file: {e}")


    def reset_index(self):
        seed_url = self.seedUrl.text().strip()
        if seed_url:
            self.initialize_crawl_state(seed_url)
            self.statusLabel.setText("Index has been reset.")
            self.update_ui_counts()  # Update counts after reset
        else:
            self.statusLabel.setText("Seed URL is empty.")

    def start_crawler(self):
        # Set stop flag to 0
        with open('stop_flag.txt', 'w') as f:
            f.write('0')

        # Get the search term from the searchTerm QLineEdit
        search_term = self.searchTerm.text().strip()
        # Get the crawl depth from the crawlDepth QLineEdit
        crawl_depth = self.crawlDepth.text().strip()

        if not search_term:
            self.statusLabel.setText("Search term is empty.")
            return

        if not crawl_depth.isdigit():
            self.statusLabel.setText("Crawl depth must be an integer.")
            return

        try:
            max_depth = int(crawl_depth)
        except ValueError:
            max_depth = 1  # Default value if invalid input

        # Run coky2.py in a subprocess, passing the search term and max depth as arguments
        self.process = subprocess.Popen(['python3', 'coky2.py', search_term, str(max_depth)])
        self.statusLabel.setText("Crawler started.")
        print("Crawler started")

    def stop_crawler(self):
        # Set stop flag to 1
        with open('stop_flag.txt', 'w') as f:
            f.write('1')

        # Wait for the process to finish
        if hasattr(self, 'process'):
            self.statusLabel.setText("Crawler stopping...")
            print("Crawler stopping")

    def show_crawl_state(self):
        db_path = '/home/glen/webbrowse/web_index.db'
        data = fetch_crawl_state(db_path)
        model = TableModel(data)
        self.crawlStateTable.setModel(model)
        self.crawlStateTable.setAlternatingRowColors(True)
        self.crawlStateTable.resizeColumnsToContents()
        self.crawlStateTable.setSortingEnabled(True)
        self.crawlStateTable.setStyleSheet("QHeaderView::section { background-color:lightgray }")

    def show_index(self):
        db_path = '/home/glen/webbrowse/web_index.db'
        data = fetch_index(db_path)
        model = TableModel(data)
        self.indexTable.setModel(model)
        self.indexTable.setAlternatingRowColors(True)
        self.indexTable.resizeColumnsToContents()
        self.indexTable.setSortingEnabled(True)
        self.indexTable.setStyleSheet("QHeaderView::section { background-color:lightgray }")

    def update_ui_counts(self):
        db_path = '/home/glen/webbrowse/web_index.db'
        # Update the number of URLs in crawl_state
        state_count = get_record_count('crawl_state', db_path)
        self.stateURLs.setText(f"{state_count}")

        # Update the number of URLs in index
        index_count = get_record_count('web_index', db_path)
        self.indexURLs.setText(f"{index_count}")

    def update_progress(self, value):
        self.pageRankProgress.setValue(value)

    def initialize_crawl_state(self, seed_url):
        db_path = '/home/glen/webbrowse/web_index.db'
        conn = sqlite3.connect(db_path)  # Replace with your actual database path
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
