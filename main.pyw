from userlogin import LoginUser, EditUser
import tkinter as tk
import tkinter.messagebox
from table_window import DrawTable


class LoginWindow(tk.Tk):
    def __init__(self):
        self.Login = LoginUser()
        self.Edit = EditUser()
        super().__init__()
        self.title('Simple Login Page')
        self.resizable(width=False, height=False)
        self.geometry(f'+{(self.winfo_screenwidth() // 2) - 300}+{(self.winfo_screenheight() // 2) - 300}')
        self.login_label = tk.Label(self, text='User Name')
        self.login_label.grid(row=0, column=0, sticky='ew', padx=15)
        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=1, column=0, sticky='ew', padx=15)
        self.entry_login = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_login.grid(row=0, column=1, padx=5, sticky='w')
        self.entry_password.grid(row=1, column=1, padx=5, sticky='w')
        self.button_login = tk.Button(text='LOGIN', width=15, command=self.login_button)
        self.button_login.grid(row=2, column=1, padx=10, pady=5)
        self.button_sign = tk.Button(text='SIGN UP', width=15, command=self.sign_button)
        self.button_sign.grid(row=2, column=0, padx=10, pady=5)

    def login_button(self):
        check = self.Login.user_login(self.entry_login.get(), self.entry_password.get())
        if check:
            draw_table = DrawTable(self, self.entry_login.get())
            draw_table.grab_set()
            self.clear_entry()
            self.withdraw()
        else:
            tkinter.messagebox.showinfo("Error", "Wrong login or password")

    def sign_button(self):
        check = self.Edit.create_user(self.entry_login.get(), self.entry_password.get())
        if check:
            tkinter.messagebox.showinfo("Success", f"User {self.entry_login.get()} created")
            self.clear_entry()
        else:
            tkinter.messagebox.showinfo("Error", "This name already taken")

    def clear_entry(self):
        self.entry_login.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)


if __name__ == "__main__":
    window = LoginWindow()
    window.mainloop()
