#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

#Initial Processes, makes sure the file is created first
user_data = open("userdata.txt","a+")
email_database = open("EmailDatabase.txt","a+")
user_data.close()
email_database.close()

#Function to create the window for sending emails
def main_window():
    main_window = tk.Tk()
    main_window.title("Email System(Sending Mail)")
    main_window.geometry("500x400")
    main_window.configure(bg='#212121')
    
    # create a themed style
    style = ttk.Style(main_window)
    style.theme_use("clam")  # use the "clam" theme
    style.configure("TLabel", font=('Arial', 14, 'bold'), foreground="white", background='#212121')

    #The Labels in the window
    label = ttk.Label(main_window, text="From: ")
    label.grid(row=0, column=0, padx=5, pady=5)
    label = ttk.Label(main_window, text="To: ")
    label.grid(row=1, column=0, padx=5, pady=5)
    label = ttk.Label(main_window, text="Title: ")
    label.grid(row=2, column=0, padx=5, pady=5)

    # Label for who the email is From
    From_useremail = ttk.Label(main_window, text=email_input)
    From_useremail.grid(row=0, column=1, padx=5, pady=5)

    # add an Entry widget for who the email is To
    To_entry = ttk.Entry(main_window, font=("Helvetica", 12))
    To_entry.grid(row=1, column=1, padx=5, pady=5)
    # add an Entry widget for the Title of the Email
    title_entry = ttk.Entry(main_window, font=("Helvetica", 12))
    title_entry.grid(row=2, column=1, padx=5, pady=5)

    # create a Text widget for the user to input text
    body = tk.Text(main_window, width=40, height=10, font=("Helvetica", 12))
    body.grid(row=3, column=1, padx=5, pady=5)

    #Function to retrieve the input text
    def get_input():
        From = email_input
        To = To_entry.get()
        Title = title_entry.get()
        Body = body.get("1.0", tk.END)

        with open("userdata.txt", "r") as f:
            data = f.readlines()
            user_list = [line.strip().split(",") for line in data]

        email_exists = False
        for user in user_list:
            if user[0] == To:
                email_exists = True
                break
        if email_exists:
                email_database = open("EmailDatabase.txt","a")
                email_database.write("From: "+From+"\n"+
                                    "To: "+To+"\n"+
                                    "Title: "+Title+"\n"+
                                    Body+"\n%")
                messagebox.showinfo(title="Email sent", message="Your email has been sent successfully!")
        else:
                messagebox.showerror(title="Email error", message="The email entered is not in the email database.")

    def log_out():
        main_window.destroy()
        menu_window()
        
    
    
    #Mail Box Window
    def mailbox():
        mailbox = tk.Tk()
        mailbox.title("Email System(Mailbox)")
        mailbox.geometry("400x300")
        mailbox.configure(bg='#212121')

        # create a themed style
        style = ttk.Style(mailbox)
        style.theme_use("clam")  # use the "clam" theme
        # Create the listbox
        listbox = tk.Listbox(mailbox, width=50,height=20, font=("Helvetica", 12), foreground="white", background="#212121", selectbackground="#6d4c41", selectforeground="white")
        # Open the file and read the lines
        with open("EmailDatabase.txt","r") as f:
            data = f.read()
            Emails = data.split("%")
            Emails.reverse() #So the latest entry is inserted first to be viewed at the top of the listbox
        new_list = [email.strip().split('\n') for email in Emails]
        #This removes any empty lists from new_list
        while new_list and new_list[0] == ['']:
            new_list.pop(0) 
        for sublist in new_list:
            if sublist[1] == "To: "+email_input:
                # Combine the relevant elements into one string with "\n" in between
                string_to_insert = (sublist[2:] + [" "])  # Add a space to the end of the list, looks better formatted when all the lists are inserted into the Listbox
                # Insert the string into the listbox
                listbox.insert(tk.END, sublist[0])
                for line in string_to_insert:
                    listbox.insert(tk.END, line)
        listbox.pack()
    # Buttons to Send Email and Button to reach the Mailbox
 
    send_button = tk.Button(main_window, text="Send Mail", command=get_input, bg="#2978b5", fg="#fff", bd=0, padx=10, pady=5)
    send_button.place(relx=0.2, rely=1.0, anchor=tk.S)
    mailbox_button = tk.Button(main_window, text="Mailbox", command=mailbox, bg="#2978b5", fg="#fff", bd=0, padx=10, pady=5)
    mailbox_button.place(relx=0.4, rely=1.0, anchor=tk.S)
    logout_button = tk.Button(main_window, text="Log out", command=log_out, bg="#2978b5", fg="#fff", bd=0, padx=10, pady=5)
    logout_button.place(relx=0.8, rely=1.0, anchor=tk.S)

# Create Global Variable for Login to Use, This variable will be used in functions called later on in the program
email_input = ""
email_entry = ""
password_entry = ""
# Create login function
def login():
    global email_input, email_entry, password_entry
    email_input = email_entry.get()
    password_input = password_entry.get()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_input):
        messagebox.showerror("Login Error", "Invalid email format.")
        return
    with open("userdata.txt", "r") as user_data:
            user_dict = {}
            for line in user_data:
                email, password = line.strip().split(",")
                user_dict[email] = password
            if email_input in user_dict and user_dict[email_input] == password_input:
                    messagebox.showinfo("Login", "Login Successful!")
                    main_window()
                    menu.destroy()
            else:
                messagebox.showerror("Login Error", "Invalid email or password.")
                            
#Creates register function
def register():
    email = email_entry.get()
    password = password_entry.get()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Registration Error", "Invalid email format.")
        return
    with open("userdata.txt", "r") as user_data:
        existing_emails = [line.split(",")[0] for line in user_data.readlines()]
        if email in existing_emails:
            messagebox.showerror("Error", "Email already exists!")
            return
        else:
            with open("userdata.txt","a") as user_data:
                user_data.write(email+","+password+"\n")
                messagebox.showinfo("Register", "Registeration Successful!")
def menu_window():
    #Creates the Initial Menu
    global menu,email_entry,password_entry
    menu = tk.Tk()
    menu.title('Email System(Menu)')
    menu.geometry('300x350')
    menu.configure(bg='#212121')

    # Set the style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background='#212121', foreground='white', font=('Arial', 14, 'bold'))
    style.configure('TEntry', background='#f5f5f5', font=('Arial', 12))
    style.configure('TButton', background='#4caf50', foreground='white', font=('Arial', 12), padding=6)

    # Create the title label
    lbl_title = ttk.Label(menu, text='Email App', style='Title.TLabel')
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
    lbl_title.pack(pady=10)

    # Create the email label and entry
    email_label = ttk.Label(menu, text='Email:')
    email_label.pack(pady=5)
    email_entry = ttk.Entry(menu, width=30)
    email_entry.pack()

    # Create the password label and entry
    password_label = ttk.Label(menu, text='Password:')
    password_label.pack(pady=5)
    password_entry = ttk.Entry(menu, width=30, show='*')
    password_entry.pack()

    # Create the login and register buttons
    frm_buttons = ttk.Frame(menu, padding=(10, 10), style='My.TFrame')
    style.configure('My.TFrame', background='#212121')
    frm_buttons.pack(fill='x')
    btn_login = ttk.Button(frm_buttons, text='Login', command=login, style='TButton')
    btn_login.pack(side='left', padx=5)
    btn_register = ttk.Button(frm_buttons, text='Register', command=register, style='TButton')
    btn_register.pack(side='left')
    menu.mainloop()
menu_window()
