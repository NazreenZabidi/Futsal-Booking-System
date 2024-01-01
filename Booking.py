import mysql.connector
import tkinter as tk
import customtkinter as ctk
import subprocess
from tkcalendar import Calendar
from tkinter import messagebox
from datetime import datetime
import re

# Custom interface color
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

win = ctk.CTk()
win.title("Booking")

def clear():
    # Clear the values in the entry fields and the selected checkboxes
    name_entered.delete(0, tk.END)
    phone_entered.delete(0, tk.END)
    add_entered.delete('1.0', tk.END)
    email_entered.delete(0, tk.END)

    court_chosen.set("")
    dateIn_entered.delete(0, tk.END)
    hour_chosen.set("")
    check1.deselect()
    check2.deselect()

def submit():
    name = name_entered.get()
    phone = phone_entered.get()
    address = add_entered.get('1.0', 'end')
    email = email_entered.get()
    court = court_chosen.get()
    dateIn = dateIn_entered.get()
    hour = hour_chosen.get()
    ball = check1.get()
    drink = check2.get()
    total = 0.0

    # Capture the current time and date
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # Check if any of the fields are empty
    if any(field.strip() == "" for field in (name, phone, address, email, court, dateIn, hour)):
        errorAll.configure(text="*fill up all the fields",
                           text_color="#E84545",
                           font=('Century Gothic', 15, "bold"))
    else:
        # Validation for name
        if not name.replace(" ", "").isalpha():
            errorName.configure(text="*please write your name properly",
                                text_color="#E84545",
                                font=('Century Gothic', 11))
            name_entered.configure(border_color="#E84545")
        else:
            errorName.configure(text="")
            name_entered.configure(border_color="green")

        # Validation for phone number
        format = re.compile(r'^\d{3}-\d{8}$')
        match = format.match(phone)

        if not match:
            errorPhone.configure(text="*must be in xxx-xxxxxxxx format",
                                 text_color="#E84545",
                                 font=('Century Gothic', 11))
            phone_entered.configure(border_color="#E84545")
        else:
            errorPhone.configure(text="")
            phone_entered.configure(border_color="green")

        # Validation for address
        if not address.strip():
            errorAddress.configure(text="*fill up this field",
                                   text_color="#E84545",
                                   font=('Century Gothic', 11))
            add_entered.configure(border_color="#E84545")
        else:
            errorAddress.configure(text="")
            add_entered.configure(border_color="green")

        # Validation for email
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(email_pattern, email):
            errorEmail.configure(text="invalid email format",
                                 text_color="#E84545",
                                 font=('Century Gothic', 11))
            email_entered.configure(border_color="#E84545")
        else:
            errorEmail.configure(text="")
            email_entered.configure(border_color="green")

        # Validation for court
        if not court.strip():
            errorCourt.configure(text="*fill up this field",
                                 text_color="#E84545",
                                 font=('Century Gothic', 11))
            court_chosen.configure(border_color="#E84545")
        else:
            errorCourt.configure(text="")
            court_chosen.configure(border_color="green")

        # Validation for Check In Date
        date_format1 = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/\d{4}$"

        if not re.match(date_format1, dateIn):
            errorDateIn.configure(text="*incorrect date format",
                                  text_color="#E84545",
                                  font=('Century Gothic', 11))
            dateIn_entered.configure(border_color="#E84545")
        else:
            errorDateIn.configure(text="")
            dateIn_entered.configure(border_color="green")

        # Validation for hour
        if not hour.strip():
            errorHour.configure(text="*fill up this field",
                                text_color="#E84545",
                                font=('Century Gothic', 11))
            hour_chosen.configure(border_color="#E84545")
        else:
            errorHour.configure(text="")
            hour_chosen.configure(border_color="green")

        try:
            court_type = court_chosen.get()

            if court_type == "Court A":
                court_price = 80.0
            elif court_type == "Court B":
                court_price = 65.0
            elif court_type == "Court C":
                court_price = 55.0
            else:
                court_price = 0.0

            # Calculate the number of hours based on the selected option
            if hour_chosen.get() == "1 Hour":
                num_hours = 1
            elif hour_chosen.get() == "1 Hour 45 Minute":
                num_hours = 1.75
            elif hour_chosen.get() == "2 Hour":
                num_hours = 2
            else:
                num_hours = 0

            # Calculate the total amount
            total = court_price * num_hours

            # Include ball charge if selected
            if check1.get():
                total += 20.0  # Ball charge

            # Include drink charge if selected
            if check2.get():
                total += 15.0  # Drink charge

        except ValueError:
            print("Invalid date format entered.")

        if errorName.cget("text") == "" and errorPhone.cget("text") == "" and errorAddress.cget("text") == "" and errorEmail.cget("text") == "" and errorCourt.cget("text") == "" and errorDateIn.cget("text") == "" and errorHour.cget("text") == "":
            # All fields are in the correct format
            result = messagebox.askquestion(title="Exit?", message="Are you sure you want to book with these values?")
            if result == 'yes':
                # Clear the input fields
                clear()

                try:
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="futsal"
                    )
                except mysql.connector.Error as error:
                    messagebox.showerror("Error", "Failed to connect to the database: {}".format(error))
                    return

                # Get cursor
                cursor = db.cursor()

                # Insert data into the database
                sql_insert = "INSERT INTO booking (ID, Name, Phone, Address, Email, Type_court, Check_In_Date, Hour, Ball, Drink, Total_Amount) VALUES (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val_insert = (name, phone, address, email, court, dateIn, hour, ball, drink, total)


                # Execute the SQL statement
                cursor.execute(sql_insert, val_insert)

                db.commit()

                # Retrieve last inserted ID
                last_insert_id = cursor.lastrowid

                # Close cursor and database connection
                cursor.close()
                db.close()

                # Show message box with confirmation and ID
                messagebox.showinfo("Booking Confirmed", "************\nBooking Receipt\n************\n\nID: #{}\nReserved at: {}\nTotal Amount: RM{}\n\nThank you for choosing our service!\n\nPlease proceed to pay your fee upon arriving.\n\n************".format(last_insert_id, formatted_datetime, total))

def home():
    result = messagebox.askquestion(title="Exit?", message="Do you wish to go back?")
    if result == 'yes':
        win.withdraw()
        subprocess.run(['python', 'UserInformation.py'])

class CustomDateEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Button-1>", self.show_calendar)

    def show_calendar(self, event):
        top = tk.Toplevel(self)
        cal = Calendar(top, date_pattern='dd/MM/yyyy')
        cal.pack()

        def set_date():
            self.delete(0, tk.END)
            self.insert(0, cal.get_date())
            top.destroy()

        ok_button = tk.Button(top, text="OK", command=set_date)
        ok_button.pack()

# Create the title label
lblTitle = ctk.CTkLabel(win, text="- Booking Details -", font=('Century Gothic', 25), text_color="lightgreen")
lblTitle.pack(pady=30, anchor=tk.CENTER)

# Create the main container frame
chIn_frame = ctk.CTkFrame(win, width=820, height=660, corner_radius=15, fg_color="#293E3B")
chIn_frame.place(relx=0.5, rely=0.53, anchor=tk.CENTER)

# Create the customer details frame
cust_frame = ctk.CTkFrame(chIn_frame, width=800, height=260)
cust_frame.place(x=10, y=10)

# Add labels and input fields for customer details
lblName = ctk.CTkLabel(master=cust_frame, text="Name\t\t    :")
lblName.place(x=50, y=30)
name_entered = ctk.CTkEntry(master=cust_frame, width=350, placeholder_text='Name')
name_entered.place(x=200, y=30)
errorName = ctk.CTkLabel(master=cust_frame, width=220, text="")
errorName.place(x=550, y=30)

lblPhone = ctk.CTkLabel(master=cust_frame, text="Phone\t\t    :")
lblPhone.place(x=50, y=70)
phone_entered = ctk.CTkEntry(master=cust_frame, width=350, placeholder_text='Phone Number')
phone_entered.place(x=200, y=70)
errorPhone = ctk.CTkLabel(master=cust_frame, width=220, text="")
errorPhone.place(x=550, y=70)

lblAddress = ctk.CTkLabel(master=cust_frame, text="Address\t\t    :")
lblAddress.place(x=50, y=110)
add_entered = ctk.CTkTextbox(master=cust_frame, width=350, height=100)
add_entered.place(x=200, y=110)
errorAddress = ctk.CTkLabel(master=cust_frame, width=220, text="")
errorAddress.place(x=550, y=110)

lblEmail = ctk.CTkLabel(master=cust_frame, text="Email\t\t    :")
lblEmail.place(x=50, y=220)
email_entered = ctk.CTkEntry(master=cust_frame, width=350, placeholder_text='Email')
email_entered.place(x=200, y=220)
errorEmail = ctk.CTkLabel(master=cust_frame, width=220, text="")
errorEmail.place(x=550, y=220)

# Court frame
court_frame = ctk.CTkFrame(chIn_frame, width=800, height=220)
court_frame.place(x=10, y=280)

lblCourt = ctk.CTkLabel(master=court_frame, text="Choose Your Court\t    :")
lblCourt.place(x=50, y=30)

lblBook = ctk.CTkLabel(master=court_frame, text="Booking Date\t    :")
lblBook.place(x=50, y=70)

lblHour = ctk.CTkLabel(master=court_frame, text="Hour Play\t    :")
lblHour.place(x=50, y=110)

lblService = ctk.CTkLabel(master=court_frame, text="Additional Service\t    :")
lblService.place(x=50, y=150)

item = ["Court A", "Court B", "Court C"]
court_chosen = ctk.CTkComboBox(master=court_frame, width=160, values=item, state='readonly')
court_chosen.place(x=200, y=30)
errorCourt = ctk.CTkLabel(master=court_frame, width=100, text="")
errorCourt.place(relx=0.76, y=30)

dateIn_entered = CustomDateEntry(master=court_frame, width=160, placeholder_text='dd/mm/yyyy')
dateIn_entered.place(x=200, y=70)
errorDateIn = ctk.CTkLabel(master=court_frame, width=100, text="")

errorDateIn.place(relx=0.76, y=70)

item = ["1 Hour", "1 Hour 45 Minute", "2 Hour"]
hour_chosen = ctk.CTkComboBox(master=court_frame, width=160, values=item, state='readonly')
hour_chosen.place(x=200, y=110)
errorHour = ctk.CTkLabel(master=court_frame, width=100, text="")
errorHour.place(relx=0.76, y=110)

check1 = ctk.CTkCheckBox(master=court_frame, text="Ball", width=80)
check1.deselect()
check1.place(x=200, y=160)

check2 = ctk.CTkCheckBox(master=court_frame, text="Drink", width=80)
check2.deselect()
check2.place(x=330, y=160)

# Button frame
btn_frame = ctk.CTkFrame(chIn_frame, width=800, height=80)
btn_frame.place(x=10, y=510)

home_button = ctk.CTkButton(master=btn_frame, width=50, text="Home", corner_radius=6, command=home)
home_button.place(x=30, y=30)

clear_button = ctk.CTkButton(master=btn_frame, width=150, text="Clear", corner_radius=6, command=clear)
clear_button.place(relx=0.5, y=30)

submit_button = ctk.CTkButton(master=btn_frame, width=150, text="Submit", corner_radius=6, command=submit)
submit_button.place(x=245, y=30)

errorAll = ctk.CTkLabel(master=chIn_frame, width=220, text="")
errorAll.place(x=300, y=610)

width = win.winfo_screenwidth()
height = win.winfo_screenheight()

win.geometry(f"{width}x{height}+0+0")
win.mainloop()
