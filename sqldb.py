import sqlite3
import os
import sys
import traceback


class SqliteWork:
    def __init__(self):
        self.userdb = 'users.db'
        if not os.path.isfile(self.userdb):
            self.create_table()

    def run_query(self, query):
        try:
            with sqlite3.connect(self.userdb) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query)
                conn.commit()
            return result
        except sqlite3.Error as error:
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Печать подробноcтей исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def create_table(self):
        sqlite_create_table = '''CREATE TABLE IF NOT EXISTS users(
                                user_id INTEGER PRIMARY KEY,
                                login TEXT not null UNIQUE,
                                pass TEXT not null);'''
        self.run_query(sqlite_create_table)

    def add_entry(self, login, password):
        sqlite_insert_query = f'''
            INSERT INTO users(login, pass) VALUES ("{login}", '{password}');
            '''
        self.run_query(sqlite_insert_query)

    def get_users(self) -> set:
        sqlite_select_query = '''SELECT login from users'''
        query = self.run_query(sqlite_select_query)
        return { i[0] for i in query }

    def get_user_data(self, login) -> dict:
        sqlite_select_query = f'''SELECT login, pass from users where login = "{login}"'''
        query = self.run_query(sqlite_select_query)
        return dict(query)

    def delete_entry(self, login):
        sqlite_delete_query = f"""DELETE FROM users WHERE login = '{login}'"""
        self.run_query(sqlite_delete_query)
