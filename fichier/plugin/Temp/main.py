from tkinter.messagebox import showinfo
import fichier.thread_telegram as tel
import fichier.plugin.Temp.fct as fct
import time
import threading
import fichier.var as var
import fichier.plugin.Temp.param as param
from tkinter import *

version = "0.0.3"


def alert(message):
    showinfo("alerte", message)


def temp(mail, popup, telegram):
    while True:
        print(mail + popup + telegram)
        tempGpu = fct.getTtemp("GPU Core")
        tempCpu = fct.getTtemp("CPU Package")
        tempMaxCpu = param.tempMaxCpu

        """try:
            #var.q.put(lambda: var.lab_tempCpu.config(text=str("CPU= " + str(tempCpu) + " / GPU= " + str(tempGpu))))
        except Exception as e:
            print(e)
        """
        tCpu = 0
        tGpu = 0
        try:
            tCpu1 = str(tempCpu).split(".")
            tCpu = int(tCpu1[0])
            var.q.put(lambda: Label(master=var.app_instance.frame_bas, bg=var.bg_frame_haut,
                                    text=_("Temp CPU ") + str(tCpu)).grid(row=0, column=3, padx=5, pady=5))

        except:
            pass
        try:
            tGpu1 = str(tempGpu).split(".")
            tGpu = int(tGpu1[0])
            print("001")
            var.q.put(lambda: Label(master=var.app_instance.frame_bas, bg=var.bg_frame_haut,
                                    text=_("Temp GPU ") + str(tGpu)).grid(row=0, column=4, padx=5, pady=5))
        except:
            pass
        print(tCpu)
        print(tGpu)
        print(tempMaxCpu)
        #if tCpu > int(tempMaxCpu) or tGpu > int(tempMaxCpu):
        if tCpu > int(tempMaxCpu):
            print("Alert")
            if mail == '1':
                if param.mail_envoi == 0:
                    param.mail_envoi = 1

            if param.popup == '1':
                if param.popup_envoi == 0:
                    var.q.put(lambda: threading.Thread(target=alert, args=("La temperature est de " + str(tempCpu),)).start())
                    param.popup_envoi = 1

            if telegram == '1':
                print("tel")
                if param.telegram_envoi == 0:
                    print("tel1")
                    var.q.put(lambda: threading.Thread(target=tel.main, args=("Site de "+str(var.nom_site)+" - La temperature est de " + str(tempCpu),)).start())
                    param.telegram_envoi = 1

        else:
            param.popup_envoi = 0
            param.telegram_envoi = 0
            param.mail_envoi = 0

        time.sleep(5)


def lancer(mail1, popup1, telegram1):
    fct.lanceopen()
    time.sleep(4)
    threading.Thread(target=temp, args=(mail1, popup1, telegram1)).start()


def main():
    param.main()
