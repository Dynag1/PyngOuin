from tkinter import *
import fichier.var as var
import pickle
import os.path
import threading
import fichier.design as design


def lire_param_db():
	try:
		fichierini = "tab4"
		if os.path.isfile(fichierini):
			fichierSauvegarde = open(fichierini,"rb")
			variables = pickle.load(fichierSauvegarde)
			fichierSauvegarde.close()

			#Affichage de la liste
			return variables
		else:
			#Le fichier n'existe pas
			print("Fichier " + fichierini + " non trouvé")
	except Exception as inst:
		design.logs("param_db - " + str(inst))




def save_param_db():
	try:
		param_delais = var.delais
		param_nbr_hs = var.envoie_alert
		param_popup = var.popup
		param_mail = var.mail
		param_telegram = var.telegram
		param_mail_recap = var.recap
		param_db_ext = var.db
		variables = [param_delais, param_nbr_hs, param_popup, param_mail, param_telegram, param_mail_recap, param_db_ext]
		try:
			fichierSauvegarde = open("tab4","wb")
			pickle.dump(variables, fichierSauvegarde)
			fichierSauvegarde.close()
		except Exception as inst:
			design.logs(str(inst))
		return
	except Exception as inst:
		design.logs("param_db - " + str(inst))



	

	




