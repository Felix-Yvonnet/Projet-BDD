#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
import psycopg2
import ttkbootstrap as ttk
from datetime import date
import os
import shutil

from os import chdir
chdir(r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\final")

from config import config

params = config()
conn = psycopg2.connect(**params)
conn.autocommit = True

# get some helper functions
from helpers import *
from menu import CreateMenu


class Researcher:
    def __init__(self, email = "", password = "") :
        self.mail = email
        self.pwd = password
        self.create_widgets()


    def add_intern(self):

        r_window = ttk.Window(themename = 'darkly')
        r_window.title("Submit internship")
        r_window.geometry('600x700+600+200')

        canvas = tk.Canvas(r_window, width=600, height=700, relief='raised')
        canvas.pack()


        quitButton(r_window, self.create_widgets, canvas)


        frame = tk.Frame()
        tk.Label(frame, text = "title : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        entry_title = tk.Entry(frame)
        entry_title.pack(fill = 'x', side = 'left')
        canvas.create_window(300, 100, window=frame)



        frame = tk.Frame()
        tk.Label(frame, text = "description : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        entry_desc = tk.scrolledtext.ScrolledText(frame, height=5, width = 30, wrap=tk.WORD)
        entry_desc.pack(fill = 'x', side = 'left')
        canvas.create_window(300, 200, window=frame)



        frame = tk.Frame()
        tk.Label(frame, text = "website : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        entry_web = tk.Entry(frame)
        entry_web.pack(fill = 'x', side = 'left')
        canvas.create_window(300, 350, window=frame)


        frame = tk.Frame()
        tk.Label(frame, text = "related topics : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        entry_topics = tk.Entry(frame)
        entry_topics.pack(fill = 'x', side = 'left')
        listbox = tk.Listbox(frame, height = 3)
        listbox.pack(fill = "x", side = tk.RIGHT)
        canvas.create_window(300, 450, window=frame)



        # to update the selection when clicked
        def on_select(event):
            # get selected item from auto-complete listbox
            selection = event.widget.curselection()
            if selection:
                value = event.widget.get(selection[0])
                entry_topics.delete(0, tk.END)
                entry_topics.insert(tk.END, value)

        cursor = conn.cursor()
        cursor.execute("SELECT title, topic_id FROM topics")
        topics = dict(cursor.fetchall())
        cursor.close()

        def select_fast(event) :
            elems = listbox.get(0)
            if elems :
                entry_topics.delete(0, tk.END)
                listbox.select_set(0)
                entry_topics.insert(tk.END, elems)

        # link the event with a recommendation
        def research_helper(event):
            value = event.widget.get()
            if value:
                names = recommend(value,topics.keys())
                listbox.delete(0, tk.END)
                for topic in names:
                    listbox.insert(tk.END, topic)
            else:
                listbox.delete(0, tk.END)


        # the boundings
        entry_topics.bind("<KeyRelease>", research_helper)
        entry_topics.bind("<Tab>", select_fast)
        listbox.bind("<ButtonRelease-1>", on_select)
        listbox.bind("<Return>", on_select)

        # to commit the result
        def submit() :
            title = entry_title.get()
            web = entry_web.get()
            descr = entry_desc.get("1.0", tk.END)
            topic = entry_topics.get()

            # Some verifications
            if not title:
                error_label.config(text='please complete a title', fg='red')
                return
            if not descr :
                error_label.config(text='please give a description', fg='red')
                return
            if not web :
                error_label.config(text='please give a website to complete your informations', fg='red')
                return
            if not topic :
                error_label.config(text='please give a topic to complete your informations', fg='red')
                return
            if not topic in topics :
                error_label.config(text='the given topic is not among the one present to add one ask an  admin', fg='red')
                return

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM internships WHERE title=%s", (title,))
            if cursor.fetchall() :
                error_label.config(text='this title is already used for an internship', fg='red')
                return

            cursor.execute("SELECT user_id FROM users WHERE email=%s", (self.mail,))
            u_id = cursor.fetchone()

            cursor.execute("INSERT INTO internships(title, descr, r_id, url) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING ", (title, descr, u_id, web))

            # Title unique key
            cursor.execute("SELECT int_id FROM internships WHERE title = %s", (title,))
            rez = cursor.fetchone()

            cursor.execute("INSERT INTO i_tops(i_id, t_id) VALUES(%s, %s) ON CONFLICT DO NOTHING", (rez, topics[topic]))

            cursor.close()

            error_label.config(text="OK, it's been added", fg='green')
            entry_title.delete(0, tk.END)
            entry_web.delete(0, tk.END)
            entry_desc.delete("1.0", tk.END)
            entry_topics.delete(0, tk.END)


        frame = tk.Frame()
        design_button("Submit", submit, frame).pack(fill = "x")
        canvas.create_window(300, 600, window = frame)



        def deposit_file():
            file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf *.png")], initialdir=r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\Documents")
            if file_path:
                # Create a folder named "Documents" if it doesn't exist
                if not os.path.exists("Documents"):
                    os.makedirs("Documents")

                # Copy the file to the "Documents" folder
                file_name = os.path.basename(file_path)
                destination = os.path.join("Documents", file_name)
                shutil.copyfile(file_path, destination)


        frame = tk.Frame()
        design_button("Add documents", deposit_file, frame).pack(fill = "x")
        canvas.create_window(300, 500, window = frame)



        error_label = tk.Label(r_window, text="", font=('helvetica', 12))
        error_label.config(text="", fg='red')
        canvas.create_window(300, 650, window=error_label)

        r_window.mainloop()












    def create_widgets(self) :


        """
        Create the pov of a researcher
        Researcher can offer a new internship
        They can actualize their profile

        """
        root = ttk.Window(themename = 'darkly')
        root.title("Researcher Options")

        root.geometry('400x500+700+300')

        canvas = tk.Canvas(root, width=400, height=500, relief='raised')
        canvas.pack()

        CreateMenu.add_menu(root)



        # to go internshipper
        def add_internshipo():
            root.destroy()
            self.add_intern()

        frame = tk.Frame()
        design_button("Add internship", add_internshipo, frame).pack(fill = "x")
        canvas.create_window(150, 150, window = frame)



        # to go change infotter
        def changeinfo():
            root.destroy()
            self.change_info()

        frame = tk.Frame()
        design_button("Change Infos", changeinfo, frame).pack(fill = "x")
        canvas.create_window(250, 350, window = frame)

        root.mainloop()



    def change_info(self):
        search_window = ttk.Window(themename = 'darkly')
        search_window.title("Search Internship")
        search_window.geometry('500x600+700+300')

        canvas = tk.Canvas(search_window, width=500, height=600, relief='raised')
        canvas.pack()

        quitButton(search_window, self.create_widgets, canvas)

        frame = tk.Frame()
        tk.Label(frame, text = "email", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry = tk.Entry(frame, font = 'Helvetica 12')
        entry.delete(0,tk.END)
        entry.insert(0,f"{self.mail}")
        entry.pack(fill = "x", side = tk.LEFT)
        canvas.create_window(250, 100, window=frame)

        def new_email(event):
            value = event.widget.get()
            if value:
                if not is_valid_email(value) :
                    error_label.config(text='Email not valid', fg='red')
                else :
                    cursor = conn.cursor()
                    cursor.execute('UPDATE users SET email = %s WHERE email = %s;', (value, self.mail))
                    cursor.close()
                    self.mail = value
                    error_label.config(text=f'Your email is now: {self.mail}', fg='green')
        entry.bind("<Return>", new_email)



        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email=%s", (self.mail,))
        u_id = cursor.fetchone()
        print(u_id)

        cursor.execute("SELECT country, city, date_start, date_end, lab FROM loc WHERE r_id = %s", (u_id,))
        loc = cursor.fetchone()
        cursor.close()
        frame = tk.Frame()
        tk.Label(frame, text = "localisation :", font='Helvetica 12').pack(fill = 'x', side = 'left')
        f2 = tk.Frame(frame)

        f3= tk.Frame(f2)
        tk.Label(f3, text = "country:", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry_country = tk.Entry(f3, font = 'Helvetica 12')
        entry_country.delete(0,tk.END)
        entry_country.insert(0,f"{loc[0]}")
        entry_country.pack(fill = "x", side = tk.RIGHT)
        f3.pack(side = tk.TOP)

        f3= tk.Frame(f2)
        tk.Label(f3, text = "city:", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry_city = tk.Entry(f3, font = 'Helvetica 12')
        entry_city.delete(0,tk.END)
        entry_city.insert(0,f"{loc[1]}")
        entry_city.pack(fill = "x", side = tk.RIGHT)
        f3.pack(side = tk.TOP)

        f3= tk.Frame(f2)
        tk.Label(f3, text = "lab:", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry_lab = tk.Entry(f3, font = 'Helvetica 12')
        entry_lab.delete(0,tk.END)
        entry_lab.insert(0,f"{loc[4]}")
        entry_lab.pack(fill = "x", side = tk.RIGHT)
        f3.pack(side = tk.TOP)

        f3= tk.Frame(f2)

        f4 = tk.Frame(f3)
        tk.Label(f4, text = "From:", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry_time1 = tk.Entry(f4, font = 'Helvetica 12')
        entry_time1.delete(0,tk.END)
        entry_time1.insert(0, getDate(loc[2]) if loc[2] else "")
        entry_time1.pack(fill = "x", side = tk.RIGHT)
        f4.pack(side = tk.TOP)


        f4 = tk.Frame(f3)
        tk.Label(f4, text = "Until:", font='Helvetica 12').pack(fill = 'x', side = 'left')
        entry_time2 = tk.Entry(f4, font = 'Helvetica 12')
        entry_time2.delete(0,tk.END)
        entry_time2.insert(0,getDate(loc[3]) if loc[3] else "")
        entry_time2.pack(fill = "x", side = tk.RIGHT)
        f4.pack(side = tk.BOTTOM)
        f3.pack(side = tk.BOTTOM)

        f2.pack(side = tk.RIGHT)

        canvas.create_window(250, 350, window = frame)


        def submit():
            country = entry_country.get()
            city = entry_city.get()
            lab = entry_lab.get()
            start = toDate(entry_time1.get()) if entry_time2.get() else None
            end = toDate(entry_time2.get()) if entry_time2.get() else None
            cursor = conn.cursor()

            if country :
                if city :
                    if lab :
                        if start :
                            if end or end is None:
                                cursor.execute('UPDATE loc SET country = %s, city = %s, lab = %s, date_start = %s, date_end = %s WHERE r_id = %s;', (country, city, lab, start, end, u_id))
                                error_label.config(text='info updated', fg='green')
                            else :
                                error_label.config(text='wrong type of date for end', fg='red')
                        else :
                            if end or end is None:
                                cursor.execute('UPDATE loc SET country = %s, city = %s, lab = %s, date_start = %s, date_end = %s WHERE r_id = %s;', (country, city, lab, toDate(date.today().strftime('%Y/%m/%d')), end, u_id))
                                error_label.config(text='info updated', fg='green')
                            else :
                                error_label.config(text='wrong type of date for end', fg='red')
                    else :
                        error_label.config(text='lab name required', fg='red')
                else :
                    error_label.config(text='city name required', fg='red')
            else :
                error_label.config(text='country name required', fg='red')



            cursor.close()

        frame = tk.Frame()
        design_button("submit", submit, frame).pack(fill = "x")
        canvas.create_window(250, 500, window = frame)



        error_label = tk.Label(search_window, text='', font=('helvetica', 10))
        canvas.create_window(250, 550, window=error_label)

        search_window.mainloop()






if __name__ == "__main__" :
    Researcher("pasmoi@gmail.com", "toujourspasmoi")
