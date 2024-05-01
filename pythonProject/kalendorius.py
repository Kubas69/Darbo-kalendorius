import tkinter as tk
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

        self.cur.execute('''CREATE TABLE IF NOT EXISTS data 
                            (id INTEGER PRIMARY KEY, title TEXT, description TEXT, date TEXT, hour INTEGER)''')
        self.conn.commit()

        self.load_data()

    def create_widgets(self):

        self.description_text = tk.Text(self.root, width=30, height=5, bg="#ffd280")
        self.description_text.grid(row=5, column=10, padx=10, pady=5)

        self.edit_btn = tk.Button(self.root, text="Redaguoti", command=self.edit_data, bg="#b37400")
        self.edit_btn.grid(row=4, column=1, padx=10, pady=5)

        self.delete_btn = tk.Button(self.root, text="Ištrinti", command=self.delete_data, bg="#b37400")
        self.delete_btn.grid(row=4, column=2, padx=10, pady=5)

        self.show_all_btn = tk.Button(self.root, text="Rodyti visus", command=self.show_all_data, bg="#b37400")
        self.show_all_btn.grid(row=4, column=3, padx=10, pady=5)

        self.new_entry_btn = tk.Button(self.root, text="Naujas įrašas", command=self.new_entry, bg="#b37400")
        self.new_entry_btn.grid(row=4, column=4, padx=10, pady=5)

        self.data_list = tk.Listbox(self.root, width=50)
        self.data_list.grid(row=5, column=0, columnspan=5, padx=10, pady=5)
        self.data_list.bind("<<ListboxSelect>>", self.show_description)

        self.calendar_frame = tk.Frame(self.root, bg="#cc8500")
        self.calendar_frame.grid(row=6, column=0, columnspan=5, padx=10, pady=5)

        self.create_calendar()

        self.today_label = tk.Label(self.root, text="", bg="#cc8500")
        self.today_label.grid(row=7, column=0, columnspan=5, padx=10, pady=5)

        self.update_today_label()

    def create_calendar(self):
        self.year_var = tk.StringVar()
        self.year_var.set(datetime.now().year)

        self.month_var = tk.StringVar()
        self.month_var.set(datetime.now().month)

        self.day_var = tk.IntVar()
        self.day_var.set(datetime.now().day)

        self.year_menu = tk.OptionMenu(self.calendar_frame, self.year_var, *range(2024, 2025))
        self.year_menu.config(bg="#ffd280")
        self.year_menu.grid(row=0, column=0, padx=5, pady=5)

        self.month_menu = tk.OptionMenu(self.calendar_frame, self.month_var, *range(1, 13))
        self.month_menu.config(bg="#ffd280")
        self.month_menu.grid(row=0, column=1, padx=5, pady=5)

        self.day_spinbox = tk.Spinbox(self.calendar_frame, from_=1, to=31, textvariable=self.day_var, width=5)
        self.day_spinbox.config(bg="#ffd280")
        self.day_spinbox.grid(row=0, column=2, padx=5, pady=5)

        self.show_btn = tk.Button(self.calendar_frame, text="Rodyti", command=self.show_data, bg="#b37400")
        self.show_btn.grid(row=0, column=3, padx=5, pady=5)

        self.month_var.trace("w", self.show_data)
        self.day_var.trace("w", self.show_data)

    def create_calendar_widget(self, edit_window, date_var):
        def select_date():
            selected_date = cal.selection_get().strftime("%Y-%m-%d")
            date_var.set(selected_date)
            cal.destroy()

        cal = Calendar(edit_window, select_mode='day', date_pattern='yyyy-mm-dd')
        cal.grid(row=2, column=2, padx=10, pady=5)
        confirm_button = tk.Button(edit_window, text="Patvirtinti", command=select_date, bg="#b37400")
        confirm_button.grid(row=3, column=2, padx=10, pady=5)

    def load_data(self):
        self.data_list.delete(0, tk.END)
        self.cur.execute("SELECT date, title, hour FROM data ORDER BY date, hour")
        rows = self.cur.fetchall()
        current_date = datetime.now().strftime("%Y-%m-%d")
        for row in rows:
            date = row[0]
            if date < current_date:
                self.data_list.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]} val.)")
                self.data_list.itemconfig(tk.END, {'bg': 'lightgray'})
            else:
                self.data_list.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]} val.)")

    def add_data(self):
        title = self.title_entry.get()
        description = self.description_text.get("1.0", "end-1c")
        date = self.date_entry.get()
        if title and description and date:
            selected_hour = self.hour_var.get()
            self.cur.execute("INSERT INTO data (title, description, date, hour) VALUES (?, ?, ?, ?)",
                             (title, description, date, selected_hour))
            self.conn.commit()
            self.load_data()
            self.title_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)

    def edit_data(self):
        selected = self.data_list.curselection()
        if selected:
            data_info = self.data_list.get(selected[0])
            date = data_info.split(" - ")[0]  # Gauti datą
            title = data_info.split(" - ")[1].split(" (")[0]
            self.open_edit_window(date, title)

    def open_edit_window(self, date, title):
        edit_window = tk.Toplevel(self.root, bg="#cc8500")
        edit_window.title("Redaguoti įrašą")

        self.cur.execute("SELECT * FROM data WHERE date=? AND title=?", (date, title))
        item = self.cur.fetchone()

        tk.Label(edit_window, text="Pavadinimas:", bg="#cc8500").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(edit_window, width=30, bg="#ffd280")
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        title_entry.insert(tk.END, item[1])

        tk.Label(edit_window, text="Aprašymas:", bg="#cc8500").grid(row=1, column=0, padx=10, pady=5)
        description_text = tk.Text(edit_window, width=30, height=5, bg="#ffd280")
        description_text.grid(row=1, column=1, padx=10, pady=5)
        description_text.insert(tk.END, item[2])

        tk.Label(edit_window, text="Data:", bg="#cc8500").grid(row=2, column=0, padx=10, pady=5)
        date_var = tk.StringVar()
        date_entry = tk.Entry(edit_window, width=20, textvariable=date_var, bg="#ffd280")
        date_entry.grid(row=2, column=1, padx=10, pady=5)
        date_entry.insert(tk.END, item[3])

        self.create_calendar_widget(edit_window, date_var)

        tk.Label(edit_window, text="Valanda:", bg="#cc8500").grid(row=4, column=0, padx=10, pady=5)
        hour_var = tk.StringVar(edit_window)
        hour_var.set(item[4])
        hour_menu = tk.OptionMenu(edit_window, hour_var,
                                  *[f"{hour:02d}:{minute:02d}" for hour in range(0, 24) for minute in range(0, 60, 15)])
        hour_menu.config(bg="#ffd280")
        hour_menu.grid(row=4, column=1, padx=10, pady=5)

        save_button = tk.Button(edit_window, text="Išsaugoti", bg="#b37400",
                                command=lambda: self.save_changes(item[0], title_entry.get(),
                                                                  description_text.get("1.0", "end-1c"), date_var.get(),
                                                                  hour_var.get(), edit_window))
        save_button.grid(row=5, columnspan=2, padx=10, pady=5)

    def save_changes(self, id_, title, description, date, hour, edit_window):
        if title and description and date and hour:
            self.cur.execute("UPDATE data SET title=?, description=?, date=?, hour=? WHERE id=?",
                             (title, description, date, hour, id_))
            self.conn.commit()
            self.load_data()
            edit_window.destroy()

    def delete_data(self):
        selected = self.data_list.curselection()
        if selected:
            data_info = self.data_list.get(selected[0])
            date = data_info.split(" - ")[0]
            title = data_info.split(" - ")[1].split(" (")[0]
            self.cur.execute("DELETE FROM data WHERE date=? AND title=?", (date, title))
            self.conn.commit()
            self.load_data()

    def show_data(self, *args):
        self.data_list.delete(0, tk.END)
        selected_year = int(self.year_var.get())
        selected_month = int(self.month_var.get())
        selected_day = int(self.day_var.get())

        selected_date = datetime(selected_year, selected_month, selected_day).strftime("%Y-%m-%d")

        self.cur.execute("SELECT date, title, hour FROM data WHERE date=? ORDER BY hour", (selected_date,))
        rows = self.cur.fetchall()
        for row in rows:
            self.data_list.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]} val.)")

    def show_description(self, event):
        selected = self.data_list.curselection()
        if selected:
            data_info = self.data_list.get(selected[0])
            date = data_info.split(" - ")[0]
            title = data_info.split(" - ")[1].split(" (")[0]
            self.cur.execute("SELECT description FROM data WHERE date=? AND title=?", (date, title))
            description = self.cur.fetchone()[0]
            self.description_text.delete("1.0", tk.END)
            self.description_text.insert(tk.END, description)

    def update_today_label(self):
        today = datetime.now().strftime("%Y-%m-%d")
        day_name = datetime.now().strftime("%A")

        for en, lt in zip(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                          LIETUVISKOS_DIENOS):
            if day_name == en:
                day_name_lt = lt

        self.today_label.config(text=f"Šiandien: {today}, {day_name_lt}")

        sventes = {
            "2024-01-01": "Naujieji metai",
            "2024-02-16": "Lietuvos Valstybės atkūrimo diena",
            "2024-03-11": "Nepriklausomybės atkūrimo diena",
            "2024-03-31": "Velykos",
            "2024-04-01": "Velykų antroji diena",
            "2024-05-01": "Tarptautinė darbo diena",
            "2024-05-05": "Motinos diena",
            "2024-06-02": "Tėvo diena",
            "2024-06-24": "Joninės",
            "2024-07-06": "Karaliaus Mindaugo karūnavimo diena",
            "2024-08-15": "Žolinė",
            "2024-11-01": "Visų šventųjų diena",
            "2024-11-02": "Vėlinės",
            "2024-12-24": "Šv. Kūčios",
            "2024-12-25": "Šv. Kalėdos",
            "2024-12-26": "Šv. Kalėdų antroji diena"
        }

        if today in sventes:
            sventes_pavadinimas = sventes[today]
            self.today_label.config(text=f"Šiandien: {today}, {day_name_lt}, {sventes_pavadinimas}")

    def show_all_data(self):
        self.data_list.delete(0, tk.END)
        self.load_data()

    def new_entry(self):
        new_entry_window = tk.Toplevel(self.root, bg="#cc8500")
        new_entry_window.title("Naujas įrašas")

        tk.Label(new_entry_window, text="Pavadinimas:", bg="#cc8500").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(new_entry_window, width=50, bg="#ffd280")
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(new_entry_window, text="Aprašymas:", bg="#cc8500").grid(row=1, column=0, padx=10, pady=5)
        description_text = tk.Text(new_entry_window, width=50, height=5, bg="#ffd280")
        description_text.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(new_entry_window, text="Data:", bg="#cc8500").grid(row=2, column=0, padx=10, pady=5)
        date_var = tk.StringVar()
        date_entry = tk.Entry(new_entry_window, width=20, textvariable=date_var, bg="#ffd280")
        date_entry.grid(row=2, column=1, padx=10, pady=5)

        self.create_calendar_widget(new_entry_window, date_var)

        tk.Label(new_entry_window, text="Valanda:", bg="#cc8500").grid(row=3, column=0, padx=10, pady=5)
        hour_var = tk.StringVar(new_entry_window)
        hour_var.set("12:00")
        hour_menu = tk.OptionMenu(new_entry_window, hour_var,
                                  *[f"{hour:02d}:{minute:02d}" for hour in range(0, 24) for minute in range(0, 60, 15)])
        hour_menu.config(bg="#ffd280")
        hour_menu.grid(row=3, column=1, padx=10, pady=5)

        save_button = tk.Button(new_entry_window, text="Išsaugoti", bg="#b37400",
                                command=lambda: self.save_new_entry(title_entry.get(),
                                                                    description_text.get("1.0", "end-1c"),
                                                                    date_var.get(), hour_var.get(), new_entry_window))
        save_button.grid(row=4, columnspan=2, padx=10, pady=5)

    def save_new_entry(self, title, description, date, hour, new_entry_window):
        if title and description and date and hour:
            self.cur.execute("INSERT INTO data (title, description, date, hour) VALUES (?, ?, ?, ?)",
                             (title, description, date, hour))
            self.conn.commit()
            self.load_data()
            new_entry_window.destroy()


LIETUVISKOS_DIENOS = ["Pirmadienis", "Antradienis", "Trečiadienis", "Ketvirtadienis", "Penktadienis", "Šeštadienis",
                      "Sekmadienis"]

root = tk.Tk()
app = DatabaseApp(root)
root.mainloop()
