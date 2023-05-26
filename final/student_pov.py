#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk as ttk2
import psycopg2
import ttkbootstrap as ttk
import os

os.chdir(r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\final")

from config import config
from initialize import AdminButton

from datetime import date



params = config()
conn = psycopg2.connect(**params)
conn.autocommit = True

# get some helper functions
from helpers import *
from menu import CreateMenu


class Student :
    def __init__(self, email, pwd, isAdmin = False):
        """
        A student can search for an internship by adding filters
        They can change their password and see their personnal infos
        The admin can initialize the database
        """

        self.email = email
        self.pwd = pwd
        self.admin = isAdmin
        self.filters = { "country": set(),
                         "city": set(),
                         "lab": set(),
                         "date_start": set(),
                         "date_end": set(),
                         "name": set(),
                         "topic": set(),
                         "mark": [0,10]
                        }
        self.filter_labels = { "country": [None, None, None],
                         "city": [None, None, None],
                         "lab": [None, None, None],
                         "name": [None, None, None],
                         "topic": [None, None, None],
                        }


        self.student_window = ttk.Window(themename = 'darkly')
        self.student_window.title("As a student")
        self.student_window.geometry('400x300+700+300')


        canvas = tk.Canvas(self.student_window, width=400, height=500, relief='raised')
        canvas.pack()

        tk.Label1 = tk.Label(self.student_window, text='What do you wanna do?')
        tk.Label1.config(font=('helvetica', 14))
        canvas.create_window(200, 25, window=tk.Label1)

        def addmark():
            self.student_window.destroy()
            self.addMark()
        buttonAddMarks = design_button("Add Marks", addmark)
        canvas.create_window(150, 80, window=buttonAddMarks)

        def search():
            self.student_window.destroy()
            self.doSearch()

        buttonSearch = design_button("Search", search)
        canvas.create_window(250, 80, window=buttonSearch)


        if isAdmin :

            buttonAdmin = design_button("init", AdminButton)
            canvas.create_window(200, 180, window=buttonAdmin)


        # add the menu
        CreateMenu.add_menu(self.student_window)

        self.student_window.mainloop()

    ## do search
    def doSearch(self, initial_error_text = "") :

        search_window = ttk.Window(themename = 'darkly')
        search_window.title("Search Internship")
        search_window.geometry('700x900+700+0')

        canvas = tk.Canvas(search_window, width=700, height=900, relief='raised')
        canvas.pack()

        # to go to the multitask place
        quitButton(search_window, lambda : Student(self.email, self.pwd, self.admin), canvas)

        addOptions = tk.Label(search_window, text = "Add Filter", font='Helvetica 18 bold')
        canvas.create_window(350, 80, window = addOptions)

        """
        self.filter_tk.Labels
"position": None,
"name": None,
"topic": None,
"period": None,
"mark": None
        """

        # get all infos
        cursor = conn.cursor()
        cursor.execute("SELECT country FROM loc;")
        country = set([elem[0] for elem in cursor.fetchall()])
        cursor.execute("SELECT city FROM loc;")
        city = set(elem[0] for elem in cursor.fetchall())
        cursor.execute("SELECT lab FROM loc;")
        lab = set([elem[0] for elem in cursor.fetchall()])
        cursor.execute("SELECT date_start FROM loc;")
        date_start = set([elem[0] for elem in cursor.fetchall()])
        cursor.execute("SELECT date_end FROM loc;")
        date_end = set([elem[0] for elem in cursor.fetchall()])
        cursor.execute("SELECT fname FROM users WHERE role='researcher';")
        name = set([elem[0] for elem in cursor.fetchall()])
        cursor.execute("SELECT title FROM topics;")
        topic = set([elem[0] for elem in cursor.fetchall()])
        cursor.close()

        # to add a filter
        def add_selection(height, type, recom):
            frame = tk.Frame()
            tk.Label(frame, text = "Add " + type + " : ", font='Helvetica 13 bold').pack(side = tk.LEFT)
            entry1 = tk.Entry(frame)
            entry1.pack(side = tk.LEFT)

            def select_fast(event) :
                elems = listbox.get(0)
                if elems :
                    event.widget.delete(0, tk.END)
                    listbox.select_set(0)
                    event.widget.insert(tk.END, elems)

            # link the event with a recommendation
            def research_helper(event):
                value = event.widget.get()
                if value:
                    names = recommend(value, recom)
                    listbox.delete(0, tk.END)
                    for topic in names:
                        listbox.insert(tk.END, topic)
                else:
                    listbox.delete(0, tk.END)

            def on_return(event):
                add(type, entry1, recom)
                entry1.delete(0, tk.END)

            def on_return_lstbox(event) :
                entry1.delete(0,tk.END)
                entry1.insert(tk.END, listbox.get(listbox.curselection()[0]))
                on_return(event)

            entry1.bind("<KeyRelease>", research_helper)
            entry1.bind("<Return>", on_return)
            entry1.bind("<Tab>", select_fast)

            # the objects and boundings
            listbox = tk.Listbox(frame, height = 3)
            listbox.pack(fill = "x", side = tk.LEFT)
            canvas.create_window(350, height, window = frame)
            listbox.bind("<Return>", on_return_lstbox)

            # print the selected ones

            frameSelected = tk.Frame()
            for i in range(3) :
                self.filter_labels[type][i] = tk.Label(frameSelected, text = "", cursor = "hand2")
                self.filter_labels[type][i].bind("<ButtonRelease-1>", lambda e: remove(type, e.widget))
                self.filter_labels[type][i].pack(fill = "x", side = tk.LEFT)

            canvas.create_window(350, height + 50, window = frameSelected)







        # more helper functions to simlpify
        # Memorise the element and show it to the user
        def add(type, widget, recom) :
            if len(self.filters[type]) < 3 and widget.get() not in self.filters[type] and widget.get() in recom:
                self.filters[type].add(widget.get())
                if not self.filter_labels[type][0].cget("text") :
                    self.filter_labels[type][0].config(text=widget.get())
                elif not self.filter_labels[type][1].cget("text") :
                    self.filter_labels[type][1].config(text=widget.get())
                elif not self.filter_labels[type][2].cget("text") :
                    self.filter_labels[type][2].config(text=widget.get())
                else :
                    self.filter_labels[type][2].config(text=widget.get())
            else :
                if widget.get() in self.filters[type] :
                    error_label.config(text='Already in', fg='red')
                elif widget.get() not in recom:
                    error_label.config(text='Unknown location', fg='red')
                else :
                    error_label.config(text='Too much already selected', fg='red')

        # remove a selected element
        def remove(type, widget) :
            if widget.cget("text") in self.filters[type] :
                print("removed")
                self.filters[type].remove(widget.cget("text"))
                widget. config(text="")


        # now it's simple: juste do the thing
        add_selection(150, "country", country)

        add_selection(260, "name", name)

        add_selection(370, "topic", topic)

        # to do some pointer trickery
        class Pointer(object) :
            def __init__(self, ref = None):
                self.ref = ref

        # date start
        frame = tk.Frame()

        tk.Label(frame, text = "date start (yyyy/mm/dd) :").pack(fill = "x", side = tk.LEFT)
        entry2 = tk.Entry(frame)
        entry2.pack(fill = "x", side = tk.LEFT)
        # because lambda functions of python are dumb and does not support assignations...
        def assign(e):
            out = entry2.get()
            if out == "": return None
            if len(out) == 10:
                if out[4] == out[7] == '/' :
                    try :
                        self.filters["date_start"] = {str(toDate(out))}

                    except:
                        error_label.config(text='wrong format', fg='red')
                else :
                     error_label.config(text='wrong format', fg='red')

        entry2.bind("<KeyRelease>", assign)

        canvas.create_window(350, 500, window = frame)

        # date end
        frame = tk.Frame()

        tk.Label(frame, text = "date end (yyyy/mm/dd) :").pack(fill = "x", side = tk.LEFT)
        entry3 = tk.Entry(frame)
        entry3.pack(fill = "x", side = tk.LEFT)
        def assign2(e):
            out = entry3.get()
            if len(out) == 10:
                if out[4] == out[7] == '/' :
                    try :
                        self.filters["date_end"] = {str(toDate(out))}

                    except:
                        error_label.config(text='wrong format', fg='red')
                else :
                     error_label.config(text='wrong format', fg='red')

        entry3.bind("<KeyRelease>", assign2)

        canvas.create_window(350, 550, window = frame)


        # if you want a good supervisor
        frame = tk.Frame()

        tk.Label(frame, text = "mark :").pack(fill = "x", side = tk.LEFT)
        fmin = tk.Frame(frame)
        tk.Label(fmin, text = "min").pack(fill = "x", side = tk.TOP)
        entry5 = tk.Entry(fmin)
        entry5.pack(fill = "x", side = tk.BOTTOM)
        fmin.pack(fill = "x", side = tk.LEFT)
        fmax = tk.Frame(frame)
        tk.Label(fmax, text = "max").pack(fill = "x", side = tk.TOP)
        entry4 = tk.Entry(fmax)
        entry4.pack(fill = "x", side = tk.BOTTOM)
        fmax.pack(fill = "x", side = tk.RIGHT)

        def assign(e,i):
            out = e.widget.get()
            if not out :
                self.filters["mark"][i] = 10 - 10 * i
                error_label.config(text='', fg='red')
                return
            try :
                error_label.config(text='')

                n = float(out)
                if n>=0 and n <= 10 :
                    self.filters["mark"][i] = n
                else :
                    raise Exception
            except :
                error_label.config(text='wrong format', fg='red')

        entry5.bind("<KeyRelease>", lambda e: assign(e,0))
        entry4.bind("<KeyRelease>", lambda e: assign(e,1))


        canvas.create_window(350, 600, window = frame)



        # now the result !!!

        def get_result():
            search_window.destroy()
            self.submit()
            self.print_submit(0)


        submitButton = design_button("Submit", get_result)
        canvas.create_window(350, 800, window=submitButton)


        # and some error handling
        error_label = tk.Label(search_window, text="", font=('helvetica', 18))
        error_label.config(text=initial_error_text, fg='red')
        canvas.create_window(350, 870, window=error_label)


        search_window.mainloop()

    def submit(self):

        def fold_left(f,init,iter) :
            rez = init
            for elem in iter:
                rez = f(rez, elem)
            return rez

        cursor = conn.cursor()

        self.has_elems_before = False

        query = """
            SELECT DISTINCT I.title, I.descr, I.r_id, I.url
            FROM internships I JOIN loc L ON
            I.r_id = L.r_id
            JOIN i_tops IT ON  IT.i_id = I.int_id
            JOIN topics T ON T.topic_id = IT.t_id
            WHERE '1' != '1'"""

        # we add the country things
        def f_l_type_loc(type):
            a = ""
            pref = "L." + type
            if type == "topic":
                pref = "T.title"
            if self.filters[type] :
                tmp = self.filters[type].pop()

                if self.has_elems_before :
                    a = " AND "
                else :
                    a = " OR "
                    self.has_elems_before = True

                op = ">=" if type == "date_start" else (" is NONE or L.date_end <=" if type == "date_end" else "=")

                # vilaine injection sql en vue :(
                a += " ( " + fold_left(lambda acc2,new2: (acc2 + f" OR {pref}{op}'{new2}' "), " " + f" {pref}{op}'{tmp}' " + " ", self.filters[type]) + " ) "
                self.filters[type].add(tmp)
            return a

        # filter country
        query += f_l_type_loc("country")
        # filter city
        query += f_l_type_loc("city")
        # filter laboratory
        query += f_l_type_loc("lab")
        # filter date_start... bon ok je triche un peu c'est pas vraiment ce qu'on veut mais flemme d'implémenter le trucs pour internships aussi
        query += f_l_type_loc("date_start")
        # filter date_end
        query += f_l_type_loc("date_end")


        name_id = set()
        for nom in self.filters["name"] :
            cursor.execute("SELECT user_id FROM users WHERE fname = %s OR lname = %s ;", (nom,nom))
            name_id.update(elem[0] for elem in cursor.fetchall())

        self.filters["r_id"] = name_id

        query += f_l_type_loc("r_id")


        # now the last two (forced)
        query += f_l_type_loc("topic")

        # the marks limits
        cursor.execute("SELECT r_id FROM marks GROUP BY r_id HAVING AVG(mark) BETWEEN %s AND %s;", (self.filters["mark"][0], self.filters["mark"][1]))
        mark_id = set(elem[0] for elem in cursor.fetchall())

        # recyclage de r_id, exécuté linéairement donc pas grave
        self.filters["r_id"] = mark_id
        query += f_l_type_loc("r_id")


        # Le moment fatidique...
        cursor.execute(query)
        self.rez = list(cursor.fetchall())

        cursor.close()

        # restart from the very begining if you wanna do it again
        self.filters = { "country": set(),
                         "city": set(),
                         "lab": set(),
                         "date_start": set(),
                         "date_end": set(),
                         "name": set(),
                         "topic": set(),
                         "mark": [0,10]
                        }
        self.filter_labels = { "country": [None, None, None],
                         "city": [None, None, None],
                         "lab": [None, None, None],
                         "name": [None, None, None],
                         "topic": [None, None, None],
                        }


    def print_submit(self, i):
        if not self.rez :
            self.doSearch("No result found")
            return 1

        current_print = self.rez[i%len(self.rez)]

        got_window = ttk.Window(themename = 'darkly')
        got_window.geometry('1200x700+300+200')

        canvas = tk.Canvas(got_window, width=1200, height=700, relief='raised')
        canvas.pack()

        # to go to the multitask place
        def temp_quitt():
            self.rez = None
            self.doSearch()
        quitButton(got_window, temp_quitt, canvas)

        frame = tk.Frame()
        tk.Label(frame, text = "title : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        tk.Label(frame, text = current_print[0]).pack(fill = 'x', side = 'left')
        canvas.create_window(600, 100, window=frame)



        cursor = conn.cursor()
        cursor.execute("SELECT fname, lname, email FROM users WHERE user_id = %s", (current_print[2],))
        fname, lname, email = cursor.fetchone()
        # define the title
        got_window.title(f"Internship from {fname} {lname}")

        frame = tk.Frame()
        tk.Label(frame, text = "from : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        label = tk.Label(frame, text = lname.upper() if lname else "" + " " + fname.capitalize() + "  " + email)
        label.pack(fill = 'x', side = 'left')
        canvas.create_window(600, 150, window=frame)


        frame = tk.Frame()
        tk.Label(frame, text = "description : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        text_display = tk.scrolledtext.ScrolledText(frame, height=5, width = 40, wrap=tk.WORD)
        text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, current_print[1])
        text_display.config(state = tk.DISABLED)
        text_display.pack(fill = 'x', side = 'left')
        canvas.create_window(600, 250, window=frame)



        frame = tk.Frame()
        tk.Label(frame, text = "website : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        label = tk.Label(frame, text = current_print[3], cursor="hand2")
        label.pack(fill = 'x', side = 'left')
        canvas.create_window(600, 400, window=frame)
        label.bind("<Button-1>", lambda e: callback(current_print[3]))

        # print where we are on the reading of internships
        frame = tk.Frame()
        entry = tk.Entry(frame, cursor="pirate", font = 'Helvetica 8')
        entry.delete(0,tk.END)
        entry.insert(0,f"{i%len(self.rez)+1}")
        entry.pack(fill = "x", side = tk.LEFT)
        tk.Label(frame, text = f"/ {len(self.rez)}", font='Helvetica 8').pack(fill = 'x', side = 'left')
        canvas.create_window(1100, 650, window=frame)

        def updateSeeing(event):
            try :
                n = int(entry.get())
                assert n > 0 and n <= len(self.rez)
                got_window.destroy()
                self.print_submit(n-1)
            except:
                entry.delete(0,tk.END)
                entry.insert(0,f"{i%len(self.rez)+1}")

        entry.bind("<Return>", updateSeeing)

        # buttons to move between things
        def change_one(dir):
            got_window.destroy()
            self.print_submit(i+dir)
        frame = tk.Frame()
        design_button("Next", lambda : change_one(1), frame).pack(fill = "x")
        canvas.create_window(750, 500, window = frame)

        frame = tk.Frame()
        design_button("Previous", lambda : change_one(-1), frame).pack(fill = "x")
        canvas.create_window(450, 500, window = frame)



        got_window.mainloop()









    ## add mark
    def addMark(self) :

        add_mark_window = ttk.Window(themename = 'darkly')
        add_mark_window.title("As a student")
        add_mark_window.geometry('400x500+700+300')

        canvas = tk.Canvas(add_mark_window, width=400, height=500, relief='raised')
        canvas.pack()

        # to go to the multitask place
        quitButton(add_mark_window, lambda : Student(self.email, self.pwd, self.admin), canvas)

        # to choose the researcher to give the mark

        # get all names / emails (flemme de rename)
        cursor = conn.cursor()

        cursor.execute("SELECT fname FROM users WHERE role=%s;", ("researcher",))
        emails = cursor.fetchall()
        cursor.close()
        assert emails, "No researchers !"
        emails = {email[0] for email in emails}

        search_label = tk.Label(add_mark_window, text='Who do you wanna mark ?')
        search_label.config(font=('helvetica', 14))
        canvas.create_window(200, 50, window=search_label)

        entry = tk.Entry(add_mark_window)
        canvas.create_window(200, 80, window=entry)



        # to update the selection when clicked
        def on_select(event):
            # get selected item from auto-complete listbox
            selection = event.widget.curselection()
            if selection:
                value = event.widget.get(selection[0])
                add_mark_window.destroy()
                self.print_profile(value, lambda: self.addMark())


        def give_the_name(event) :
            research_name = event.widget.get()
            if research_name not in emails:
                error_label.config(text='Unknown email', fg='red')
                return
            add_mark_window.destroy()
            self.print_profile(research_name, lambda: self.addMark())
        def select_fast(event) :
            elems = listbox.get(0)
            if elems :
                entry.delete(0, tk.END)
                listbox.select_set(0)
                entry.insert(tk.END, elems)


        # link the event with a recommendation
        def research_helper(event):
            value = event.widget.get()
            if value:
                names = recommend(value, emails)
                listbox.delete(0, tk.END)
                for topic in names:
                    listbox.insert(tk.END, topic)
            else:
                listbox.delete(0, tk.END)


        # the objects and boundings
        listbox = tk.Listbox(add_mark_window, height = 3)
        canvas.create_window(200, 150, window=listbox)

        entry.bind("<KeyRelease>", research_helper)
        entry.bind("<Return>", give_the_name)
        entry.bind("<Tab>", select_fast)
        listbox.bind("<ButtonRelease-1>", on_select)
        listbox.bind("<Return>", on_select)


        error_label = tk.Label(add_mark_window, text='', font=('helvetica', 10))
        canvas.create_window(200, 220, window=error_label)


        add_mark_window.mainloop()

    ## print profile
    def print_profile(self, name, reload) :
        user_window = ttk.Window(themename = 'darkly')
        user_window.title(f"{name} profile")
        user_window.geometry('400x500+700+300')

        canvas = tk.Canvas(user_window, width=400, height=500, relief='raised')
        canvas.pack()

        quitButton(user_window, reload, canvas)

        cursor = conn.cursor()

        # get the user id
        cursor.execute("SELECT user_id, email FROM users WHERE fname=%s;", (name,))
        ids = cursor.fetchall()
        assert ids, f"no id for {name}"

        # get the user location
        cursor.execute(f"SELECT country, city, lab, date_start, date_end FROM loc WHERE r_id=%s AND {toDate(date.today().strftime('%Y/%m/%d'))} >= date_start AND (date_end IS NULL OR date_end >= {toDate(date.today().strftime('%Y/%m/%d'))});", (f"{ids[0][0]}",))
        infos = cursor.fetchall()


        # user id
        cursor.execute("SELECT user_id FROM users WHERE email=%s;", (self.email,))
        iduser = cursor.fetchall()

        # get the researcher mark
        cursor.execute(f"SELECT AVG(mark) FROM marks WHERE r_id=%s;", (ids[0][0],))
        mark = cursor.fetchall()


        # flemme de réécrire le code pour faire qu'une query
        cursor.execute(f"SELECT mark FROM marks WHERE r_id=%s AND s_id = %s;", (ids[0][0], iduser[0][0]))
        personnal_mark = cursor.fetchone()
        cursor.close()

        assert infos, "pas d'info"
        infos = list(infos[0])


        # make a pseudo dictionary
        arg = ["country", "city", "lab", "date_start", "date_end"]

        # print infos
        for i in range(len(infos)):

            frame = tk.Frame()
            tk.Label(frame, text = arg[i] + " : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
            if arg[i].startswith("date") :
                infos[i] = getDate(infos[i])

            tk.Label(frame, text = infos[i] if infos[i] else "??").pack(fill = 'x', side = 'left')
            canvas.create_window(200, 80 + 30*i, window=frame)


        frame = tk.Frame()
        tk.Label(frame, text = "email : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        label = tk.Label(frame, text = ids[0][1], cursor="hand2")
        label.pack(fill = 'x', side = 'left')
        canvas.create_window(200, 250, window=frame)
        label.bind("<Button-1>", lambda e: callback(ids[0][1]))


        # print mark
        frame = tk.Frame()
        tk.Label(frame, text = "Average mark : ", font='Helvetica 13 bold').pack(fill = 'x', side = 'left')
        currmark = tk.Label(frame, text = str(round(float(mark[0][0]), 2)) if mark else "??")
        currmark.pack(fill = 'x', side = 'left')
        canvas.create_window(200, 280, window=frame)


        entry1 = tk.Entry(user_window)
        entry1.delete(0,tk.END)
        entry1.insert(0,f'{personnal_mark[0] if personnal_mark else ""}')
        canvas.create_window(200, 350, window=entry1)

        def updateMarks(event):
            try :
                val = int(entry1.get())
                if val < 0 or val >10 :
                    raise Exception("nope")

                cursor = conn.cursor()


                cursor.execute('SELECT s_id FROM marks WHERE r_id = %s AND s_id = %s;', (ids[0][0], iduser[0][0]))

                cursor.execute('UPDATE marks SET mark = %s WHERE r_id = %s AND s_id = %s;', (val, ids[0][0], iduser[0][0]))

                cursor.execute('SELECT AVG(mark) FROM marks WHERE r_id = %s;', (ids[0][0],))
                new_mark = cursor.fetchall()
                print(new_mark)

                cursor.close()
                currmark.config(text = str(round(float(new_mark[0][0]), 2)))

            except :
                error_label.config(text='Invalid format, write an integer between 0 and 10', fg='red')


        entry1.bind("<Return>", updateMarks)


        error_label = tk.Label(user_window, text='', font=('helvetica', 10))
        canvas.create_window(200, 400, window=error_label)






if __name__ == "__main__" :
    Student("admin@admin.fr", "admin", True)




