import mysql.connector
import tkinter as tk
import subprocess
import re
import customtkinter as ctk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageFilter
from tkinter import messagebox as msg

# Initialize the terms window as None
terms_window = None
policy_window = None


# custom interface color 
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

win = ctk.CTk()
win.title("Home Page")


bgimg = ImageTk.PhotoImage(Image.open("pattern.png"))
l1 = ctk.CTkLabel(master=win,image=bgimg)
l1.pack()

# function
# clear all the input fields value
def clear():
	#clear entry box
	name_entered.delete(0, ctk.END)
	phone_entered.delete(0, ctk.END)
	add_entered.delete(0, ctk.END)
	email_entered.delete(0, ctk.END)

	# Deselect radio buttons
	radVar.set(None)
    
    # Reset error labels
	errorName.configure(text="")
	errorPhone.configure(text="")
	errorAddress.configure(text="")
	errorEmail.configure(text="")
	errorChoose.configure(text="")
    
    # Reset border colors
	name_entered.configure(ctk.CTkEntry)
	phone_entered.configure(ctk.CTkEntry)
	add_entered.configure(ctk.CTkEntry)
	email_entered.configure(ctk.CTkEntry)



def cancel():
    result = messagebox.askquestion(title="Exit?", message="Do you want to close the program?")
    if result == 'yes':
    	win.withdraw()
    	subprocess.run(["python", "login.py"])


def submit():
    terms_checked = terms_var.get()
    policies_checked = policies_var.get()

    # Check the selected option for "Check In" or "Check Out"
    if not radVar.get() in (1, 2):
        errorChoose.configure(text="choose either Check In or Check Out",
                              text_color="#E84545",
                              font=('Century Gothic', 11))

    elif radVar.get() == 1:
    	if not terms_checked or not policies_checked:
    		messagebox.showwarning("Missing Information", "Please accept the terms and policies.")
    	else:		        
    		subprocess.run(["python", "Booking.py"])



    elif radVar.get() == 2:
        if not terms_checked or not policies_checked:
            messagebox.showwarning("Missing Information", "Please accept the terms and policies.")
        else:               
            subprocess.run(["python", "Payment.py"])


def show_terms_window():
    global terms_window

    # Check if the terms window is already open
    if terms_window is not None and terms_window.winfo_exists():
        terms_window.lift()
        return

    # Create a new Toplevel window to show the terms and conditions
    terms_window = tk.Toplevel(win)
    terms_window.title("Terms and Conditions")
    terms_text = """
    1. By using our website, you agree to our terms and conditions, which include the use of cookies to improve your browsing experience.
    2. Our service is provided "as is" and we make no warranty or guarantee as to its accuracy, reliability, or suitability for your specific needs.
    3. Payment is required at the time of booking and all fees are non-refundable.
    4. We reserve the right to modify or terminate our service at any time, without notice or liability to you.
    5. You agree not to use our service for any illegal or unauthorized purpose, and to comply with all applicable laws and regulations.
    6. Our liability to you for any claim arising from your use of our service is limited to the amount you paid for the service.
    7. We may suspend or terminate your account at any time if we believe you have violated our terms and conditions.
    8. By submitting content to our website, you grant us a non-exclusive, royalty-free, perpetual, and irrevocable license to use, reproduce, modify,
       and distribute the content in any form and for any purpose. 
    9. We may send you promotional emails or newsletters from time to time, but you may opt-out of receiving them at any time by following the instructions provided.
    10. Any dispute arising from your use of our service will be governed by the laws of the jurisdiction in which we are located,
       and you agree to submit to the exclusive jurisdiction of the courts in that jurisdiction.
    """

    terms_text_widget = tk.Text(terms_window)
    terms_text_widget.insert(tk.END, terms_text)
    terms_text_widget.pack(fill=tk.BOTH, expand=True)

    # Add a close button to the window
    close_button = ctk.CTkButton(terms_window, text="Close", command=terms_window.destroy)
    close_button.pack()


def show_policy():
    global policy_window
    
    # Check if the terms window is already open
    if policy_window is not None and policy_window.winfo_exists():
        policy_window.lift()
        return
    
    # Create a new window with a text widget containing the terms and conditions
    policy_window = tk.Toplevel(win)
    policy_window.title("Privacy Policy")
    policy_text = """
    1. Our privacy policy outlines how we collect, use, and protect your personal information when you use our service.
    2. We do not share your personal information with third parties for marketing purposes without your explicit consent.
    3. Our policy prohibits discrimination against any individual on the basis of their race, ethnicity, religion, gender, sexual orientation, or age.
    4. We have a zero-tolerance policy for harassment or abusive behavior and will take appropriate action against anyone who violates this policy.
    5. Our policy regarding refunds and cancellations is outlined in our terms and conditions and is subject to change without notice.
    6. We reserve the right to modify our policy at any time, and any changes will be posted on our website.
    7. Our policy on intellectual property rights outlines how we respect the intellectual property of others and expect our users to do the same.
    8. Our policy on data retention specifies how long we will keep your personal information and under what circumstances we may delete it.
    9. Our policy on information security outlines the measures we take to protect your personal information from unauthorized access, disclosure, or use.
    10.Our policy on accessibility outlines our commitment to making our service accessible to all users, including those with disabilities.
    """


    terms_text_widget = tk.Text(policy_window)
    terms_text_widget.insert(tk.END, policy_text)
    terms_text_widget.pack(fill=tk.BOTH, expand=True)


     # Add a close button to the window
    close_button = ctk.CTkButton(policy_window, text="Close", command=policy_window.destroy)
    close_button.pack()

# Create an info container
frame = ctk.CTkFrame(master=l1, width=900, height=660, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


#title company name
lblTitle = ctk.CTkLabel(master=frame, text="- WELCOME TO N.A.Z FUTSAL CENTER -",font=('Century Gothic',20, "bold"), text_color="lightgreen")
lblTitle.place(x=50, y=45)

# Create variable for radiobutton value
radVar = ctk.IntVar()


# Create a checkbox with the "Terms and Condition*" sentence
terms_var = ctk.CTkCheckBox(master=frame, text="I have read and agree to the", width=80)
terms_var.deselect()
terms_var.place(relx=0.05, y=180)

# Create the hyperlink label
terms_label = ctk.CTkLabel(master=frame, text=" Terms and Conditions*", text_color="yellow", cursor="hand2")
terms_label.pack(side=tk.LEFT)
terms_label.place(relx=0.26, y=178)

# Bind the hyperlink label to the show_terms() function when the user clicks on it
terms_label.bind("<Button-1>", lambda e: show_terms_window())

# Create a checkbox with the "Policy*" sentence
policies_var = ctk.CTkCheckBox(master=frame, text="I have read and agree to the", width=80)
policies_var.deselect()
policies_var.place(relx=0.05, y=210)

# Create the hyperlink label
policy_label = ctk.CTkLabel(master=frame, text=" Policy*", text_color="yellow", cursor="hand2")
policy_label.pack(side=tk.LEFT)
policy_label.place(relx=0.26, y=208)

# Bind the hyperlink label to the show_terms() function when the user clicks on it
policy_label.bind("<Button-1>", lambda e: show_policy())


lblChoose = ctk.CTkLabel(master=frame, text="Choose :",font=('Century Gothic',15), text_color="lightgreen")
lblChoose.place(x=50, y=350)
rad1 = ctk.CTkRadioButton(master=frame, text="Booking", variable=radVar, value=1)
rad1.place(x=130, y=355)
rad2 = ctk.CTkRadioButton(master=frame, text="Payment", variable=radVar, value=2)
rad2.place(x=250, y=355)

errorChoose = ctk.CTkLabel(master=frame, width=220, text="")
errorChoose.place(x=350, y=350)

cancel = ctk.CTkButton(master=frame, width=150, text="Cancel",corner_radius=6, command=cancel)
cancel.place(x=130, y=480)

submit = ctk.CTkButton(master=frame, width=150, text="Submit",corner_radius=6, command=submit)
submit.place(x=130, y=520)

# Court details
lblRoomDetails = ctk.CTkLabel(master=frame, text="COURT DETAILS",font=('Century Gothic',17, "bold"), text_color="lightgreen")
lblRoomDetails.place(x=580, y=45)

# Court A
secframe = ctk.CTkFrame(master=frame)
secframe.place(x=420, y=90, anchor="nw")

lblFrameTitle = ctk.CTkLabel(master=secframe, text="Court A", font=('Century Gothic',15, "bold"), text_color="lightgreen")
lblFrameTitle.pack(padx=15, pady=10, anchor="w")

# Load the image
court_image = Image.open("court.jpg")
court_image = court_image.resize((130, 130))

court_image = ImageTk.PhotoImage(court_image)

# Create a label to display the image
court_image_label = tk.Label(secframe, image=court_image)
court_image_label.image = court_image  # Keep a reference to the image to prevent it from being garbage collected
court_image_label.pack(padx=15, pady=10, anchor="w")


lblCap1 = ctk.CTkLabel(master=secframe, text="Court Capacity  : 14 Person",font=('Century Gothic',12), text_color="lightgreen")
lblCap1.pack(padx=15, anchor="w")

lblPrice1 = ctk.CTkLabel(master=secframe, text="Court Price/Hour : RM 80/hour",font=('Century Gothic',12), text_color="lightgreen")
lblPrice1.pack(padx=15, anchor="w")


# Court B
trdframe = ctk.CTkFrame(master=frame)
trdframe.place(x=650, y=90, anchor="nw")

lbltitle2 = ctk.CTkLabel(master=trdframe, text="Court B",font=('Century Gothic',15, "bold"), text_color="lightgreen")
lbltitle2.pack(padx=15, pady=10, anchor="w")
# Load the image
court_image = Image.open("court.jpg")
court_image = court_image.resize((130, 130))  # Resize the image if needed
court_image = ImageTk.PhotoImage(court_image)

# Create a label to display the image
court_image_label = tk.Label(trdframe, image=court_image)
court_image_label.image = court_image  # Keep a reference to the image to prevent it from being garbage collected
court_image_label.pack(padx=15, pady=10, anchor="w")


lblCap2 = ctk.CTkLabel(master=trdframe, text="Court Capacity  : 12 Person",font=('Century Gothic',12), text_color="lightgreen")
lblCap2.pack(padx=15, anchor="w")

lblPrice2 = ctk.CTkLabel(master=trdframe, text="Court Price/Hour : RM 65/hour",font=('Century Gothic',12), text_color="lightgreen")
lblPrice2.pack(padx=15, anchor="w")


# Court C
fthframe = ctk.CTkFrame(master=frame)
fthframe.place(x=550, y=370, anchor="nw")

lbltitle3 = ctk.CTkLabel(master=fthframe, text="Court C",font=('Century Gothic',15, "bold"), text_color="lightgreen")
lbltitle3.pack(padx=15, pady=10, anchor="w")

# Load the image
court_image = Image.open("court.jpg")
court_image = court_image.resize((130, 130))  # Resize the image if needed
court_image = ImageTk.PhotoImage(court_image)

# Create a label to display the image
court_image_label = tk.Label(fthframe, image=court_image)
court_image_label.image = court_image  # Keep a reference to the image to prevent it from being garbage collected
court_image_label.pack(padx=15, pady=10, anchor="w")

lblCap3 = ctk.CTkLabel(master=fthframe, text="Court Capacity  : 10 Person",font=('Century Gothic',12), text_color="lightgreen")
lblCap3.pack(padx=15, anchor="w")

lblPrice3 = ctk.CTkLabel(master=fthframe, text="Court Price/Night : RM 55/hour",font=('Century Gothic',12), text_color="lightgreen")
lblPrice3.pack(padx=15, anchor="w")



width = win.winfo_screenwidth()            
height = win.winfo_screenheight()

win.geometry(f"{width}x{height}+0+0")
win.mainloop()