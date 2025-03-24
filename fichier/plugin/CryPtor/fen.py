#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import fichier.plugin.CryPtor.main as main1
import fichier.plugin.CryPtor.fct as fct
import fichier.var as var
import fichier.design as design
import random
import os






def fen():
    fenetre2 = Toplevel()

    def stop():
        fenetre2.destroy()
    def crypt():
        text = ent0.get()
        cle = ent1.get()
        print(text + " * " + cle)
        Cryptage(text, cle)
    def Cryptage(text, cle):
        result = fct.crypt(text, cle)
        ent2.delete(0,END)
        ent2.insert(0,result)

    def dict(nbr):

        liste = ""
        path = os.getcwd()

        with open(path+"\\fichier\\plugin\\Cryptor\\"+"dict.txt", "r", encoding='utf-8') as file:
            allText = file.read()
            words = list(map(str, allText.split()))
            i=1
            while i <= int(nbr):
                if i == nbr:
                    liste = liste + random.choice(words)
                else:
                    liste = liste + random.choice(words) + "_"
                i+=1
            # print random string
            print(liste)
        ent0.delete(0, END)
        ent0.insert(0, liste)

    ###################################################################################################################
    ###### Fenetre principale																					 ######
    ###################################################################################################################
    # Créer une nouvelle fenêtre

    fenetre2.title("Cryptor - version "+main1.version)
    fenetre2.geometry("400x400")
    fenetre2.overrideredirect(1)

    frame_haut = Frame(master=fenetre2, bg=var.bg_frame_haut, height=50, padx=5, pady=5)
    frame_haut.pack(fill=X)
    frame_mid = Frame(master=fenetre2, bg=var.bg_frame_mid, height=300,padx=5, pady=5)
    frame_mid.pack(fill=X)
    frame_bot = Frame(master=fenetre2, bg=var.bg_frame_haut, height=50, padx=5, pady=5)
    frame_bot.pack(fill=X)



    ########################################
    ## Titre
    Label(master=frame_haut, text="Cryptor, génération de mots de passes forts", bg="#FFFFFF").pack(fill=X)
    Label(master=frame_haut, text="version "+main1.version, bg="#FFFFFF").pack(fill=X)
    ####################################################################################################################
    # Caméras
    texte1 = Label(master=frame_mid, text="Texte", bg="#FFFFFF", width=20)
    texte1.grid(row=0, column=0, padx=5, pady=5, columnspan=1)
    ent0 = Entry(frame_mid, text="", width=37)
    ent0.insert(0, '0')
    ent0.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    cle = Label(master=frame_mid, text="Clé (chiffres)", bg="#FFFFFF", width=20)
    cle.grid(row=1, column=0, padx=5, pady=5, columnspan=1)
    ent1 = Entry(frame_mid, text="")
    ent1.insert(0, '0')
    ent1.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    result = Label(master=frame_mid, text="Résultat", bg="#FFFFFF", width=20)
    result.grid(row=2, column=0, padx=5, pady=5, columnspan=1)
    ent2 = Entry(frame_mid, text="", width=35)
    ent2.insert(0, '0')
    ent2.grid(row=2, column=1, padx=5, pady=5, sticky='w')


    Button(frame_bot, text='Annuler', padx=10, command=stop).pack(side=LEFT, padx=5, pady=5)
    Button(frame_bot, text='Valider', padx=10, command=crypt).pack(side=LEFT, padx=5, pady=5)
    dict(3)

    # ______________________________________________________________
    # Créer un menu
    # ______________________________________________________________
    design.center_window(fenetre2)
    fenetre2.mainloop()

