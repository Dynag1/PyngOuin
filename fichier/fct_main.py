import os
import threading
from pathlib import Path

import fichier.design as design
import psutil

import fichier.var as var

def plug():
    for filename in os.listdir("../plugin"):
        full_filename = os.path.join("../plugin", filename)
        if os.path.isdir(full_filename):
            var.plugIn.append(filename)

def plugin(name):
    result = 0
    try:
        file=open("plugin/"+name+"/main.py")
        result = True
        file.close()
    except:
        pass
    return result

def maj():
    import fichier.thread_maj as maj1
    threading.Thread(target=maj1.main(), args=()).start()

def Intercepte():
    try:
        val = design.question_box(_("Attention"), _("Etes vous sur de vouloir quitter ?"))
        if val == True:
            for process in (process for process in psutil.process_iter() if process.name() == "OpenHardwareMonitor.exe"):
                process.kill()
            os._exit(0)


    except Exception as e:
        design.logs("exit - " + str(e))

def creerDossier(nom):
    # Spécifiez le chemin du dossier à créer
    chemin_dossier = os.getcwd()+"\\"+nom

    # Vérifiez si le dossier n'existe pas, puis créez-le
    dossier = Path(chemin_dossier)
    if not dossier.exists():
        dossier.mkdir(parents=True, exist_ok=True)
    else:
        pass
