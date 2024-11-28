import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime as datetime

class Hotel:
    sortParam = 'name'

    def __init__(self, name='', room='', checkInDate='', checkOutDate='', housekeeper=False, bookingCost=0):
        self.name = name
        self.room = room
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
        self.housekeeper = housekeeper
        self.bookingCost = bookingCost

    def __lt__(self, other):
        return getattr(self, Hotel.sortParam) < getattr(other, Hotel.sortParam)

    @classmethod
    def sortByRate(cls):
        cls.sortParam = 'rating'

    @classmethod
    def sortByRoomAvailable(cls):
        cls.sortParam = 'room'
class User:
        def __init__(self, uname='', uId=0, cost=0):
            self.uname = uname
            self.uId = uId
            self.cost = cost

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.conn = sqlite3.connect('hotel_management.db')
        self.create_tables()
        self.hotels = []
        self.users = []
        self.load_data_from_db()

        self.tabControl = ttk.Notebook(root)
        self.tabHotelData = ttk.Frame(self.tabControl)
        self.tabUserData = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tabHotelData, text='Hotels')
        self.tabControl.add(self.tabUserData, text='Customers information')
        self.tabControl.pack(expand=1, fill="both")

        self.create_hotel_tab()
        self.create_user_tab()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS hotels (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT,
                                    room TEXT,
                                    checkInDate TEXT,
                                    checkOutDate TEXT,
                                    housekeeper INTEGER,
                                    bookingCost INTEGER
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    uname TEXT,
                                    uId INTEGER,
                                    cost INTEGER
                                )''')

    def load_data_from_db(self):
        cursor = self.conn.execute('SELECT name, room, checkInDate, checkOutDate, housekeeper, bookingCost FROM hotels')
        for row in cursor:
            h = Hotel(*row)
            self.hotels.append(h)

    def create_hotel_tab(self):
        self.hotel_tree = ttk.Treeview(self.tabHotelData, columns=("Name", "Room", "Check-in", "Check-out", "Housekeeper", "Booking Cost"), show="headings")
        self.hotel_tree.heading("Name", text="Hotel Name")
        self.hotel_tree.heading("Room", text="Room")
        self.hotel_tree.heading("Check-in", text="Check-in Date")
        self.hotel_tree.heading("Check-out", text="Check-out Date")
        self.hotel_tree.heading("Housekeeper", text="Housekeeper")
        self.hotel_tree.heading("Booking Cost", text="Booking Cost ($)")
        self.hotel_tree.pack(expand=True, fill='both')

        self.update_hotel_tree()

        insert_btn = ttk.Button(self.tabHotelData, text="Add New Hotel Booking", command=self.insert_hotel_data)
        insert_btn.pack(pady=10)
        
        sort_frame = ttk.Frame(self.tabHotelData)
        sort_frame.pack(pady=10)

        btn_sort_name = ttk.Button(sort_frame, text="Sort by Name", command=self.sort_by_name)
        btn_sort_name.grid(row=0, column=0, padx=5)

        btn_sort_rating = ttk.Button(sort_frame, text="Sort by Rating", command=self.sort_by_rating)
        btn_sort_rating.grid(row=0, column=1, padx=5)

    def update_hotel_tree(self):
        for item in self.hotel_tree.get_children():
            self.hotel_tree.delete(item)
        for h in self.hotels:
            self.hotel_tree.insert('', 'end', values=(h.name, h.room, h.checkInDate, h.checkOutDate, "Yes" if h.housekeeper else "No", h.bookingCost))


    def sort_by_name(self):
        Hotel.sortByName()
        self.hotels.sort()
        self.update_hotel_tree()

    def sort_by_rating(self):
        Hotel.sortByRate()
        self.hotels.sort()
        self.update_hotel_tree()

    def sort_by_rooms(self):
        Hotel.sortByRoomAvailable()
        self.hotels.sort()
        self.update_hotel_tree()

    def create_user_tab(self):
        self.user_tree = ttk.Treeview(self.tabUserData, columns=("Name", "ID", "Cost"), show="headings")
        self.user_tree.heading("Name", text="Customer Name")
        self.user_tree.heading("ID", text="Customer ID")
        self.user_tree.heading("Cost", text="Booking Cost")
        self.user_tree.pack(expand=True, fill='both')

        for u in self.users:
            self.user_tree.insert('', 'end', values=(u.uname, u.uId, u.cost))

        insert_user_btn = ttk.Button(self.tabUserData, text="Add New Customer", command=self.insert_user_data)
        insert_user_btn.pack(pady=10)

    def insert_hotel_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Add New Hotel")

        tk.Label(new_window, text="Hotel Name").grid(row=0, column=0)
        tk.Label(new_window, text="Room").grid(row=1, column=0)
        tk.Label(new_window, text="Check-in Date").grid(row=2, column=0)
        tk.Label(new_window, text="Check-out Date").grid(row=3, column=0)
        tk.Label(new_window, text="Housekeeper Available").grid(row=4, column=0)
        tk.Label(new_window, text="Booking Cost").grid(row=5, column=0)

        name_entry = tk.Entry(new_window)
        room_entry = tk.Entry(new_window)
        checkin_entry = tk.Entry(new_window)
        checkout_entry = tk.Entry(new_window)
        housekeeper_var = tk.IntVar()
        housekeeper_check = tk.Checkbutton(new_window, variable=housekeeper_var)
        cost_entry = tk.Entry(new_window)

        name_entry.grid(row=0, column=1)
        room_entry.grid(row=1, column=1)
        checkin_entry.grid(row=2, column=1)
        checkout_entry.grid(row=3, column=1)
        housekeeper_check.grid(row=4, column=1)
        cost_entry.grid(row=5, column=1)

        def save_hotel():
            name = name_entry.get()
            room = room_entry.get()
            checkInDate = checkin_entry.get()
            checkOutDate = checkout_entry.get()
            housekeeper = housekeeper_var.get() == 1
            bookingCost = int(cost_entry.get())

            h = Hotel(name, room, checkInDate, checkOutDate, housekeeper, bookingCost)
            self.hotels.append(h)
            self.conn.execute('INSERT INTO hotels (name, room, checkInDate, checkOutDate, housekeeper, bookingCost) VALUES (?, ?, ?, ?, ?, ?)',
                              (name, room, checkInDate, checkOutDate, int(housekeeper), bookingCost))
            self.conn.commit()
            self.update_hotel_tree()
            new_window.destroy()
            messagebox.showinfo("Success", "New hotel booking added successfully!")

        tk.Button(new_window, text="Add Booking", command=save_hotel).grid(row=6, columnspan=2)
    def load_users_from_db(self):
        cursor = self.conn.execute('SELECT uname, uId, cost FROM users')
        for row in cursor:
            u = User(*row)
            self.users.append(u)

    def insert_user_data(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Add New User")

        tk.Label(new_window, text="User Name").grid(row=0, column=0)
        tk.Label(new_window, text="User ID").grid(row=1, column=0)
        tk.Label(new_window, text="Booking Cost").grid(row=2, column=0)

        name_entry = tk.Entry(new_window)
        id_entry = tk.Entry(new_window)
        cost_entry = tk.Entry(new_window)

        name_entry.grid(row=0, column=1)
        id_entry.grid(row=1, column=1)
        cost_entry.grid(row=2, column=1)

        def save_user():
            uname = name_entry.get()
            uId = int(id_entry.get())
            cost = int(cost_entry.get())

            u = User(uname, uId, cost)
            self.users.append(u)
            self.conn.execute('INSERT INTO users (uname, uId, cost) VALUES (?, ?, ?)', (uname, uId, cost))
            self.conn.commit()
            self.user_tree.insert('', 'end', values=(uname, uId, cost))
            new_window.destroy()
            messagebox.showinfo("Success", "New user added successfully!")

        tk.Button(new_window, text="Add User", command=save_user).grid(row=3, columnspan=2)


if __name__ == '__main__':
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
