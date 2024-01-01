import mysql.connector
import tkinter
import customtkinter as ctk
import subprocess
from PIL import ImageTk,Image
from tkinter import messagebox as msg

# custom interface color 
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

win = ctk.CTk()
win.geometry('600x400')
win.title('Login')

bgimg = ImageTk.PhotoImage(Image.open("pattern.png"))
l1 = ctk.CTkLabel(master=win,image=bgimg)
l1.pack()

# function
# Link to the signup.py using label
def link():
        win.withdraw()
        subprocess.run(["python", "signup.py"])

def login():
    username = entry1.get()
    password = entry2.get()
    if username == "Admin" and password =="Admin123":
        win.withdraw()
        subprocess.run(["python","admin.py"])
    else:
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
        sql = "SELECT * FROM user_account WHERE username = %s and password = %s "
        val = (username,password,)
        cursor.execute(sql, val)
        result = cursor.fetchone()

        if not result:
            errorLogin.configure(text="Incorrect Username or Password", 
                         text_color="#E84545", 
                         font=('Century Gothic',11))
            entry1.configure(border_color="#E84545")
            entry2.configure(border_color="#E84545")
        else:
            msg.showinfo("Success", "Welcome Back !")
            win.withdraw()
            subprocess.run(["python", "Userinformation.py"])

def home():
    win.withdraw()
    subprocess.run(["python","Home.py"])



# frame
frame = ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

lblTitle = ctk.CTkLabel(master=frame, text="Login",font=('Century Gothic',20), text_color="lightgreen")
lblTitle.place(x=50, y=45)

entry1 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Username')
entry1.place(x=50, y=110)

entry2 = ctk.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=165)

lblacc2 = ctk.CTkLabel(master=frame, text="Sign Up Here",font=('Century Gothic',12), text_color="lightgreen", cursor="hand2")
lblacc2.place(x=190,y=200)
lblacc2.bind("<Button-1>", lambda event: link())

btnLogin = ctk.CTkButton(master=frame, width=220, text="Login",corner_radius=6, command=login)
btnLogin.place(x=50, y=240)

btnHome = ctk.CTkButton(master=frame, width=220, text="Home",corner_radius=6, command=home)
btnHome.place(x=50, y=320)

errorLogin = ctk.CTkLabel(master=frame, width=220, text="")
errorLogin.place(x=50, y=280)

width = win.winfo_screenwidth()            
height = win.winfo_screenheight()

win.geometry(f"{width}x{height}+0+0")
win.mainloop()