import hashlib
import uuid
from tkinter import *
from tkinter import ttk
from queue import Queue

version = "2.2.2"
site = 'http://prog.dynag.co'
###########   Couleurs ##########
bg_frame_haut = "#81BEF7"
bg_frame_mid = "#A9D0F5"
bg_frame_droit = "#A9D0F5"
bg_but = "#81BEF7"
app_instance = ""
q = Queue()
langue = "fr"
liste_maj = {}
code = ""



couleur_vert = "#baf595"
couleur_jaune = "#fffd6a"
couleur_orange = "#ffb845"
couleur_rouge = "#f97e7e"
couleur_noir = "#6d6d6d"


ipPing = 0
popup = 0
mail = 0
telegram = 0
db = 0
recap = 0
lat = 0
nom_site=""
z=0
checkPort = False
nom_site

envoie_alert = 1

tab_ip = ttk.Treeview
lab_thread = Label
progress = ttk.Progressbar
but_lancer_ping = Button
lab_nom_site = Label
lab_pourcent = Label
lab_tempCpu = Label

threadouvert=0
threadferme=0
delais=5

liste_nom={}
liste_hs={}
liste_mail={}
liste_telegram={}

param_mail_compte=""
param_mail_pass=""
param_mail_smtp=""
param_mail_port=""
param_mail_serveur=""
param_mail_envoie=""

b = False
telegram_id = "548421802"
l=""
hik = 0
axis = 0
samsung = 0
avigilon = 0
onvif = 0
upnp = 0

timeTest = 3

plugIn = []
plugTempVal = 50

def li(a):
    c = a+5874632589
    c = c*54
    c = hashlib.sha256(str(c).encode()).hexdigest()
    print(l)
    print(c)
    if str(c) == str(l):
        print("LI OK")
        return True
    else:
        print("LI NONOK")
        return False
