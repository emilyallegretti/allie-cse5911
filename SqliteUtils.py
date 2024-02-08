'''
Set up database connection and run queries
'''
import os
import sqlite3 as sq

class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cur = None

    def connect(self):
        '''Check if the database file exists'''
        if not os.path.isfile(self.db_file):
            raise Exception('Database file does not exist.')
        
        # self.conn = sq.connect(self.db_file)
        # self.cur = self.conn.cursor()

        self.conn = sq.connect(self.db_file)
        print("Database connection established.")
        self.conn.row_factory = sq.Row
        self.cur = self.conn.cursor()   # Create a cursor to use to access the data
        print('Cursor created.')

    def close(self):
        '''Close the database connection'''
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

    def run_query(self, query_string):
        '''Run a SQLite query and return the result'''
        if not self.conn:
            raise Exception('Database connection not established.')
        try:
            result = self.cur.execute(query_string)
        except sq.Error as e:
            print("Query error:", e)
            result = None
        return result