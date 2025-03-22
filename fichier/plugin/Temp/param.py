from tkinter import * 
import fichier.var as var
import fichier.design as design
import fichier.plugin.Temp.main as a
import fichier.plugin.Temp.param as param


popup_envoi = 0
mail_envoi = 0
telegram_envoi = 0
tempMaxCpu = 60

mail = 0
popup = 0
telegram = 0

def main():
	def save_param_mail():
		param.mail = ent0.get()
		param.popup = ent1.get()
		param.telegram = ent3.get()
		temp = ent4.get()
		param.tempMaxCpu = int(temp)
		print(mail+popup+telegram)

		a.lancer(mail, popup, telegram)
		fenetre1.destroy()
		return

	fenetre1 = Toplevel()
	fenetre1.title("Paramètres")
	fenetre1.geometry("400x400")
	frame_haut = Frame(master=fenetre1, height=50, bg=var.bg_frame_mid, padx=5, pady=5)
	frame_haut.pack(fill=X)

	Label(master=frame_haut, text="Version "+a.version, bg=var.bg_frame_mid).grid(row=0, columnspan=2, padx=5, pady=5, sticky='w')


	Label(master=frame_haut, text="Envoie mail", bg=var.bg_frame_mid).grid(row=1, column=0, padx=5, pady=5, sticky = 'w')
	ent0 = Entry(frame_haut, text="")
	ent0.insert(0, '0')
	ent0.grid(row=1, column=2, padx=5, pady=5, sticky = 'w')

	Label(master=frame_haut, text="Popup", bg=var.bg_frame_mid).grid(row=2, column=0, padx=5, pady=5, sticky = 'w')
	ent1 = Entry(frame_haut, text="")
	ent1.insert(0, '0')
	ent1.grid(row=2, column=2, padx=5, pady=5, sticky = 'w')

	Label(master=frame_haut, text="Telegram", bg=var.bg_frame_mid).grid(row=3, column=0, padx=5, pady=5, sticky = 'w')
	ent3 = Entry(frame_haut, text="")
	ent3.insert(0, '0')
	ent3.grid(row=3, column=2, padx=5, pady=5, sticky = 'w')

	Label(master=frame_haut, text="Température", bg=var.bg_frame_mid).grid(row=4, column=0, padx=5, pady=5, sticky='w')
	ent4 = Entry(frame_haut, text="")
	ent4.insert(0, '60')
	ent4.grid(row=4, column=2, padx=5, pady=5, sticky='w')




	but_ip = Button(frame_haut, text='Valider', padx=10, command=save_param_mail).grid(row=6, columnspan=2, pady=5)
	try:
		fenetre1.mainloop()
	except Exception as inst:
		design.logs("mail-"+str(inst))
		pass
	

	




