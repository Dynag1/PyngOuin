import csv
import threading
from tkinter import *
from tkinter.messagebox import *
from tkinter import messagebox, filedialog
from fichier import param_mail, param_gene, param_db, param_mail_recap, var, thread_xls, fct_ping
import fichier.param_db_quit as db_quit
import logging.config
import logging
import os
import sys
import importlib.util

from fichier import lic


def logs(log):
    logging.config.fileConfig('fichier/logger.ini', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    logger.error(log, exc_info=True)


def question_box(title, message):
    var = messagebox.askquestion(title, message)
    resp = False
    if var == "yes":
        resp = True
    else:
        resp = False
    return resp

def affilogs():
    path = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    print(path + "/log.log")
    os.startfile(path + "/log.log")

def effalogs():
    path = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    if os.path.exists(path+ "/log.log"):
        os.remove(path+ "/log.log")

def rac_s(ev=None):
    try:
        save_csv()
    except Exception as e:
        logs("design - " + str(e))

def rac_o(ev=None):
    try:
        load_csv()
    except Exception as e:
        logs("design - " + str(e))

def rac_x(ev=None):
    try:
        xlsExport()
    except Exception as e:
        logs("design - " + str(e))


def rac_w(ev=None):
    try:
        xlsImport()
    except Exception as e:
        logs("design - " + str(e))


"""def rac_f(ev=None):
    try:
        pluginSnyf()
    except Exception as e:
        logs("design - " + str(e))"""


def fenAPropos():
    try:
        import fichier.fen_a_propos as apropos
        apropos.main()
    except Exception as e:
        logs("design - " + str(e))


def fenAChangelog():
    try:
        import fichier.fen_changelog as apropos
        apropos.main()
    except Exception as e:
        logs("design - " + str(e))


def xlsImport():
    # try:
    thread_xls.openExcel()


# except Exception as e:
#	logs("design - " + str(e))

def xlsExport():
    # try:
    thread_xls.saveExcel()


# except Exception as e:
#	logs("design - " + str(e))



def test():
    try:
        import fichier.MySql as test
        t = threading.Thread(target=test.create_table(test)).start()
    except Exception as e:
        logs("design - " + str(e))


def alert(message):
    showinfo("alerte", message)


def lire_nom(ip):
    try:
        nom1 = var.app_instance.tab_ip.item(ip, 'values')
        nom = nom1[1]
        return nom
    except Exception as e:
        # logs("design - " + str(e))
        pass


def save_csv():
    try:

        Tk().withdraw()
        doss = os.getcwd()+"\\bd\\"
        filename = filedialog.asksaveasfilename(initialdir=doss, title="Select file", filetypes=(
            ("Pin", "*.pin"), ("all files", "*.*")))
        filename = filename.split(".")
        filename = filename[0]
        with open(filename+".pin", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')

            for row_id in var.app_instance.tab_ip.get_children():
                row = var.app_instance.tab_ip.item(row_id)['values']
                csvwriter.writerow(row)

        threading.Thread(target=alert, args=(_("Votre plage IP à été enregistré"),)).start()
    except Exception as e:
        logs("design - " + str(e))
        return


def load_csv():
    try:
        doss = os.getcwd() + "\\bd\\"
        filename = filedialog.askopenfilename(initialdir=doss, title="Select File", filetypes=(
            ("Pin", "*.pin"), ("all files", "*.*")))
        with open(filename) as myfile:
            csvread = csv.reader(myfile, delimiter=',')
            i = 0
            for row in csvread:
                var.app_instance.tab_ip.insert(parent='', index=i, tag=row[0], iid=row[0], values=row)
                var.app_instance.tab_ip.tag_configure(tagname=row[0])
                i = i + 1
    except Exception as e:
        logs("design - " + str(e))
        return


def paramGene():
    threading.Thread(target=param_gene.main).start()


def paramDb():
    threading.Thread(target=param_db.main).start()


def paramMail():
    threading.Thread(target=param_mail.main).start()


def paramMailRecap():
    threading.Thread(target=param_mail_recap.main).start()

def quit_db():
    db_quit.save_param_db()

def pluginGest():
    try:
        import os
        import subprocess
        path = os.path.abspath(os.getcwd())+"\\fichier\\plugin"
        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    except Exception as e:
        print(e)
        logs("design - " + str(e))


def logs(message):
    """Fonction simple pour enregistrer les logs."""
    with open("plugin_logs.txt", "a") as log_file:
        log_file.write(message + "\n")


def logs(message):
    """Fonction simple pour enregistrer les logs."""
    with open("plugin_logs.txt", "a") as log_file:
        log_file.write(message + "\n")


def plugIn(plugin_name):
    """
    Charge et exécute dynamiquement un plugin Python.

    :param plugin_name: Nom du plugin à charger (doit correspondre au nom du dossier dans 'plugin/')
    """
    print(f"Tentative de chargement du plugin : {plugin_name}")
    #try:
    # Configuration du chemin vers le dossier des plugins (au même niveau que l'exécutable principal)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire contenant main.py
    plugin_root = os.path.join(base_dir, 'plugin')  # Dossier plugin au même niveau

    # Vérification que le dossier 'plugin' existe
    if not os.path.exists(plugin_root):
        raise FileNotFoundError(f"Le dossier 'plugin' est introuvable : {plugin_root}")

    # Ajout du dossier 'plugin' au PYTHONPATH si nécessaire
    if plugin_root not in sys.path:
        sys.path.insert(0, plugin_root)

    # Construction du chemin complet vers le fichier main.py du plugin
    plugin_dir = os.path.join(plugin_root, plugin_name)
    full_path_to_module = os.path.join(plugin_dir, 'main.py')

    if not os.path.exists(full_path_to_module):
        raise FileNotFoundError(f"Le fichier main.py est introuvable dans le dossier : {plugin_dir}")

    print(f"Chemin du module détecté : {full_path_to_module}")

    # Génération d'un nom unique pour le module
    module_name = f"plugin_{plugin_name}_main"

    # Chargement dynamique du module
    spec = importlib.util.spec_from_file_location(module_name, full_path_to_module)
    if spec is None:
        raise ImportError("Impossible de créer la spécification du module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module  # Nécessaire pour les imports relatifs dans le plugin
    spec.loader.exec_module(module)

    # Vérification et exécution de la fonction main() du plugin
    if hasattr(module, 'main'):
        print(f"Exécution de la fonction main() du plugin {plugin_name}")
        module.main()
    else:
        raise AttributeError(f"La fonction main() est introuvable dans le module {module_name}.")

    """except Exception as e:
        error_message = f"Erreur lors du chargement ou de l'exécution du plugin '{plugin_name}': {str(e)}"
        print(error_message)
        logs(error_message)"""


"""def pluginSnyf():
    try:
        import plugin.Snyf.main as apropos
        apropos.main()
    except Exception as e:
        print(e)
        logs("design - " + str(e))"""
#  Menu
def create_menu(fenetre, frame_haut):
    menubar = Menu(fenetre)



    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label=_("Sauvegarder  ctrl+s"), command=save_csv)
    menu1.add_command(label=_("Ouvrir  ctrl+o"), command=load_csv)
    menu1.add_command(label=_("Charger"), command=load_csv)
    menu1.add_command(label=_("Tout effacer"), command=tab_erase)
    menu1.add_separator()
    #menu1.add_command(label=_("Test"), command=test)
    menu1.add_command(label=_("Sauvegarder les réglages"), command=quit_db)
    menubar.add_cascade(label=_("Fichier"), menu=menu1)

    menu2 = Menu(menubar, tearoff=0)
    menu2.add_command(label=_("Général"), command=paramGene)


    if lic.verify_license():
        menu2.add_command(label=_("Envoies"), command=paramMail)
        menu2.add_command(label=_("Mail Recap"), command=paramMailRecap)
        menu2.add_command(label=_("DB"), command=paramDb)
    menubar.add_cascade(label=_("Paramètres"), menu=menu2)

    menu4 = Menu(menubar, tearoff=0)
    menu4.add_command(label=_("Export xls ctrl+x"), command=xlsExport)
    menu4.add_command(label=_("Import xls ctrl+w"), command=xlsImport)
    menu4.add_separator()
    menubar.add_cascade(label=_("Fonctions"), menu=menu4)

    menu3 = Menu(menubar, tearoff=0)
    menu3.add_command(label=_("A propos"), command=fenAPropos)
    menu3.add_command(label=_("Changelog"), command=fenAChangelog)
    menu3.add_command(label=_("Logs"), command=affilogs)
    menu3.add_command(label=_("Effacer Logs"), command=effalogs)
    menu3.add_separator()

    menu5 = Menu(menubar, tearoff=0)
    menu5.add_command(label=_("Gestion"), command=pluginGest)
    menu5.add_separator()
    for plug in var.plugIn:
        menu5.add_command(label=plug, command=lambda plug1=plug: plugIn(plug1))


    menubar.add_cascade(label=_("Plugins"), menu=menu5)

    menubar.add_cascade(label="?", menu=menu3)
    menubar.bind_all('<Control-s>', rac_s)
    menubar.bind_all('<Control-l>', lambda ev: fct_ping.lancerping(frame_haut))
    menubar.bind_all('<Control-x>', rac_x)
    menubar.bind_all('<Control-w>', rac_w)
    menubar.bind_all('<Control-o>', rac_o)
    return menubar


def tab_erase():
    try:
        val = question_box(_("Attention"), _("Etes vous sur de vouloir effacer la liste ?"))
        if val == True:
            for i in var.app_instance.tab_ip.get_children():
                var.app_instance.tab_ip.delete(i)
    except Exception as e:
        logs("design - " + str(e))


def center_window(w):
    try:
        eval_ = w.nametowidget('.').eval
        eval_('tk::PlaceWindow %s center' % w)
    except Exception as e:
        logs("design - " + str(e))
