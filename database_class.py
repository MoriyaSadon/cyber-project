import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, table_name, db_file='my_db.db'):
        self.db_file = db_file
        self.table_name = table_name
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            print("Connected to the database.")
            return conn
        except Error as e:
            print(f"Error creating connection: {e}")
            return None

    def create_table(self, columns):
        try:
            cursor = self.conn.cursor()
            # Example columns: "id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER"
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})")
            print(f"Table '{self.table_name}' created.")
            return cursor
        except Error as e:
            print(f"Error creating table: {e}")
            return None

    def add_data(self, data):
        ## type(data) = dict {column:word}
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in range(len(data))])
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            self.conn.execute(query, tuple(data.values()))
            self.conn.commit()
            print(f"Data added to '{self.table_name}' table.")
        except Error as e:
            print(f"Error adding data: {e}")

    def remove_data(self, data):
        ## type(data) = dict {column:word}
        try:
            # deletes the data
            self.conn.execute(f'DELETE FROM {self.table_name} WHERE {data.keys()} = ?', (data[data[0]],))
            self.conn.commit()

            # reorders the id numbers
            reorder_query = f"UPDATE {self.table_name} SET id = (SELECT COUNT(*) FROM {self.table_name} t2 WHERE t2.id <= {self.table_name}.id)"
            self.conn.execute(reorder_query)
            self.conn.commit()
        except Error as e:
            print(f"Error adding data: {e}")

    def check_word_in_table(self, word_to_check):
        try:
            query = "SELECT COUNT(*) FROM words WHERE word = ?"
            self.conn.execute(query, (word_to_check,))
            result = self.conn.cursor().fetchone()

            # Check if the count is greater than 0, indicating that the word is in the table
            return result[0] > 0 if result else False
        except Error as e:
            return None

    def get_all_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error retrieving data: {e}")
            return None

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")

