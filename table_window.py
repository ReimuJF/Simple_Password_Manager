import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from managerfunc import TableFunctions


class DrawTable(tk.Toplevel):

    def __init__(self, parent, user_info):
        super().__init__(parent)
        self.manager = TableFunctions(user_info)
        self.parent_window = parent
        self.resizable(width=False, height=False)
        self.title('Simple Password Manager')
        self.geometry(f'+{self.winfo_screenwidth() // 2 - 400}+{self.winfo_screenheight() // 2 - 300}')
        self.top_menu = tk.Menubutton(self, text='Menu', activebackground='darkgrey')
        self.user_menu = tk.Menu(self.top_menu, tearoff=0)
        self.user_menu.add_command(label='Delete user', command=self.delete_profile)
        self.top_menu.pack(anchor='nw')
        self.top_menu.config(menu=self.user_menu)
        self.button_frame = tk.Frame(self)
        self.add_button = ttk.Button(self.button_frame, text='Add Entry', command=self.add_entry)
        self.add_button.pack(padx=5, pady=3)
        self.button_frame.pack(anchor='nw')
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(padx=5, side='bottom')
        self.scroll = tk.Scrollbar(self.table_frame)
        self.scroll.pack(side='right', fill='y')
        self.table = ttk.Treeview(self.table_frame, yscrollcommand=self.scroll.set)
        self.style = ttk.Style()
        self.style.theme_use('alt')

        self.right_click_menu = tk.Menu(self.table, tearoff=0)

        self.right_click_menu.add_command(label='Edit', command=self.edit_entry)
        self.right_click_menu.add_command(label='Delete', command=self.delete_row)
        self.right_click_menu.add_command(label='Copy Password', command=self.copy_pass)

        self.table['columns'] = ('ID', 'Site', 'Login', 'Password')

        self.table.column('#0', width=0, stretch=False)
        self.table.column('#1', anchor='center', width=0)
        self.table.column('#2', anchor='center', width=120)
        self.table.column('#3', anchor='center', width=120)
        self.table.column('#4', anchor='center', width=120)

        self.table.heading('#0', text='', anchor='center')
        self.table.heading('#1', text='ID', anchor='center')
        self.table.heading('#2', text='Site', anchor='center')
        self.table.heading('#3', text='Login', anchor='center')
        self.table.heading('#4', text='Password', anchor='center')

        self.table.bind('<Double-Button-1>', self.edit_entry)
        self.table.bind('<Button-3>', lambda event: self.right_click_menu.post(event.x_root, event.y_root))
        for index, row in enumerate(self.manager.get_rows(), 1):
            self.table.insert(parent='', index='end', iid=f'{index}', text='', values=row)
        self.table.pack()
        self.scroll.config(command=self.table.yview)

        self.protocol("WM_DELETE_WINDOW", self._destroy)

    def _destroy(self):
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.parent_window.deiconify()
            self.destroy()

    def delete_row(self):
        self.manager.delete_entry(self.table.item(self.table.focus())['values'][0])
        selected_items = self.table.selection()
        for selected_item in selected_items:
            self.table.delete(selected_item)

    def copy_pass(self):
        data = self.table.item(self.table.focus())['values'][3]
        self.clipboard_clear()
        self.clipboard_append(data)

    def edit_entry(self, event=None):
        iid = self.table.selection()[0]
        data = self.table.item(self.table.focus())['values']
        edit_entry = EditWindow(self, data)
        edit_entry.wait_visibility() # to avoid errors on linx systems
        edit_entry.grab_set()
        edit_entry.wait_window()
        if data := edit_entry.new_value:
            self.manager.edit_entry(data)
            self.table.item(iid, values=data)

    def add_entry(self):
        e_id = self.manager.max_entry_id()
        new_entry = AddEntryWindow(self, e_id)
        new_entry.grab_set()
        new_entry.wait_window()
        if data := new_entry.new_value:
            self.manager.add_new_entry(data)
            self.table.insert(parent='', index='end', text='', values=data)

    def delete_profile(self):
        if tkinter.messagebox.askokcancel('Delete Profile', 'Do you want to delete profile and associated entries?'):
            self.manager.delete_profile()
            self.parent_window.deiconify()
            self.destroy()


class AddEntryWindow(tk.Toplevel):

    def __init__(self, parent, e_id=None):
        super().__init__(parent)
        self.new_value = None
        self.title('Add new entry')
        self.geometry(f'250x125+{parent.winfo_rootx()}+{parent.winfo_rooty()}')
        self.style = ttk.Style()
        self.style.theme_use('alt')

        self.id_label = tk.Label(self, text='ID')
        self.id_label.grid(row=0, column=0, sticky='w')

        self.id_number = tk.Label(self, text=e_id)
        self.id_number.grid(row=0, column=1, sticky='w', padx=10)

        self.site_label = tk.Label(self, text='Site')
        self.site_label.grid(row=1, column=0, sticky='w')

        self.site_entry = tk.Entry(self)
        self.site_entry.grid(row=1, column=1, sticky='we', padx=10)

        self.login_label = tk.Label(self, text='Login')
        self.login_label.grid(row=2, column=0, sticky='w')

        self.login_entry = tk.Entry(self)
        self.login_entry.grid(row=2, column=1, sticky='we', padx=10)

        self.password_label = tk.Label(self, text='Password')
        self.password_label.grid(row=3, column=0, sticky='w')

        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=3, column=1, sticky='we', padx=10)

        self.ok_button = ttk.Button(self, text='OK', command=self.return_values)
        self.cancel_button = ttk.Button(self, text='CANCEL', command=self.close)
        self.ok_button.grid(row=4, column=0, sticky='we', padx=10, pady=10)
        self.cancel_button.grid(row=4, column=1, sticky='we', padx=10, pady=10)

        self.grid_columnconfigure(index='all', weight=1)

    def return_values(self):
        if self.password_entry.get() == '':
            self.password_entry.insert(tk.END, TableFunctions.generate_password())
        self.new_value = self.id_number[
            'text'], self.site_entry.get(), self.login_entry.get(), self.password_entry.get()
        self.destroy()

    def close(self):
        self.destroy()


class EditWindow(AddEntryWindow):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title('Edit entry')
        self.id_number.config(text=data[0])
        self.site_entry.insert(tk.END, data[1])
        self.login_entry.insert(tk.END, data[2])
        self.password_entry.insert(tk.END, data[3])
