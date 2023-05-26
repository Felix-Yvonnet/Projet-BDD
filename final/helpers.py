#!/usr/bin/env python3

"""

A file only to write once every usefull helper functions i will use in most files

"""

import tkinter as tk
import difflib
import webbrowser
import os
from datetime import date, timedelta, datetime
diff_time_day = 14

# Some helper functions
def design_button(text, command, master = None) :
    if master is not None :
        return tk.Button(master, text=text, command=command, bg='brown', fg='white', font=('helvetica', 9, 'bold'))

    return tk.Button(text=text, command=command, bg='brown', fg='white', font=('helvetica', 9, 'bold'))


def getDate(dateint):
    return f"{dateint // 10000}/{(dateint %10000) // 100}/{dateint % 100 }" # yyyy-mm-dd

def toDate(datestr):
    date = datestr.split("/")
    return int(date[0])*10000 + int(date[1]) * 100 + int(date[2])

def callback(url):
    webbrowser.open_new(url)




def quitButton(origin, dest, canvas):
    def quit():
        origin.destroy()
        dest()
    buttonQuit = design_button("Go Back", quit)
    canvas.create_window(50, 20, window=buttonQuit)




def recommend(word, possible_words):
    # find the closest match using difflib
    word = word.lower()
    lpos = {p.lower(): p for p in possible_words}
    match = difflib.get_close_matches(word, lpos.keys(), n=3, cutoff=0.45)

    # return up to 3 recommendations
    return [lpos[mat] for mat in match[:3]]


# to handle les cookies d'inscription
def add_cookie(email, pwd):
    with open(f"./Cookie/{email}", "w") as file :
        file.write(f"encrypted,{email},{pwd},{date.today()}")


def get_cookie():
    if not os.path.exists("Cookie/"):
        os.makedirs("Cookie")
    for truc in os.listdir("./Cookie/") :
        path = os.path.join("./Cookie/", truc)
        with open(path) as fichier:
            line = fichier.readlines()[0]
            _, name, pwd, last_time = line.split(",")
            if date.fromisoformat(last_time) + timedelta(days=diff_time_day) > date.today():
                return name, pwd
            else :
                path = os.path.join("./Documents/", email)
                os.remove(path)
    return "",""







