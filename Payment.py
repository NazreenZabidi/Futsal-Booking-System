import mysql.connector
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import subprocess
from datetime import datetime
import re
from tkinter import messagebox as msg
from PIL import ImageTk, Image

# custom interface color 
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

win = ctk.CTk()
win.title("Payment/Check Out")



def clear():
    # Clear the values in the entry fields and the selected radio button
    name_entered.delete(0, tk.END)
    phone_entered.delete(0, tk.END)
    add_entered.delete('1.0', tk.END)
    email_entered.delete(0, tk.END)
    
    court_chosen.set("")
    dateIn_entered.delete(0, tk.END)
    hour_entered.delete(0, tk.END)

def check():
    name = name_entered.get()
    phone = phone_entered.get()
    address = add_entered.get('1.0', 'end')
    email = email_entered.get()
    court = court_chosen.get()
    date_in = dateIn_entered.get()
    hour = hour_entered.get()
    total = total_entered.get()
    ID = id_entered.get()

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="futsal"
        )

    except mysql.connector.Error as error:
        msg.showerror("Error", "Failed to connect to the database: {}".format(error))
        return

    # Get cursor
    cursor = db.cursor()

    sql_check_data = "SELECT * FROM booking WHERE ID = %s"
    val_check_email = (ID,)
    cursor.execute(sql_check_data, val_check_email)
    result = cursor.fetchone()

    if not result:
        msg.showerror("Error", "ID Is Not Exist.Please Try Again Or Try Another ID")
    else:
        # Display the retrieved data into the entry widgets
        name_entered.delete(0, tk.END)
        name_entered.insert(tk.END, result[1])  # Assuming name is in the second column of the table
        phone_entered.delete(0, tk.END)
        phone_entered.insert(tk.END, result[2])  # Assuming phone is in the third column of the table
        add_entered.delete('1.0', tk.END)
        add_entered.insert(tk.END, result[3])  # Assuming address is in the fourth column of the table
        email_entered.delete(0, tk.END)
        email_entered.insert(tk.END, result[4])  # Assuming email is in the fifth column of the table
        court_chosen.set(result[5])  # Assuming room is in the sixth column of the table
        dateIn_entered.delete(0, tk.END)
        dateIn_entered.insert(tk.END, result[6])  # Assuming check-in date is in the seventh column of the table
        hour_entered.delete(0, tk.END)
        hour_entered.insert(tk.END, result[7])  # Assuming check-out date is in the eighth column of the table
        total_entered.delete(0, tk.END)
        total_entered.insert(tk.END, result[10])  # Assuming total is in the ninth column of the table
        #id_entered.delete(0, tk.END)
        #id_entered.insert(tk.END, result[0])  # Assuming ID is in the first column of the table

        # Disable the room selection combobox
        # Make the other fields read-only
        name_entered.configure(state="disabled")
        phone_entered.configure(state="disabled")
        add_entered.configure(state="disabled")
        email_entered.configure(state="disabled")
        dateIn_entered.configure(state="disabled")
        hour_entered.configure(state="disabled")
        total_entered.configure(state="disabled")
        court_chosen.configure(state="disabled")

    cursor.close()
    db.close()

def CheckOut():
    # Get the entered ID
    entered_id = id_entered.get()


    result = msg.askquestion(title="Exit?", message="Are Sure You Want To Check Out Now ?")
    if result == 'yes':
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="futsal"
            )

            # Get cursor
            cursor = db.cursor()
            # Execute the SQL command to delete the data
            sql_delete_data = "DELETE FROM booking WHERE id = %s"
            val_delete_data = (entered_id,)
            cursor.execute(sql_delete_data, val_delete_data)

            # Commit the changes
            db.commit()

            name_entered.configure(state="normal")
            phone_entered.configure(state="normal")
            add_entered.configure(state="normal")
            email_entered.configure(state="normal")
            dateIn_entered.configure(state="normal")
            hour_entered.configure(state="normal")
            total_entered.configure(state="normal")
            court_chosen.configure(state="normal")

            # Clear the input fields
            id_entered.delete(0, "end")
            name_entered.delete(0, "end")
            phone_entered.delete(0, "end")
            add_entered.delete('1.0', "end")
            email_entered.delete(0, "end")
            dateIn_entered.delete(0, "end")
            hour_entered.delete(0, "end")
            total_entered.delete(0, "end")
            court_chosen.set("")

        except mysql.connector.Error as error:
            msg.showerror("Error", "Failed to connect to the database: {}".format(error))

        finally:
            # Close the database connection
            if db.is_connected():
                msg.showinfo("Thank You", "Thank You For Using Our Service, Come Again !")
                cursor.close()
                db.close()
##
def home():
    result = msg.askquestion(title="Exit?", message="Do you wish to go back?")
    if result =='yes':
        win.withdraw()
        subprocess.run(['python','UserInformation.py'])
##

# Create the title label
lblTitle = ctk.CTkLabel(win, text="- Check Out Details -", font=('Century Gothic', 25), text_color="lightgreen")
lblTitle.pack(pady=30, anchor=tk.CENTER)

# Create the main container frame
chIn_frame = ctk.CTkFrame(win, width=820, height=640, corner_radius=15, fg_color="#293E3B")
chIn_frame.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

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

# court frame
court_frame = ctk.CTkFrame(chIn_frame, width=800, height=220)
court_frame.place(x=10, y=280)

lblRoom = ctk.CTkLabel(master=court_frame, text="Choose Your Room\t    :")
lblRoom.place(x=50, y=30)

lblDateIn = ctk.CTkLabel(master=court_frame, text="Check In Date\t    :")
lblDateIn.place(x=50, y=70)

lblHour = ctk.CTkLabel(master=court_frame, text="Hour Play\t    :")
lblHour.place(x=50, y=110)

lblTotal = ctk.CTkLabel(master=court_frame, text="Total Amount (RM)\t    :")
lblTotal.place(x=50, y=150)

item = ["Single Room", "Twin Room", "Deluxe Room"]
court_chosen = ctk.CTkComboBox(master=court_frame, width=160, values=item, state='readonly')
court_chosen.place(x=200, y=30)
errorRoom = ctk.CTkLabel(master=court_frame, width=100, text="")
errorRoom.place(relx=0.76, y=30)

dateIn_entered = ctk.CTkEntry(master=court_frame, width=160, placeholder_text='dd/mm/yyyy')
dateIn_entered.place(x=200, y=70)
errorDateIn = ctk.CTkLabel(master=court_frame, width=100, text="")
errorDateIn.place(relx=0.76, y=70)

hour_entered = ctk.CTkEntry(master=court_frame, width=160, placeholder_text='hour play')
hour_entered.place(x=200, y=110)
errorHour = ctk.CTkLabel(master=court_frame, width=100, text="")
errorHour.place(relx=0.76, y=110)

total_entered = ctk.CTkEntry(master=court_frame, width=160, placeholder_text='RM')
total_entered.place(x=200, y=150)

# button frame
btn_frame = ctk.CTkFrame(chIn_frame, width=800, height=80)
btn_frame.place(x=10, y=510)

##
home = ctk.CTkButton(master=btn_frame, width=50, text="Home", corner_radius=6, command=home)
home.place(x=30, y=30)
##

clear = ctk.CTkButton(master=btn_frame, width=150, text="Clear", corner_radius=6, command=clear)
clear.place(relx=0.5, y=30)

submit = ctk.CTkButton(master=btn_frame, width=150, text="Pay", corner_radius=6, command=CheckOut)
submit.place(x=245, y=30)

lblID = ctk.CTkLabel(master=btn_frame, text="ID")
lblID.place(x=600, y=30)
id_entered = ctk.CTkEntry(master=btn_frame, width=50, placeholder_text='ID')
id_entered.place(x=620, y=30)

check = ctk.CTkButton(master=btn_frame, width=50, text="Check", corner_radius=6,command=check)
check.place(x=680, y=30)

errorAll = ctk.CTkLabel(master=chIn_frame, width=220, text="")
errorAll.place(x=300, y=610)

width = win.winfo_screenwidth()            
height = win.winfo_screenheight()

win.geometry(f"{width}x{height}+0+0")
win.mainloop()