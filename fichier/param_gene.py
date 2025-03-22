import uuid
from tkinter import *
from fichier import var, design, lic
import pickle
import os.path

fichierini = "tabG"
"""
check_popup1 = IntVar()
check_mail1 = IntVar()
check_recap1 = IntVar()

popup = False
mail = False
recap = False
"""
licence = ""
def lire_param_gene():
	try:
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
		design.logs("param_gene - "+str(inst))


def nom_site():
	try:
		param = lire_param_gene()
		var.nom_site=param[0]
		var.l = param[1]
		print(param[0])
	except Exception as inst:
		design.logs("param_gene - "+str(inst))
		return


def main():

	def save_param_gene():
		param_site = ent0.get()
		param_li = ent2.get()
		variables = [param_site, param_li]
		try:
			fichierSauvegarde = open(fichierini,"wb")
			pickle.dump(variables, fichierSauvegarde)
			fichierSauvegarde.close()
		except Exception as inst:
			design.logs("param_gene - "+str(inst))
		fenetre1.destroy()
		return
	def lire():
		try:
			variables=lire_param_gene()
			licence = variables[1]
			ent0.insert(0, variables[0])
			#ent1.insert(0, variables[1])
			ent2.insert(0, variables[1])

		except Exception as inst:
			design.logs("param_gene - "+str(inst))
			return

	fenetre1 = Toplevel()
	fenetre1.title("Paramètres généraux")
	fenetre1.geometry("400x400")
	frame_haut = Frame(master=fenetre1, height=50, bg=var.bg_frame_mid, padx=5, pady=5)
	frame_haut.pack(fill=X)

	lab0 = Label(master=frame_haut, text=_("Nom du site"), bg=var.bg_frame_mid).grid(row=0, column=0, padx=5, pady=5, sticky = 'w')
	ent0 = Entry(frame_haut, text="")
	ent0.grid(row=0, column=1, padx=5, pady=5, sticky = 'w')

	var.code = lic.generate_activation_code()
	print(var.code)
	lab1 = Label(master=frame_haut, text=_("Code"), bg=var.bg_frame_mid).grid(row=1, column=0, padx=5, pady=5,
																				  sticky='w')
	ent1 = Entry(frame_haut, text="")
	ent1.grid(row=1, column=1, padx=5, pady=5, sticky='w')
	ent1.insert(0, var.code)

	lab2 = Label(master=frame_haut, text=_("Licence"), bg=var.bg_frame_mid).grid(row=2, column=0, padx=5, pady=5,
																				  sticky='w')
	ent2 = Entry(frame_haut, text="")
	ent2.grid(row=2, column=1, padx=5, pady=5, sticky='w')

	print(lic.verify_license())

	if lic.verify_license() == True:
		Licence = _("Licence Valide")
	else:
		Licence = _("Licence Non Valide")
	Label(master=frame_haut, text=Licence, bg=var.bg_frame_mid).grid(row=3, columnspan=2, padx=5, pady=5,
																	   sticky='w')

	but_ip = Button(frame_haut, text=_('Valider'), padx=10, command=save_param_gene).grid(row=6, columnspan=2, pady=5)
	lire()
	try:
		fenetre1.mainloop()
	except Exception as inst:
		design.logs("param_gene - "+str(inst))
	

	




