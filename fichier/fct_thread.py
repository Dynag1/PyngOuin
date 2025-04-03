import threading
import time
import fichier.design as design
import fichier.fct_thread_mail as fct_thread_mail
import fichier.thread_recap_mail as recap
import fichier.thread_telegram as thread_telegram
import fichier.var as var
from queue import Queue

"""
*********************************************************************************************
*********************************************************************************************
*****	Threads des alertes															    *****
*********************************************************************************************
*********************************************************************************************
"""



############################################################################################
#####	Lancement des différentes alertes										       #####
############################################################################################
def main():
    while True:
        time.sleep(10)
        if int(var.delais) < 10:
            time.sleep(10)
        else:
            time.sleep(int(var.delais))

        try:
            if var.ipPing == 1:
                if var.popup == 1:
                    try:
                        threading.Thread(target=popup, args=()).start()
                    except Exception as inst:
                        design.logs("fct_thread -" + str(inst))
                if var.mail == 1:
                    try:
                        threading.Thread(target=mail, args=()).start()
                    except Exception as inst:
                        design.logs("fct_thread -" + str(inst))
                if var.telegram == 1:
                    try:
                        threading.Thread(target=telegram, args=()).start()
                    except Exception as inst:
                        design.logs("fct_thread -" + str(inst))


            else:
                break
        except Exception as inst:
            design.logs("fct_thread--" + str(inst))
    if var.ipPing == 1:
        if var.recap == 1:
            try:
                threading.Thread(target=recapmail(), args=()).start()
            except Exception as inst:
                design.logs("fct_thread -" + str(inst))

############################################################################################
#####	Alerte Popup															       #####
############################################################################################
def popup():
    try:
        time.sleep(0)
        erase = ()
        ip_hs = ""
        ip_ok = ""
        for key, value in var.liste_hs.items():

            if int(value) == int(var.envoie_alert):
                ip_hs = ip_hs + key + "\n "
                var.liste_hs[key] = 10
            elif value == 20:
                ip_ok = ip_ok + key + "\n "
                erase = erase + (str(key),)
        for cle in erase:
            try:
                del var.liste_hs[cle]
            except:
                pass
        if len(ip_hs) > 0:
            mess = _("les hotes suivants sont HS : \n") + ip_hs
            var.q.put(lambda: threading.Thread(target=design.alert, args=(mess,)).start())
        if len(ip_ok) > 0:
            mess = _("les hotes suivants sont OK : \n") + ip_ok
            var.q.put(lambda: threading.Thread(target=design.alert, args=(mess,)).start())
        ip_hs = ""
        ip_ok = ""
    except Exception as inst:
        design.logs("fct_thread--" + str(inst))


############################################################################################
#####	Alertes mails															       #####
############################################################################################
def mail():
    # time.sleep(10)
    try:
        erase = ()
        ip_hs1 = ""
        ip_ok1 = ""
        mess = 0
        message = _("""\
		Bonjour,<br><br>
		<table border=1><tr><td width='50%' align=center>Nom</td><td width='50%' align=center>IP</td></tr>
		""")
        sujet = _("Alerte sur le site ") + var.nom_site
        time.sleep(1)
        for key1, value1 in var.liste_mail.items():
            if int(value1) == int(var.envoie_alert):
                nom = design.lire_nom(key1)
                p1 = "<tr><td align=center>" + nom + "</td><td bgcolor=" + var.couleur_noir + " align=center>" + key1 + "</td></tr>"
                ip_hs1 = ip_hs1 + p1
                var.liste_mail[key1] = 10

            elif value1 == 20:
                nom = design.lire_nom(key1)
                p1 = "<tr><td align=center>" + nom + "</td><td bgcolor=" + var.couleur_vert + " align=center>" + key1 + "</td></tr>"
                ip_ok1 = ip_ok1 + p1
                erase = erase + (str(key1),)
        for cle in erase:
            try:
                del var.liste_mail[cle]
            except Exception as inst:
                design.logs("fct_thread--" + str(inst))

        if len(ip_hs1) > 0:
            mess = 1
            message = message + _("""\
			Les hôtes suivants sont <font color=red>HS</font><br>""") + ip_hs1 + _("""\
			</table><br><br>
			Cordialement,
			""")

        if len(ip_ok1) > 0:
            mess = 1
            message = message + _("""\
			Les hôtes suivants sont <font color=green>revenus</font><br>""") + ip_ok1 + _("""\
			</table><br><br>
			Cordialement,
			""")
        if mess == 1:
            threading.Thread(target=fct_thread_mail.envoie_mail, args=(message, sujet)).start()
            mess = 0
        ip_hs = ""
        ip_ok = ""
    except Exception as inst:
        design.logs("fct_thread--" + str(inst))


############################################################################################
#####	Alertes Télégram														       #####
############################################################################################
def telegram():
    try:
        erase = ()
        ip_hs1 = ""
        ip_ok1 = ""
        mess = 0
        message = _("Alerte sur le site ") + var.nom_site + "\n \n"
        sujet = _("Alerte sur le site ") + var.nom_site
        time.sleep(1)
        for key1, value1 in var.liste_telegram.items():
            if int(value1) == int(var.envoie_alert):
                nom = design.lire_nom(key1)
                p1 = "" + nom + " : " + key1 + "\n"
                ip_hs1 = ip_hs1 + p1
                var.liste_telegram[key1] = 10

            elif value1 == 20:
                nom = design.lire_nom(key1)
                p1 = "" + nom + " : " + key1 + "\n"
                ip_ok1 = ip_ok1 + p1
                erase = erase + (str(key1),)
        for cle in erase:
            try:
                del var.liste_telegram[cle]
            except:
                pass

        if len(ip_hs1) > 0:
            mess = 1
            message = message + _("""\
							Les hôtes suivants sont HS \n""") + ip_hs1

        if len(ip_ok1) > 0:
            mess = 1
            message = message + _("""\
							Les hôtes suivants sont revenus \n""") + ip_ok1
        if mess == 1:
            threading.Thread(target=thread_telegram.main, args=(message,)).start()
            mess = 0
        ip_hs = ""
        ip_ok = ""
    except Exception as inst:
        design.logs("fct_thread--" + str(inst))

def recapmail():
    recap.main()