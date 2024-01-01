import mysql.connector
import tkinter
import customtkinter as ctk
import subprocess
import re
from PIL import ImageTk, Image
from tkinter import messagebox as msg

# custom interface color 
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.geometry('600x480')
window.title('Sign Up')

bgimg = ImageTk.PhotoImage(Image.open("pattern.png"))
l1 = ctk.CTkLabel(master=window, image=bgimg)
l1.pack()

# function
# Link to the login.py using label
def back():
    window.withdraw()
    subprocess.run(["python", "login.py"])

def validate():
    username = entry1.get()
    email = entry2.get()
    password = entry3.get()

    # validation for username
    if username.strip() == "":
        error1.configure(text="fill up this fields", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry1.configure(border_color="#E84545")

    elif len(username) < 6 or len(username) > 20:
        error1.configure(text="must be between 6 and 20 characters \nlong", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry1.configure(border_color="#E84545")
    
    elif not all(c.isalnum() or c == '_' for c in username):
        error1.configure(text="must contain only letters, numbers, and \nunderscores", 
                         text_color="#E84545",
                         font=('Century Gothic',11))
        entry1.configure(border_color="#E84545")

    else:
        error1.configure(text="")
        entry1.configure(border_color="green")

    # validation for email
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if email.strip() == "":
        error2.configure(text="fill up this fields", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry2.configure(border_color="#E84545")

    elif re.match(email_pattern, email) is None:
        error2.configure(text="invalid email format", 
                         text_color="#E84545",
                         font=('Century Gothic',11))
        entry2.configure(border_color="#E84545")
    
    else:
        error2.configure(text="")
        entry2.configure(border_color="green")

    # validation for password
    if password.strip() == "":
        error3.configure(text="fill up this fields", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry3.configure(border_color="#E84545")
    
    elif len(password) < 8 or len(password) > 20:
        error3.configure(text="must be between 8 and 20 characters \nlong", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry3.configure(border_color="#E84545")
    
    elif not any(c.isupper() for c in password):
        error3.configure(text="must contain at least one uppercase \nletter", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry3.configure(border_color="#E84545")

    elif not any(c.islower() for c in password):
        error3.configure(text="must contain at least one lowercase \nletter", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry3.configure(border_color="#E84545")

    elif not any(c.isdigit() for c in password):
        error3.configure(text="must contain at least one digit", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
        entry3.configure(border_color="#E84545")

    else:
        error3.configure(text="")
        entry3.configure(border_color="green")

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

        # Check if email already exists in the database
        sql_check_email = "SELECT * FROM user_account WHERE email = %s"
        val_check_email = (email,)
        cursor.execute(sql_check_email, val_check_email)
        result = cursor.fetchone()

        if result:
            msg.showerror("Error", "Email already exists in the database.")
        else:
            # Insert data into the database
            sql_insert = "INSERT INTO user_account (ID, username, email, password) VALUES (NULL, %s, %s, %s)"
            val_insert = (username, email, password)
            cursor.execute(sql_insert, val_insert)
            db.commit()
            ##
            msg.showinfo("Welcome..","You Have Successfully Registered With Us !")
            window.withdraw()
            subprocess.run(['python','login.py'])
            ##

        cursor.close()
        db.close()


# frame
frame = ctk.CTkFrame(master=l1, width=320, height=400, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

lblTitle = ctk.CTkLabel(master=frame, text="Sign Up", font=('Century Gothic',20), text_color="lightgreen")
lblTitle.place(x=50, y=45)

entry1 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=50, y=110)

error1 = ctk.CTkLabel(master=frame, width=220, text="")
error1.place(x=50, y=140)

entry2 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Email')
entry2.place(x=50, y=175)

error2 = ctk.CTkLabel(master=frame, width=220, text="")
error2.place(x=50, y=205)

entry3 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry3.place(x=50, y=235)

error3 = ctk.CTkLabel(master=frame, width=220, text="")
error3.place(x=50, y=265)

btnLogin = ctk.CTkButton(master=frame, width=220, text="Sign Up", corner_radius=6, command=validate)
btnLogin.place(x=50, y=300)

btnBack = ctk.CTkButton(master=frame, width=220, text="Back", corner_radius=6, command=back)
btnBack.place(x=50, y=340)

width = window.winfo_screenwidth()            
height = window.winfo_screenheight()

window.geometry(f"{width}x{height}+0+0")
window.mainloop()
