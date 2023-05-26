#!/usr/bin/env python3

from tkinter import *
import psycopg2
import ttkbootstrap as ttk
import re

from os import chdir
chdir(r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\final")

from config import config

from student_pov import Student
from researcher_pov import Researcher

params = config()
conn = psycopg2.connect(**params)
conn.autocommit = True


# get some helper functions
from helpers import *

# Create tkinter window for user identification
def identification_window():
    """
    Build the first seen window
    The user should be able to connect using a unique id / password
    The user can also create a new account
    """
    root = ttk.Window(themename = 'darkly')
    root.geometry('400x400+700+300')
    root.title("Register")

    canvas = Canvas(root, width=400, height=500, relief='raised')
    canvas.pack()

    # title
    label1 = Label(root, text='Login to access the system')
    label1.config(font=('helvetica', 14))
    canvas.create_window(200, 25, window=label1)

    # I love cookie ☺
    cook_mail, cook_pwd = get_cookie()

    # ident
    label2 = Label(root, text='Email:')
    label2.config(font=('helvetica', 10))
    canvas.create_window(200, 80, window=label2)

    # get ident
    entry1 = Entry(root)
    if cook_mail : entry1.insert(tk.END, cook_mail)
    canvas.create_window(200, 110, window=entry1)

    # pwd
    label3 = Label(root, text='Password:')
    label3.config(font=('helvetica', 10))
    canvas.create_window(200, 140, window=label3)

    entry2 = Entry(root, show='*')
    if cook_pwd : entry2.insert(tk.END, cook_pwd)
    canvas.create_window(200, 170, window=entry2)


    # user type

    label4 = Label(root, text='User Type:')
    label4.config(font=('helvetica', 10))
    canvas.create_window(200, 200, window=label4)

    user_types = ["student", "researcher"]
    combo_user_type = ttk.Combobox(root, values=user_types)
    canvas.create_window(200, 230, window=combo_user_type)

    # use the written info
    def login():
        email = entry1.get()
        password = entry2.get()
        user_type = combo_user_type.get()

        cursor = conn.cursor()

        # Use parameterized SQL queries to avoid SQL injections (it's what they said... not sure it's that secure)
        cursor.execute('SELECT role, user_id FROM users WHERE email=%s AND password=%s;', (email, password))
        role, id = cursor.fetchone()
        cursor.close()
        print(role)

        if role :
            print(role)
            add_cookie(email, password)
            if role == 'student' :
                print("ok")
                root.destroy()
                Student(email, password, email == "admin@admin.admin")
            elif role == 'researcher':
                root.destroy()
                Researcher(email, password)
        else:
            error_label.config(text='Invalid email or password', fg='red')

    # define button to sign in
    button1 = design_button("Login", login)
    canvas.create_window(250, 270, window=button1)
    entry1.bind("<Return>", lambda _:login())
    entry2.bind("<Return>", lambda _:login())


    # logic to sign up
    def sign_up():

        email = entry1.get()
        password = entry2.get()
        type = combo_user_type.get()

        cursor = conn.cursor()

        cursor.execute('SELECT role FROM users WHERE email=%s;', (email,))
        role = cursor.fetchone()

        if role :
            error_label.config(text=f'User already exist as {role[0]}', fg='red')

        else :
            if not is_valid_email(email) or (type != "researcher" and not email.endswith('.ens-paris-saclay.fr')) :
                error_label.config(text='Invalid email, please enter your ens address', fg='red')
            else :
                if len(password) < 8 :
                    error_label.config(text='your password is too weak, it must be at least 8 characters long', fg='red')
                else :
                    if not type :
                        error_label.config(text='please complete your role', fg='red')
                    else :
                        cursor.execute('INSERT INTO users(email, password, role) VALUES(%s, %s, %s);', (email, password, type))

                        cursor.close()
                        root.destroy()
                        Student(email, password)






    button_new_account = Button(text='Sign Up', command=sign_up, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
    canvas.create_window(150, 270, window=button_new_account)




    error_label = Label(root, text='', font=('helvetica', 10))
    canvas.create_window(200, 320, window=error_label)

    root.mainloop()





if __name__ == '__main__':
    try : identification_window()
    finally : conn.close()
