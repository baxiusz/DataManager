import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_path = os.path.join('databases', db_name)
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database '{db_name}': {e}")

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table '{table_name}': {e}")

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?'] * len(data))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        try:
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print(f"Data inserted into '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data into '{table_name}': {e}")

    def select_data(self, table_name, columns='*', condition=None, limit=None):
        try:
            if condition:
                select_query = f"SELECT {columns} FROM {table_name} WHERE {condition}"
            else:
                select_query = f"SELECT {columns} FROM {table_name}"
            if limit:
                select_query += f" LIMIT {limit}"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error selecting data from '{table_name}': {e}")
            return None
    
    def delete_table(self, table_name):
        delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
        try:
            self.cursor.execute(delete_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting table '{table_name}': {e}")

    def add_column(self, table_name, column_name, column_type):
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        try:
            self.cursor.execute(add_column_query)
            self.conn.commit()
            print(f"Column '{column_name}' added to table '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error adding column '{column_name}' to table '{table_name}': {e}")

    def delete_column(self, table_name, column_name):
        delete_column_query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        try:
            self.cursor.execute(delete_column_query)
            self.conn.commit()
            print(f"Column '{column_name}' deleted from table '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting column '{column_name}' from table '{table_name}': {e}")

    def close(self):
        self.conn.close()
