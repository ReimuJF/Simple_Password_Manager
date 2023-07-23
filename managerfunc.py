from sqldb import SqlitePManager
from password_generator import PasswordGenerator


class TableFunctions:

    def __init__(self, user_info: str):
        self.user_info = user_info
        self.database_pm = SqlitePManager()

    def get_rows(self) -> list:
        return self.database_pm.get_pm_data(self.user_info)

    def max_entry_id(self) -> int:
        return self.database_pm.get_max_entry_id() + 1

    def add_new_entry(self, data):
        self.database_pm.add_entry_pm(*data, self.user_info)

    def delete_entry(self, entry_id):
        self.database_pm.delete_entry_pm(entry_id)

    def edit_entry(self, data):
        self.database_pm.update_entry(*data)

    def delete_profile(self):
        self.database_pm.delete_rows(self.user_info)
        self.database_pm.delete_entry(self.user_info)

    @staticmethod
    def generate_password():
        rng_password = PasswordGenerator()
        rng_password.minlen = 8
        rng_password.maxlen = 12
        rng_password.minnumbers = 1
        rng_password.minschars = 1
        rng_password.minuchars = 1
        return rng_password.generate()
