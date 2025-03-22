import subprocess
import time
from tkinter import *
import datetime
import os
import queue
import threading
from multiprocessing import Pool
import multiprocessing
import fichier.fct_thread as fct_thread_popup
import pythonping as ping
import fichier.param_gene as param_gene
import fichier.thread_recap_mail as thread_recap_mail
import fichier.var as var
import fichier.fct_ip as fct_ip
import fichier.fct_suivi as fct_suivi
import fichier.MySql as mysql
import fichier.design as design

"""
*********************************************************************************************
*********************************************************************************************
*****	Fonctions de pings															   ******
*********************************************************************************************
*********************************************************************************************
"""
q = queue.Queue()


###########################################################################################
#####				Incrémentation de la perte sur la liste							  #####
###########################################################################################
def list_increment(liste, ip):
    try:
        if ip in liste:
            if int(liste[ip]) < int(var.envoie_alert):
                liste[ip] += 1
            else:
                liste[ip] = liste[ip]
            #print(str(ip.pin)+" - "+str(liste[ip.pin]))
        else:

            liste[ip] = 1
    except Exception as inst:
        design.logs("ping-" + str(inst))


###########################################################################################
#####				Marqué l'hôte comme revenu sur les listes						  #####
###########################################################################################
def list_ok(liste, ip):
    try:
        if ip in liste:
            if liste[ip] == 10:
                liste[ip] = 20
            else:
                try:
                    del var.liste[ip]
                except:
                    pass
    except Exception as inst:
        design.logs("ping-" + str(inst))


def db_ext(ip, nom, etat, latence):
    if var.db == 1:
        try:
            var.q.put(lambda: mysql.add_enre(ip, nom, etat, latence, var.nom_site))
        except Exception as inst:
            design.logs("ping-" + str(inst))


###########################################################################################
#####				Fonction de ping												  #####
###########################################################################################
def test_ping(ip):
    try:
        result = ping.ping(ip, size=10, count=1)
        etat = ""
        latence = ""
        nom = ""
        suivi = ""
        selected_item = ip
        valeur = var.app_instance.tab_ip.item(selected_item)["values"]
        excl = ""

        try:
            suivi = str(valeur[5])
            excl = str(valeur[7])
            nom = valeur[1]
        except Exception as inst:
            #design.logs("ping-" + str(inst))
            pass
        if suivi != "X":
            if os.path.exists('suivi/' + ip + '.txt'):
                var.q.put(fct_suivi.supprimer(ip))

        date = str(datetime.datetime.now())
        message = date + " || "

        if var.ipPing == 0:
            return
#### Si HS
        if result.rtt_avg_ms == int(2000):
            message = message + "HS || 200"
            color = var.couleur_noir
            if excl != "X":
                try:
                    list_increment(var.liste_hs, ip)
                    list_increment(var.liste_mail, ip)
                    list_increment(var.liste_telegram, ip)
                except Exception as inst:
                    design.logs("ping-" + str(inst))
            etat = "HS"
            latence = ""
            ttot = "HS"
            var.q.put(lambda: var.app_instance.tab_ip.tag_configure(tagname=ip, background=color))
#### SI OK
        else:
            message = message + " OK || " + str(result.rtt_avg_ms) + " ms"
            if result.rtt_avg_ms < 2:
                color = var.couleur_vert
            elif result.rtt_avg_ms < 10:
                color = var.couleur_jaune
            elif result.rtt_avg_ms < 50:
                color = var.couleur_orange
            else:
                color = var.couleur_rouge
            if result.rtt_avg_ms < 1:
                ttot = "<1 ms"
            else:
                ttot = str(result.rtt_avg_ms) + " ms"
            etat = "OK"
            latence = ttot
            if excl != "X":
                try:
                    list_ok(var.liste_hs, ip)
                    list_ok(var.liste_mail, ip)
                    list_ok(var.liste_telegram, ip)
                except Exception as inst:
                    design.logs("ping-" + str(inst))


#####  Afficher sur la lise les valeurs + couleur
        try:
            var.q.put(lambda: var.app_instance.tab_ip.tag_configure(tagname=ip, background=color))
            var.q.put(lambda: var.app_instance.tab_ip.set(ip, column=_("Latence"), value=ttot))
        except TclError as inst:
            design.logs("ping-" + str(inst))


        message = message + "\n"
        print("fin test")
        if var.db == 1:
            var.q.put(lambda: db_ext(ip, nom, etat, latence))
        if suivi == "X":
            var.q.put(lambda: fct_suivi.ecrire(ip, message))
        return message
        threading.current_thread().join()
    except Exception as e:
        design.logs("fct_ping - " + str(e))



###########################################################################################
#####				Lancement des pings sur les workers                  			  #####
###########################################################################################
def worker():
    try:
        while True:
            item = q.get()
            if item is None:
                break
            subprocess.call(test_ping(str(item)), shell=True)
            #test_ping(str(item))
            q.task_done()

    except Exception as e:
        design.logs("fct_ping - " + str(e))



"""def workerPing(task):

    print("Worker exécute la tâche :",task)"""
###########################################################################################
#####				Création des workers et mise en liste des tâches     			  #####
###########################################################################################

"""def testPing():
    tasks = queue.Queue()
    tasks.empty()
    pool2 = Pool(processes=4)

    for parent in var.app_instance.tab_ip.get_children():
        result = var.app_instance.tab_ip.item(parent)["values"]
        ip1 = result[0]
        tasks.put(test_ping(str(ip1)))
        # tasks.put(ip1)
    pool2.apply_async(workerPing, tasks)

    # Fermer la pool de workers
    print("close")
    pool2.close()
    print("closeOK")
    #pool2.join()
    print("closeOK1")"""

def test2():

    for parent in var.app_instance.tab_ip.get_children():
        result = var.app_instance.tab_ip.item(parent)["values"]
        ip1 = result[0]
        q.put(ip1)
    q.join()

def threadPing():
    param_gene.nom_site()
    cpus = multiprocessing.cpu_count()
    cpu = cpus/2 # Detect number of cores
    print("Creating %d threads" % cpu)
    for i in range(int(cpu)):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
    if var.db == 1:
        try:
            mysql.create_table(var.nom_site)
        except:
            pass
    while True:
        try:
            if var.ipPing == 1:
               startfct = time.time() * 1000.0
               test2()
               stopfct = time.time() * 1000.0
               tpsfct = (stopfct - startfct) / 1000
               if tpsfct < int(var.delais):
                   time.sleep(int(var.delais) - tpsfct)
               else:
                   pass
            else:
                print("STOP")
                break
        except Exception as e:
            #design.logs("fct_ping - " + str(e))
            #print(e)
            pass


"""def threadPing1():
    param_gene.nom_site()
    if var.db == 1:
        try:
            mysql.create_table(var.nom_site)
        except:
            pass
    while True:
        try:
            if var.db == 1:
                try:
                    mysql.vider_table(var.nom_site)
                except:
                    pass
            startfct = time.time() * 1000.0

            startfct = time.time() * 1000.0
            if var.ipPing == 1:
                nbrworker = multiprocessing.cpu_count()
                if nbrworker > 1:
                    nbrworker = 1

                num_worker_threads = nbrworker
                q = queue.Queue()
                threads = []
                for i in range(num_worker_threads):
                    t = threading.Thread(target=worker, args=(q, i,), daemon=True)
                    t.start()
                    threads.append(t)
                i = 0
                for parent in var.app_instance.tab_ip.get_children():
                    result = var.app_instance.tab_ip.item(parent)["values"]
                    ip1 = result[0]
                    q.put(ip1)
                # block until all tasks are done
                q.join()
                # stop workers
                for i in range(num_worker_threads):
                    q.put(None)
                for t in threads:
                    t.join()

                stopfct = time.time() * 1000.0
                tpsfct = (stopfct - startfct) / 1000

                if tpsfct < int(var.delais):
                    time.sleep(int(var.delais) - tpsfct)
                else:
                    pass
            else:
                print("STOP")
                break

        except Exception as e:
            design.logs("fct_ping - " + str(e))

"""
###########################################################################################
#####				Gestion du bouton ping, lancer ou arrêter les pings				  #####
###########################################################################################
def lancerping(fenetre1):
    if var.ipPing == 0:
        fct_suivi.creerDossier()
        var.ipPing = 1
        Button(fenetre1, text='Stop', padx=15, bg=var.couleur_vert,
               command=lambda: lancerping(fenetre1), height=3).grid(row=0, column=1, pady=5)
        threading.Thread(target=threadPing).start()
        if var.popup == 1 or var.mail == 1 or var.telegram == 1:
            var.q.put(lambda: threading.Thread(target=fct_thread_popup.main).start())
        if var.recap == 1:
            var.q.put(lambda: threading.Thread(target=thread_recap_mail.main).start())
        if var.lat == 1:
            var.q.put(lambda: threading.Thread(target=fct_ip.suiviLat, args=()).start())
    else:
        Button(fenetre1, text='Start', padx=15, bg=var.couleur_rouge,
               command=lambda: lancerping(fenetre1), height=3).grid(row=0, column=1, pady=5)
        var.ipPing = 0
    return


###########################################################################################
#####				Arrêt des pings si coche d'une case								  #####
###########################################################################################
def stopping(fenetre1):
    if var.ipPing == 0:
        return
    else:
        var.but_lancer_ping = Button(fenetre1, text='Start', padx=10, bg=var.couleur_rouge,
                                     command=lambda: lancerping(fenetre1), height=3).grid(row=0, column=1, pady=5)
        var.ipPing = 0
    return
