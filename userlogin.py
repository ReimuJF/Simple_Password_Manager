import argon2
from sqldb import SqliteWork


class LoginPage:

    def __init__(self):
        self.database = SqliteWork()
        self.ph = argon2.PasswordHasher()


class EditUser(LoginPage):

    def hash_pass(self, password):
        hashed_pass = self.ph.hash(password)
        return hashed_pass

    def create_user(self, login: str, password: str) -> bool:
        table = self.database.get_users()
        if login in table:
            return False
        self.database.add_entry(login, self.hash_pass(password))
        return True

    def delete_user(self, user_name: str) -> bool:
        table = self.database.get_users()
        if user_name not in table:
            return False
        self.database.delete_entry(user_name)
        return True


class LoginUser(LoginPage):

    def user_login(self, login: str, password: str) -> bool:
        db_user_data = self.database.get_user_data(login)
        try:
            return self.ph.verify(db_user_data[login], password)
        except (argon2.exceptions.VerifyMismatchError, KeyError):
            return False

    def get_list(self):  # test function will be removed in future
        table = self.database.get_users()
        return '\n'.join(table) if len(table) > 0 else 'No users found'  # users_list
