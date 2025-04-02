#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from fichier import design, var, fct_ip, fct_ping, param_gene, Thread_aj_ip, fct_main, param_db_quit, fct_suivi, fct_graph, lic
import gettext
import os
import psutil
import threading
from tkinter import *
import tkinter as tk
from tkinter import ttk
import math
import webbrowser
from tkinter.messagebox import *
from PIL import ImageTk, Image

def queu():
    while True:
        #time.sleep(.01)
        try:
            try:
                f = var.q.get()
                f()
                if f is None:
                    break
            except Exception as inst:
                design.logs("queu-" + str(inst))
                pass
        except TclError as inst:
            design.logs("queu-" + str(inst))


global app_instance
app_instance = None
def quitter():
    os._exit(0)

class main:

    def __init__(self, fenetre):
        global app_instance
        var.app_instance = self
        self.fenetre = fenetre
        self.fenetre.title("PyngOuin")
        self.fenetre.geometry("910x600")
        self.fenetre.minsize(width=910, height=600)
        fct_main.creerDossier("bd")
        fct_main.creerDossier("fichier")
        fct_main.creerDossier("fichier/plugin")
        self.lireParam()
        var.nom_site = param_gene.nom_site()
        ip_pc = fct_ip.recup_ip()
        self.get_lang()
        self.plug()
        self.check_popup1 = IntVar()
        self.check_mail1 = IntVar()
        self.check_recap1 = IntVar()
        self.check_lat1 = IntVar()
        self.check_port1 = IntVar()
        self.check_telegram1 = IntVar()
        self.check_db1 = IntVar()
        lic.verify_license()
        try:
            self.maj()
        except Exception as e:
            design.logs("MAJ - " + str(e))
            pass
        threading.Thread(target=queu, args=()).start()
        # threading.Thread(target=threado, args=()).start()
        ###################################################################################################################
        ###### Définition des frames																				 ######
        ###################################################################################################################
        self.frame_haut = Frame(master=self.fenetre, height=50, bg=var.bg_frame_haut, padx=5, pady=5)
        self.frame_haut.pack(fill=X)

        self.frame_main = Frame(master=self.fenetre, bg=var.bg_frame_mid, padx=5, pady=5)
        self.frame_main.pack(fill=BOTH, expand=True)

        self.frame_bas = Frame(master=self.fenetre, width=25, height=25, bg=var.bg_frame_haut, padx=5, pady=5)
        self.frame_bas.pack(fill=X)

        ###################################################################################################################
        ###### Frame bas																							 ######
        ###################################################################################################################
        var.lab_thread = Label(master=self.frame_bas, bg=var.bg_frame_haut, text="")
        var.lab_thread.grid(row=0, column=0, padx=5, pady=5)
        self.lab_version = Label(master=self.frame_bas, bg=var.bg_frame_haut, text=_("PyngOuin version :") + var.version)
        self.lab_version.grid(row=0, column=1, padx=5, pady=5)
        self.lab_touvert = Label(master=self.frame_bas, bg=var.bg_frame_haut, text="")
        self.lab_touvert.grid(row=0, column=2, padx=5, pady=5)
        if lic.verify_license() == True:
            self.lab_lic = Label(master=self.frame_bas, bg=var.bg_frame_haut,
                                     text=_("Votre licence est active, il vous reste "+lic.jours_restants_licence()+" jours"))
            self.lab_lic.grid(row=0, column=10, padx=5, pady=5)
        else:
            self.lab_lic = Label(master=self.frame_bas, bg=var.bg_frame_haut,
                                 text=_("Vous n'avez pas de licence active"))
            self.lab_lic.grid(row=0, column=10, padx=5, pady=5)

        ###################################################################################################################
        ###### Frame haut 																							 ######
        ###################################################################################################################
        self.img = Image.open("logoP.png")
        self.img = self.img.resize((65, 65), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        self.panel = Label(self.frame_haut, image=self.img, height=65, width=65, bg=var.bg_frame_haut)
        self.panel.grid(row=0, column=0, pady=5, padx=10)
        Button(self.frame_haut, text='Start', padx=15, bg=var.couleur_rouge,
               command=lambda: fct_ping.lancerping(self.frame_haut), height=3).grid(row=0, column=1,
                                                                               pady=5)
        self.progress = ttk.Progressbar(self.frame_haut, orient=HORIZONTAL,
                                       length=250, mode='determinate')
        self.progress.grid(row=0, column=2, padx=5, pady=5)
        self.progress.grid_forget()
        self.lab_pourcent = Label(master=self.frame_haut, text="", bg=var.bg_frame_haut)
        self.lab_pourcent.grid(row=0, column=3, padx=5, pady=5)
        self.lab_pourcent.grid_forget()
        self.lab_nom_site = Label(master=self.frame_haut, text="", bg=var.bg_frame_haut)
        self.lab_nom_site.grid(row=0, column=4, padx=5, pady=5)
        self.lab_nom_site.config(text=var.nom_site)

        ###################################################################################################################
        ###### Frame centrale 																						 ######
        ###################################################################################################################
        self.frame1 = Frame(master=self.frame_main, bg=var.bg_frame_droit, padx=0, pady=0, width=200, relief=SUNKEN)
        self.frame1.pack(fill=BOTH, side=LEFT)
        self.frame2 = Frame(master=self.frame_main, bg=var.bg_frame_droit, padx=5, pady=5)
        self.frame2.pack(fill=BOTH, expand=True, side=LEFT)
        self.frame3 = Frame(master=self.frame_main, bg=var.bg_frame_droit, padx=0, pady=0, width=200, relief=SUNKEN)
        self.frame3.pack(fill=BOTH, side=LEFT)
        self.frame3.pack_propagate(False)
        #############################################
        ##### Gauche
        self.frameIp = Frame(master=self.frame1, bg="#FFFFFF", padx=5, pady=0, width=150, height=200, relief=SUNKEN)
        self.frameIp.pack_propagate(0)
        self.frameIp.pack(side=TOP, padx=5, pady=5, fill=X)
        self.frameAutre = Frame(master=self.frame1, bg="#FFFFFF", padx=5, pady=10, width=150, height=200, relief=SUNKEN)
        self.frameAutre.pack_propagate(0)
        self.frameAutre.pack(side=TOP, padx=5, pady=5, fill=X)

        self.lab_ip = Label(master=self.frameIp, text=_("IP"), bg="#FFFFFF")
        self.lab_ip.grid(row=0, column=0, padx=5, pady=5)
        self.ent_ip = Entry(self.frameIp, text=ip_pc)
        self.ent_ip.grid(row=1, column=0, padx=5, pady=5)
        self.ent_ip.insert(0, ip_pc)
        self.lab_hote = Label(master=self.frameIp, text=_("Nombre d'hotes"), bg="#FFFFFF")
        self.lab_hote.grid(row=2, column=0, padx=5, pady=5)
        self.ent_hote = Entry(self.frameIp, text="255")
        self.ent_hote.grid(row=3, column=0, padx=5, pady=5)
        self.ent_hote.insert(0, "255")
        self.ent_tout = ttk.Combobox(master=self.frameIp, values=[
            "Tout",
            "Alive"], width=18)
        self.ent_tout.set("Tout")
        self.ent_tout.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.lab_port = Label(master=self.frameIp, text=_("Ports (xx,xx)"), bg="#FFFFFF")
        self.lab_port.grid(row=5, column=0, padx=5, pady=5)
        self.ent_port = Entry(self.frameIp, text="80")
        self.ent_port.grid(row=6, column=0, padx=5, pady=5)

        Button(self.frameIp, text=_('Valider'), width=15, padx=10, command=self.aj_ip, bg=var.bg_but).grid(row=10, columnspan=2,
                                                                                              pady=5)

        #############################################
        ##### Frame centrale
        #############################################

        self.tab_ip_scroll = Scrollbar(self.frame2)
        self.tab_ip_scroll.pack(side=RIGHT, fill=Y)
        self.columns = (_('IP'), _('Nom'), _('mac'), _('port'), _('Latence'), _('Suivi'), _('Comm'), _('exc'))
        self.tab_ip = ttk.Treeview(self.frame2, yscrollcommand=self.tab_ip_scroll.set, selectmode="extended", columns=self.columns,
                                  show='headings')
        for col in self.columns:
            self.tab_ip.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tab_ip, _col, False))
        self.tab_ip.column("#0", width=0, stretch=FALSE)
        self.tab_ip.column(_("IP"), anchor=CENTER, stretch=TRUE, width=80)
        self.tab_ip.column(_("Nom"), anchor=CENTER, stretch=TRUE, width=80)
        self.tab_ip.column(_("mac"), anchor=CENTER, stretch=TRUE, width=80)
        self.tab_ip.column(_("port"), anchor=CENTER, stretch=TRUE, width=80)
        self.tab_ip.column(_("Latence"), anchor=CENTER, width=50, stretch=TRUE)
        self.tab_ip.column(_("Suivi"), anchor=CENTER, width=30, stretch=FALSE)
        self.tab_ip.column(_("Comm"), anchor=CENTER, stretch=TRUE, width=80)
        self.tab_ip.column(_("exc"), anchor=CENTER, width=30, stretch=TRUE)
        self.tab_ip.bind('<ButtonRelease-1>', self.item_selected)
        self.tab_ip.bind('<3>', self.right_clic)
        self.tab_ip.pack(expand=YES, fill=BOTH)
        self.tab_ip.bind("<Double-Button-1>", self.on_double_click)


        ### Frame Droit

        self.frameNom = Frame(master=self.frame3, bg="#FFFFFF", padx=5, pady=5, width=180, relief=SUNKEN)
        self.frameNom.pack_propagate(0)
        self.frameNom.pack(side=TOP, padx=5, pady=5, fill=X)

        self.ent_nom = Entry(self.frameNom, text="")
        self.ent_nom.grid_propagate(0)
        self.ent_nom.grid(row=0, column=0, padx=5, pady=5)

        self.ent_nom.insert(0, "")

        self.ent_comm = Entry(self.frameNom, text="")
        self.ent_comm.grid_propagate(0)
        self.ent_comm.grid(row=1, column=0, padx=5, pady=5)

        self.ent_comm.insert(0, "")

        Button(self.frameNom, text=_('Modifier'), padx=10, command=self.nom_modif, width=10, bg=var.bg_but).grid(row=2, pady=5)

        self.frametab2 = Frame(master=self.frame3, bg=var.bg_frame_droit, padx=5, pady=5, width=180, height=20, relief=SUNKEN)
        self.frametab2.pack_propagate(0)
        self.frametab2.pack(side=TOP)
        self.frameDelais = Frame(master=self.frame3, bg="#FFFFFF", padx=5, pady=5, width=180, relief=SUNKEN)
        self.frameDelais.pack(side=TOP, padx=5, pady=5, fill=X)

        self.lab_delais = Label(master=self.frameDelais, text=_("Délais entre 2 pings"), bg="#FFFFFF", width=20)
        self.lab_delais.grid(row=0, column=0, padx=5, pady=5, columnspan=3)
        delais = StringVar(value=var.delais)
        self.spin_delais = Spinbox(self.frameDelais, from_=5, to=100000000, width=5, textvariable=delais, command=self.spinDelais)
        self.spin_delais.grid(row=1, column=1, padx=0, pady=5)
        self.lab_delais1 = Label(master=self.frameDelais, text="5 s", bg="#FFFFFF")
        self.lab_delais1.grid(row=1, column=0, padx=0, pady=5)

        self.lab_test = Label(master=self.frameDelais, text=_("Nombre HS"), bg="#FFFFFF")
        self.lab_test.grid(row=2, column=0, padx=0, pady=5)
        delais1 = StringVar(value=var.envoie_alert)
        self.spin_test = Spinbox(self.frameDelais, from_=1, to=10, width=5, textvariable=delais1, command=self.spinTest)
        self.spin_test.grid(row=2, column=1, padx=0, pady=5)
        self.check_popup1.set(var.popup)
        self.check_popup = Checkbutton(self.frameDelais, text=_('Popup'), variable=self.check_popup1, onvalue=1, offvalue=0, bg="#FFFFFF",
                                  command=self.isCheckedpopup)
        self.check_popup.grid(row=3, columnspan=3, padx=0, pady=5, sticky='w')
        self.check_mail1.set(var.mail)
        self.check_mail = Checkbutton(self.frameDelais, text=_('Mail'), variable=self.check_mail1, onvalue=1, offvalue=0, bg="#FFFFFF",
                                 command=self.isCheckedMail)
        self.check_mail.grid(row=4, columnspan=3, padx=0, pady=5, sticky='w')
        self.check_telegram1.set(var.telegram)
        self.check_telegram = Checkbutton(self.frameDelais, text=_('Telegram'), variable=self.check_telegram1, onvalue=1, offvalue=0,
                                     bg="#FFFFFF",
                                     command=self.isCheckedTelegram)
        self.check_telegram.grid(row=5, columnspan=3, padx=0, pady=5, sticky='w')
        self.check_recap1.set(var.recap)
        self.check_recap = Checkbutton(self.frameDelais, text=_('Mail Recap'), variable=self.check_recap1, onvalue=1, offvalue=0,
                                  bg="#FFFFFF",
                                  command=self.isCheckedRecap)
        self.check_recap.grid(row=6, columnspan=3, padx=0, pady=5, sticky='w')
        self.check_db1.set(var.db)
        self.check_db = Checkbutton(self.frameDelais, text=_('DB Externe'), variable=self.check_db1, onvalue=1, offvalue=0,
                               bg="#FFFFFF",
                               command=self.isCheckedDb)
        self.check_db.grid(row=7, columnspan=3, padx=0, pady=5, sticky='w')

        if lic.verify_license() == False:
            self.check_popup.config(state=DISABLED)
            self.check_mail.config(state=DISABLED)
            self.check_telegram.config(state=DISABLED)
            self.check_recap.config(state=DISABLED)
            self.check_db.config(state=DISABLED)

        ########### Effacer #########################################
        self.frametab1 = Frame(master=self.frame3, bg=var.bg_frame_droit, padx=5, pady=5, width=180, height=20, relief=SUNKEN)
        self.frametab1.pack_propagate(0)
        self.frametab1.pack(side=TOP, expand=False)
        # ______________________________________________________________
        # Créer un menu
        # ______________________________________________________________
        self.menubar = design.create_menu(self.fenetre, self.frame_haut)
        self.fenetre.config(menu=self.menubar)

        # ______________________________________________________________
        # Lancer la fenetre
        # ______________________________________________________________
        self.fenetre.protocol("WM_DELETE_WINDOW", self.Intercepte)




    def get_lang(self):
        try:
            # Détection du chemin de base (normal ou depuis un exécutable PyInstaller)
            if getattr(sys, 'frozen', False):  # Vérifie si le script est exécuté depuis un exe
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()

            # Récupération de la langue via param_gene
            langue = param_gene.lang()
            var.langue = langue

            # Chemin vers le dossier contenant les fichiers de traduction
            localedir = os.path.join(base_path, 'fichier/locale')

            # Chargement des traductions
            traduction = gettext.translation(var.langue, localedir=localedir, languages=[var.langue])
            traduction.install()

        except Exception as e:
            # Gestion des erreurs : affichage d'un message d'erreur et fallback sur gettext par défaut
            error_message = f"Error: {str(e)}"
            design.alert(error_message)  # Affiche l'erreur dans l'interface utilisateur
            print(error_message)  # Affiche l'erreur dans la console

            # Fallback : installation de gettext sans fichier de traduction spécifique
            gettext.install('PyngOuin')

    def plugin(name):
        result = 0
        try:
            file=open("fichir/plugin/"+name+"/main.py")
            result = True
            file.close()
        except:
            pass
        return result

    def plug(self):
        for filename in os.listdir("fichier/plugin"):
            full_filename = os.path.join("fichier/plugin", filename)
            if os.path.isdir(full_filename):
                var.plugIn.append(filename)



    def maj(self):
        import fichier.thread_maj as maj1
        threading.Thread(target=maj1.main(), args=()).start()

    def lireParam(self):
        try:
            variable = param_db_quit.lire_param_db()
            var.delais = int(variable[0])
            var.envoie_alert = int(variable[1])
            var.popup = variable[2]
            var.mail = variable[3]
            var.telegram = variable[4]
            var.recap = variable[5]
        except:
            pass


    def histo(self):
        selected_item = self.tab_ip.selection()[0]
        val = selected_item = self.tab_ip.selection()[0]
        fct_suivi.suivitxt(val)


    def graph(self):
        val = self.tab_ip.selection()[0]
        fct_graph.main(val)


    def suivi(self):
        selected_item = self.tab_ip.selection()[0]
        suivi = ""
        try:
            suivi = self.tab_ip.item(selected_item)["values"][5]
        except:
            pass
        if suivi == "X":
            self.tab_ip.set(selected_item, column="Suivi", value="")
        else:
            self.tab_ip.set(selected_item, column="Suivi", value="X")

    def exclusion(self):
        selected_item = self.tab_ip.selection()[0]
        suivi = ""
        try:
            suivi = self.tab_ip.item(selected_item)["values"][7]
        except:
            pass
        if suivi == "X":
            self.tab_ip.set(selected_item, column="exc", value="")
        else:
            self.tab_ip.set(selected_item, column="exc", value="X")

    ###### Récupérer l'ip.pin du PC
    def getentip(self):
        ip = self.ent_ip.get()
        showinfo("OK", ip)
    def quitSav(self):
        param_db_quit.save_param_db()

    ###### Fermeture de la fenetre
    def Intercepte(self):
        try:
            val = design.question_box("Attention", "Etes vous sur de vouloir quitter ?")
            if val == True:
                for process in (process for process in psutil.process_iter() if process.name() == "OpenHardwareMonitor.exe"):
                    process.kill()
                os._exit(0)


        except Exception as e:
            design.logs("exit - " + str(e))


    ###### Fonction ajouter une IP
    def aj_ip(self):
        Thread_aj_ip.aj_ip(self.ent_ip.get(), self.ent_hote.get(), self.ent_tout.get(), self.ent_port.get(), 0)


    ###### Délais entre 2 pings
    def spinDelais(self):
        fct_ping.stopping(self.frame_haut)
        var.delais = 5
        nbr = self.spin_delais.get()
        var.delais = nbr
        if int(nbr) < 60:
            delais = str(nbr) + " s"
        elif int(nbr) < 3600:
            nbr = math.ceil(int(nbr) / 60)
            delais = str(nbr) + " min"
        elif int(nbr) < 86400:
            nbr = math.ceil(int(nbr) / 3600)
            delais = str(nbr) + " h"
        else:
            nbr = math.ceil(int(nbr) / 86400)
            delais = str(nbr) + " j"
        self.lab_delais1.config(text=delais)


    def spinTest(self):
        fct_ping.stopping(self.frame_haut)
        nbr = self.spin_test.get()
        var.envoie_alert = nbr


    ###### Sélection d'une ligne
    def item_selected(self, event):
        selected_item = self.tab_ip.selection()
        result = self.tab_ip.item(selected_item)["values"]
        try:
            self.nom = result[1]
            self.ent_nom.delete(0, END)
            self.ent_nom.insert(0, self.nom)

            self.comm = result[6]
            self.ent_comm.delete(0, END)
            self.ent_comm.insert(0, self.comm)
        except Exception as e:
            print(e)
            #design.logs("exit - " + str(e))


    def open_nav(self, ip):
        webbrowser.open('http://' + ip)

    def on_double_click(self, event):
        selected_item = self.tab_ip.selection()
        result = self.tab_ip.item(selected_item)["values"]
        try:
            ip = result[0]
            self.open_nav(ip)
        except Exception as e:
            print(e)

    def right_clic(self, event):
        # create a popup menu
        selected_item = self.tab_ip.selection()[0]
        suivi1 = ""
        try:
            suivi1 = self.tab_ip.item(selected_item)["values"][5]
            excl1 = self.tab_ip.item(selected_item)["values"][7]
        except:
            pass
        rowID = self.tab_ip.identify('item', event.x, event.y)
        if rowID:
            self.tab_ip.selection_set(rowID)
            self.tab_ip.focus_set()
            self.tab_ip.focus(rowID)

            menu_tree = Menu(self.fenetre, tearoff=0)
            menu_tree.add_command(label="Ouvrir dans le navigateur", command=lambda: self.open_nav(rowID))
            menu_tree.add_separator()
            menu_tree.add_command(label="Suivi", command=self.suivi)
            menu_tree.add_command(label="Exclure", command=self.exclusion)
            if suivi1 == "X":
                menu_tree.add_command(label="Historique", command=self.histo)
                menu_tree.add_command(label="Graphique", command=self.graph)
            menu_tree.add_separator()
            menu_tree.add_command(label="Effacer", command=self.delete_item)
            menu_tree.post(event.x_root, event.y_root)
        else:
            pass


    ###### Supprimer un item
    def delete_item(self):
        selected_item = self.tab_ip.selection()[0]
        val = design.question_box("Attention", "Etes vous sur de vouloir effacer l'ip.pin " + selected_item[0])
        if val:
            self.tab_ip.delete(selected_item)
            fct_ping.lancerping(self.frame_haut)


    ###### Modifier le nom
    def nom_modif(self):
        selected_item = self.tab_ip.selection()
        self.tab_ip.set(selected_item, column=_("Nom"), value=self.ent_nom.get())
        self.tab_ip.set(selected_item, column=_("Comm"), value=self.ent_comm.get())
        pass


    def treeview_sort_column(self, tv, col, reverse):
        column_index = self.tab_ip["columns"].index(col)
        l = [(str(tv.item(k)["values"][column_index]), k) for k in tv.get_children()]
        l.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


    ###### Cocher case Popup
    def isCheckedpopup(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_popup1.get() == 1:
            var.popup = 1
        elif self.check_popup1.get() == 0:
            var.popup = 0


    def isCheckedPort(self):
        if self.check_port1.get() == 1:
            var.checkPort = True
        elif self.check_port1.get() == 0:
            var.checkPort = False


    ###### Cocher case mail
    def isCheckedMail(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_mail1.get() == 1:
            var.mail = 1
        elif self.check_mail1.get() == 0:
            var.mail = 0


    ###### Cocher case recap
    def isCheckedRecap(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_recap1.get() == 1:
            var.recap = 1
        elif self.check_recap1.get() == 0:
            var.recap = 0


    def isCheckedLat(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_lat1.get() == 1:
            var.lat = 1

        elif self.check_lat1.get() == 0:
            var.lat = 0


    def isCheckedTelegram(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_telegram1.get() == 1:
            var.telegram = 1

        elif self.check_telegram1.get() == 0:
            var.telegram = 0


    def isCheckedDb(self):
        fct_ping.stopping(self.frame_haut)
        if self.check_db1.get() == 1:
            var.db = 1

        elif self.check_db1.get() == 0:
            var.db = 0

    def reload_all(self):
        self.fenetre.destroy()

        root = tk.Tk()
        page_principale = main(root)
        root.protocol("WM_DELETE_WINDOW", quitter)
        root.mainloop()


###################################################################################################################
###### Fenetre principale																					 ######
###################################################################################################################
# Créer une nouvelle fenêtre



root = tk.Tk()
page_principale = main(root)
root.protocol("WM_DELETE_WINDOW", quitter)
root.mainloop()

