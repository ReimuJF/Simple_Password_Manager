from userlogin import LoginUser, EditUser
import tkinter as tk
import tkinter.messagebox


class LoginWindow(tk.Tk):
    def __init__(self):
        self.Login = LoginUser()
        self.Edit = EditUser()
        super().__init__()
        self.title('Simple Login Page')
        self.resizable(width=False, height=False)
        self.geometry(f'310x110+{(self.winfo_screenwidth() // 2) - 300}+{(self.winfo_screenheight() // 2) - 300}')
        self.entry_login = tk.Entry(width=25)
        self.entry_password = tk.Entry(width=25, show="*")
        self.entry_login.grid(row=0, column=0, padx=10)
        self.entry_password.grid(row=1, column=0, padx=10)
        self.button_login = tk.Button(text='LOGIN', width=15, command=self.login_button)
        self.button_login.grid(row=0, column=1, padx=10, pady=5)
        self.button_sign = tk.Button(text='SIGN UP', width=15, command=self.sign_button)
        self.button_sign.grid(row=1, column=1, padx=10)
        self.button_get = tk.Button(text='GET USER LIST', width=15, command=self.get_button)
        self.button_get.grid(row=2, column=0, pady=10, sticky='ws', padx=5)
        self.button_delete = tk.Button(text='DELETE USER', width=15, command=self.delete_button)
        self.button_delete.grid(row=2, column=1, pady=10, sticky='es', padx=10)

    def login_button(self):
        check = self.Login.user_login(self.entry_login.get(), self.entry_password.get())
        if check:
            tkinter.messagebox.showinfo("Success", f"Hello {self.entry_login.get()}!")
            self.clear_entry()
        else:
            tkinter.messagebox.showinfo("Error", "Wrong login or password")

    def sign_button(self):
        check = self.Edit.create_user(self.entry_login.get(), self.entry_password.get())
        if check:
            tkinter.messagebox.showinfo("Success", f"User {self.entry_login.get()} created")
            self.clear_entry()
        else:
            tkinter.messagebox.showinfo("Error", "This name already taken")

    def get_button(self):
        users_list = self.Login.get_list()
        tkinter.messagebox.showinfo("Success", f"{users_list}")

    def delete_button(self):
        check = self.Edit.delete_user(self.entry_login.get())
        if check:
            tkinter.messagebox.showinfo("Success", "User was deleted")
            self.clear_entry()
        else:
            tkinter.messagebox.showinfo("Error", "User not found")

    def clear_entry(self):
        self.entry_login.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)


if __name__ == "__main__":
    window = LoginWindow()
    window.mainloop()
