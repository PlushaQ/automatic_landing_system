import psycopg2
import sqlite3
from database_config import DB_CONFIG


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.db_info = DB_CONFIG
        self.active = False
        self.connection_id = None

    def __repr__(self):
        return f'<Connection ID {self.connection_id}. Active: {self.active}>'

    def _connect(self):
        if len(self.db_info) == 1:
            try:
                self.connection = sqlite3.connect(self.db_info['database'])
            except sqlite3.Error:
                print("Error occurred while connecting to SQLITE database. Please check configurations and try again.")
        else:
            try:
                self.connection = psycopg2.connect(**self.db_info)
            except psycopg2.Error:
                print("Error occurred while connecting to postgre database. Please check configurations and try again.")

        self.connection_id = id(self.connection)

    def conn_info(self):
        self._connect()
        return self

