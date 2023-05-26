#!/usr/bin/env python3

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os

os.chdir(r"C:\Users\felix\Desktop\ENS\Cours\L3\BDD\Projet_BDD\Code Projet\final")

from helpers import callback

class CreateMenu(object) :

    def todo():
        showinfo("alerte", "Pas encore implémenté")


    def disconnect():
        fichier.destroy()
        code.identification_window()

    def add_menu(fenetre) :


        menubar = Menu(fenetre)

        fichiers = Menu(menubar, tearoff=0)
        fichiers.add_command(label="Disconnect", command=CreateMenu.todo)
        fichiers.add_separator()
        fichiers.add_command(label="Quitter", command=fenetre.destroy)
        menubar.add_cascade(label="Fichier", menu=fichiers)

        editer = Menu(menubar, tearoff=0)
        editer.add_command(label="Couper", command=CreateMenu.todo)
        editer.add_command(label="Copier", command=CreateMenu.todo)
        editer.add_command(label="Coller", command=CreateMenu.todo)
        menubar.add_cascade(label="Editer", menu=editer)

        help_ = Menu(menubar, tearoff=0)
        help_.add_command(label="A propos", command=lambda : callback("https://moodle.psl.eu/pluginfile.php/398101/mod_resource/content/1/FORA.pdf"))
        menubar.add_cascade(label="Aide", menu=help_)
        fenetre.config(menu=menubar)


if __name__ == "__main__":
    fenetre = Tk()
    fenetre.geometry("1250x700")
    fenetre.title("BDD")

    CreateMenu.add_menu(fenetre)

    fenetre.mainloop()