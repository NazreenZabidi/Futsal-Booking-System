import tkinter as tk
import subprocess
import customtkinter as ctk

def login():
    window.withdraw()
    subprocess.run(["python", "login.py"])

def register():
    window.withdraw()
    subprocess.run(["python", "signup.py"])

def admin():
    window.withdraw()
    subprocess.run(["python", "login.py"])

# Create the main window
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
window = tk.Tk()
window.title("Court Booking System")
window.geometry("750x200")

# Set the background color to dark
window.configure(bg="black")


lblTitle = ctk.CTkLabel(master=window, text="Welcome To The Badminton Court Booking",font=('Century Gothic', 25), text_color="lightgreen")
lblTitle.place(x=125, y=20)

login_btn = ctk.CTkButton(master=window, width=200, text="Login", corner_radius=6, command = login)
login_btn.place(x=165, y=100)

register_btn = ctk.CTkButton(master=window, width=200, text="Register", corner_radius=6, command = register)
register_btn.place(x=375, y=100)

admin_btn = ctk.CTkButton(master=window, width=413, text="Learn More", corner_radius=6, command = admin)
admin_btn.place(x=165, y=135)


window.resizable(False,False)
# Start the main event loop
window.mainloop()