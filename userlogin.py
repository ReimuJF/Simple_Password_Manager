import argon2
from sqldb import SqliteUsers


class LoginPage:

    def __init__(self):
        self.database = SqliteUsers()
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


class LoginUser(LoginPage):

    def user_login(self, login: str, password: str) -> bool:
        db_user_data = self.database.get_user_data(login)
        try:
            return self.ph.verify(db_user_data[login], password)
        except (argon2.exceptions.VerifyMismatchError, KeyError):
            return False
