import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from tkcalendar import Calendar


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Darbo kalendorius 2024")
        self.root.configure(bg="#cc8500")

        self.create_widgets()

        self.conn = sqlite3.connect("duomenys.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, title TEXT, description TEXT, 
        date TEXT, hour INTEGER)''')
        self.conn.commit()
        self.load_data()

    def create_widgets(self):
        self.description_text = tk.Text(self.root, width=30, height=5, bg="#ffd280")

root = tk.Tk()
app = DatabaseApp(root)
root.mainloop()
