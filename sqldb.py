import sqlite3
import tkinter.messagebox


class SqliteUsers:
    def __init__(self):
        self.userdb = 'users.db'
        self.create_table()

    def run_query(self, query):
        try:
            with sqlite3.connect(self.userdb) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query)
                conn.commit()
            return result
        except sqlite3.Error as error:
            tkinter.messagebox.showerror("Error", str(error.args))

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


class SqlitePManager(SqliteUsers):

    def create_table(self):
        sqlite_create_table = '''CREATE TABLE IF NOT EXISTS pmanager (
                                 entry_id INTEGER PRIMARY KEY,
                                 site TEXT,
                                 login TEXT not null,
                                 password TEXT not null,
                                 user_id INTEGER not null,
                                 FOREIGN KEY (user_id) REFERENCES users(user_id));'''
        self.run_query(sqlite_create_table)

    def add_entry_pm(self, entry_id, site, login, password, user_info):
        sqlite_insert_query = f'''
            INSERT INTO pmanager (entry_id, site, login, password, user_id) 
            VALUES ({entry_id}, "{site}","{login}", "{password}", (select user_id from users 
            where login = "{user_info}"));'''
        self.run_query(sqlite_insert_query)

    def get_pm_data(self, login) -> list:
        sqlite_query = f'''SELECT pm.entry_id, pm.site, pm.login, pm.password 
                            from pmanager as pm right join users as u on pm.user_id = u.user_id 
                            where u.login = "{login}"'''
        rows = self.run_query(sqlite_query)
        return list(rows)

    def delete_entry_pm(self, entry_id):
        sqlite_delete_query = f"""DELETE FROM pmanager WHERE entry_id = '{entry_id}'"""
        self.run_query(sqlite_delete_query)

    def update_entry(self, entry_id, site, login, password):
        sqlite_update_entry = f"""UPDATE pmanager 
                                SET site = '{site}',
                                password = '{password}',
                                login = '{login}'
                                WHERE entry_id = '{entry_id}'"""
        self.run_query(sqlite_update_entry)

    def delete_rows(self, user_info):
        sqlite_delete_query = f"""DELETE FROM pmanager WHERE user_id = (select user_id from users 
            where login = "{user_info}")"""
        self.run_query(sqlite_delete_query)

    def get_max_entry_id(self) -> int:
        get_query = """select max(entry_id) from pmanager"""
        index = self.run_query(get_query).fetchall()[0][0]
        return index if index else 0
