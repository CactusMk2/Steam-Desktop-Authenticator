from config import *
log.debug("Importing SteamClient")
from steam.client import SteamClient
log.debug("Importing SteamAuthenticator")
from steam.guard import SteamAuthenticator, SteamAuthenticatorError
log.debug("Importing other libraries")
import json
from pyperclip import copy
import os
import binascii
from tkinter import ttk
import tkinter as tk
from datetime import datetime
import time
import threading
from win10toast import ToastNotifier
from random import randint
from pathlib import Path

root = tk.Tk()

if debug_mode:
	log.info("Engaged debug mode!")


#custom progress bar as a frame
class Custombar(tk.Frame):
	start_pos = 0
	end_pos = 100
	one_percent = 1
	def set_positions(self, start_pos=0, end_pos=100, width=50):
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.one_percent = self.end_pos / 100
		self.configure(width=width)

	def set_progress(self, progress):
		if progress > 100:
			progress=100
		if progress < self.start_pos:
			progress=self.start_pos

		self.width = progress * self.one_percent
		self.configure(width=self.width)



class Setup_account(tk.Toplevel):
	login_var = "None"
	password_var = "None"
	tfa_var = "None"
	is_up = True
	tfa_entry = None
	tfa_up_label = None
	setup_account_btn = None
	def on_closing(self):
		self.is_up = False
		self.destroy()
	def __init__(self, parent):
		super().__init__(parent)
		self.geometry(f"{SIZEW}x{SIZEH}-{POSW-SIZEW}-{POSH}")
		self.resizable(False, False)
		self.attributes(
			# '-topmost', 1,
			'-alpha', ALPHA,
			'-toolwindow', True)
		self.configure(bg=OUTLINE_BG)
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.is_up = True

		#frames
		setup_mainframe = tk.Frame(
			self,
			relief=tk.FLAT,
			bg=MAINFRAME_BG)
		setup_mainframe.place(relx=MF_LOC, rely=MF_LOC, relwidth=0.98, relheight=0.98)

		login_frame = tk.Frame(
			setup_mainframe,
			relief=tk.FLAT,
			width=275,
			height=120,
			bg=MAINFRAME_BG
			)

		tfa_frame = tk.Frame(
			setup_mainframe,
			relief=tk.FLAT,
			width=275,
			height=120,
			bg=MAINFRAME_BG
			)

		#widgets
		setup_up_label = tk.Label(
			setup_mainframe,
			text="Setup new account",
			bg=MAINFRAME_BG,
			fg=UPLABEL,
			font=("Arial", 16)
			)

		self.login_var = tk.StringVar()
		login_entry = tk.Entry(
			login_frame,
			relief=tk.FLAT,
			textvariable=self.login_var,
			bg=LOGIN_BG,
			fg=LOGIN,
			justify="left",
			width=275,
			font=("Impact", 20),
			selectbackground=SELECTED_LOGIN,
			selectforeground=LOGIN
			)

		self.password_var = tk.StringVar()
		password_entry = tk.Entry(
			login_frame,
			relief=tk.FLAT,
			textvariable=self.password_var,
			bg=LOGIN_BG,
			fg=LOGIN,
			justify="left",
			width=275,
			font=("Impact", 20),
			selectbackground=SELECTED_LOGIN,
			selectforeground=LOGIN,
			show="*"
			)


		self.setup_account_btn = tk.Button(
			setup_mainframe,
			relief=tk.FLAT,
			text="Setup new account",
			bg=SETUP_BTN_BG,
			fg=SETUP_BTN,
			activebackground=SETUP_BTN_ACTIVE_BG,
			activeforeground=SETUP_BTN_ACTIVE,
			font = ("Impact", 22),
			command=add_account
			)

		self.tfa_up_label = tk.Label(
			tfa_frame,
			text="Enter 2FA or email code",
			bg=MAINFRAME_BG,
			fg=UPLABEL,
			font=("Arial", 16)
			)

		self.tfa_var = tk.StringVar()
		self.tfa_entry = tk.Entry(
			tfa_frame,
			relief=tk.FLAT,
			textvariable=self.tfa_var,
			bg="black",
			fg=CODELABEL,
			justify="left",
			width=275,
			font=("Arial", 18),
			selectbackground=SELECTED_LOGIN,
			selectforeground=LOGIN,
			insertbackground="white"

			)


		self.password_var.set("tussca007")
		self.login_var.set("lethal_industrie15@hotmail.com")

		setup_up_label.pack()
		login_frame.pack()
		login_entry.place(anchor="w",rely=0.3,height=35)
		password_entry.place(anchor="w", rely=0.8, height=35)
		tfa_frame.pack()
		# self.tfa_entry.place(anchor="w", rely=0.55, height=30,)
		# self.tfa_up_label.place(anchor="n",relx=0.5, rely=0.1)

		self.setup_account_btn.place(anchor="s",rely=0.97, relx=0.5, height=40, width=260)



class Add_account(tk.Toplevel):

	def on_closing(self):
			self.is_up = False
			self.destroy()
	smscode_entry_var = None
	is_up = True	

	def __init__(self, parent):
		

		super().__init__(parent)
		self.geometry(f"{SIZEW}x{SIZEH}-{POSW-SIZEW}-{POSH}")
		self.resizable(False, False)
		self.attributes(
			# '-topmost', 1,
			'-alpha', ALPHA,
			'-toolwindow', True)
		self.configure(bg=OUTLINE_BG)
		self.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.is_up = True

		add_account_mainframe = tk.Frame(
			self,
			relief=tk.FLAT,
			bg=MAINFRAME_BG)
		add_account_mainframe.place(relx=MF_LOC, rely=MF_LOC, relwidth=0.98, relheight=0.98)

		up_smslabel = tk.Label(
			add_account_mainframe,
			text="Enter SMS code\nyou just received",
			bg=MAINFRAME_BG,
			fg=SMSLABEL,
			font=("Arial", 24))

		self.smscode_entry_var = tk.StringVar()
		smscode_entry = tk.Entry(
			add_account_mainframe,
			textvariable=self.smscode_entry_var,
			bg=SMSLABEL,
			fg="black",
			justify="center",
			width=200,
			font=("Arial", 22),
			selectbackground="black",
			selectforeground=SMSLABEL
			)

		ok_btn = tk.Button(
			add_account_mainframe,
			text="OK",
			bg=SMSLABEL,
			fg="black",
			activebackground=OK_BTN_ACTIVE_BG,
			activeforeground=OK_BTN_ACTIVE,
			font=("Arial", 24),
			command=finalize_new_account
			)

		up_smslabel.place(anchor="center", relx=0.5, rely=0.3)
		smscode_entry.place(anchor="center", relx=0.5, rely=0.55, width=200)
		ok_btn.place(anchor="center", relx=0.5, rely=0.75, width=100, height=40)



def add_account():
	global tfa_type_new
	if debug_mode:
		result = 85
	else:
		log.debug("starting client first")
		client = SteamClient()
		log.debug("first login first")
		result = client.login(setup_login, setup_password).value
	if result == 5:
		show_error("Invalid password")
		return
	elif result == 84:
		show_error("try again later")
		return
	elif result == 85 or result == 63:
		tfa_type_new = result
		log.debug("w/o tfa failed")
		setup.setup_account_btn.configure(command=add_account_tfa)
		setup.tfa_entry.place(anchor="w", rely=0.55, height=30,)
		setup.tfa_up_label.place(anchor="n",relx=0.5, rely=0.1)
	elif not client.logged_on:
		show_error("some error")
		return
	else:
		setup.destroy()
		setup_new_account(client)

def add_account_tfa():
	if debug_mode:
		setup.destroy()
		setup_new_account("lol")
		return

	log.debug("starting client w tfa")
	client = SteamClient()
	log.debug("login w tfa")
	print(setup_login)
	print(setup_password)
	print(setup_tfa)
	if tfa_type_new == 85:
		result = client.login(setup_login, setup_password, two_factor_code=setup_tfa).value
	elif tfa_type_new == 63:
		result = client.login(setup_login, setup_password, auth_code=setup_tfa).value
	else:
		show_error("wrong tfa type")
		return
	print(result)
	if result == 88:
		show_error("wrong tfa")
	elif result == 5:
		show_error("Invalid password")
		return
	elif result == 84:
		show_error("try again later")
		return
	elif not client.logged_on:
		show_error("some error")
		return
	else:
		setup.destroy()
		setup_new_account(client)


def setup_new_account(client):
	global new_auth
	global new_secrets
	open_addacc()
	if debug_mode:
		print("logged in")
		new_auth = "debug"
		return
	new_auth = SteamAuthenticator(backend=client)
	try:
		new_auth.add()
	except SteamAuthenticatorError:
		show_error("TFA already exists")
		addacc.destroy()
		return
	except:
		show_error("some error")
		addacc.destroy()
		return
	print(new_auth.secrets)
	new_secrets = new_auth.secrets

def finalize_new_account():
	Path(SECRETS_FOLDER).mkdir(parents=True, exist_ok=True)
	if new_auth == "debug":
		print("finalized")
		username = "debug"
		with open(SECRETS_FOLDER+username+".json", "w") as f:
			json.dump({"shared_secret":"debug", "account_name":"debug"}, f)
		get_all_secrets()
		user_list = update_user_list(secrets_list)
		get_last_update()
		addacc.destroy()
		return
	if add_smscode == "":
		show_error("input sms code")
	answer = new_auth.finalize(add_smscode)
	print(answer)
	username = new_secrets.get("account_name",UNKNOWN_USER)
	with open(SECRETS_FOLDER+username+".json", "w") as f:
		json.dump(new_secrets, f)
	get_all_secrets()
	user_list = update_user_list(secrets_list)
	get_last_update()
	addacc.destroy()


def open_setup():
	global setup
	setup = Setup_account(root)
	setup.grab_set()

def open_addacc():
	global addacc
	addacc = Add_account(root)
	addacc.grab_set()


#guard functions
def exit_with_error(error_text):
	log.critical(error_text)
	toast = ToastNotifier()
	toast.show_toast("Fatal Error", error_text, duration=3)
	exit()


def show_error(error_text):
	log.warning(error_text)

def get_code(secrets, offset=0):
	if debug_mode:
		code = randint(10000,99999)
		log.debug(f"sleeping {debug_sleep_time}")
		time.sleep(debug_sleep_time)
		log.debug(f"returning {code}")
		return code

	auth = SteamAuthenticator(secrets)
	if offset:
		auth.steam_time_offset = offset
	try:
		code = auth.get_code()
	except AttributeError as er:
		user = auth.secrets.get("account_name",UNKNOWN_USER)
		show_error(f"Secrets file for {user} is corrupted: {er}")
		return "ERROR"
	except binascii.Error as er:
		user = auth.secrets.get("account_name")
		exit_with_error(f"Secrets file for {user} is corrupted: {er}")
	else:
		return code
	


def update_user_list(secrets_list):
	global user_list
	user_list = []
	for index, user_secret in enumerate(secrets_list):
		user_list.append(user_secret.get("account_name",UNKNOWN_USER))
	return user_list



def get_code_by_username(acc_var, tfa_list, user_list):
	username = acc_var.get()
	index = user_list.index(username)
	return tfa_list[index]


def get_tfa_list(secrets_list):
	global tfa_list
	tfa_list = []
	for secrets in secrets_list:
		usern = secrets.get("account_name")
		log.info(f"Getting tfa for {usern}")
		code = get_code(secrets)
		tfa_list.append(code)

def on_root_closing():
	root.destroy()
	exit()

def copy_code():
	global code
	copy(code)


# sizes
W = root.winfo_screenwidth() // 2
H = root.winfo_screenheight() // 2
POSW = W-(SIZEW//2)
POSH = H-(SIZEH//2)

#main window configuration
root.geometry(f"{SIZEW}x{SIZEH}-{POSW}-{POSH}")
root.resizable(False, False)
root.attributes(
	# '-topmost', 1,
	'-alpha', ALPHA,)
root.configure(bg=OUTLINE_BG)
root.title("Desktop Authenticator")
root.protocol("WM_DELETE_WINDOW", on_root_closing)



# creating frames
mainframe = tk.Frame(
	root,
	relief=tk.FLAT,
	bg=MAINFRAME_BG)
mainframe.place(relx=MF_LOC, rely=MF_LOC, relwidth=0.98, relheight=0.98)

uplabel_frame = tk.Frame(
	mainframe,
	relief=tk.FLAT,
	width=300,
	bg=MAINFRAME_BG,
	height=45
	)

progressbar_frame = tk.Frame(
	mainframe,
	relief=tk.FLAT,
	width=260,
	height=22,
	bg=MAINFRAME_BG,
	)

copy_btn_frame = tk.Frame(
	mainframe,
	relief=tk.FLAT,
	width=240,
	height=43,
	bg="white")

acc_frame = tk.Frame(
	mainframe,
	relief=tk.FLAT,
	width=240,
	height=43,
	bg=MAINFRAME_BG)

setup_frame = tk.Frame(
	mainframe,
	relief=tk.FLAT,
	width=240,
	height=43,
	bg="white"
	)


# creating widgets
up_label = tk.Label(
	uplabel_frame,
	text="Steam Guard Authenticator",
	bg=MAINFRAME_BG,
	fg=UPLABEL,
	height=1,
	font=("Arial", 16),)

code_var = tk.StringVar()
code_var.set("Loading")

code_entry = tk.Entry(
	mainframe,
	readonlybackground=CODEFRAME_BG,
	relief=tk.FLAT,
	textvariable=code_var,
	bg=CODEFRAME_BG,
	fg=CODELABEL,
	justify=tk.CENTER,
	width=260,
	font=("Impact", 50),
	selectbackground=SELECTED_CODE,
	selectforeground=CODELABEL
	)
code_entry.configure(state="readonly")


acc_lbl = tk.Label(
	acc_frame,
	text="Account:",
	bg=MAINFRAME_BG,
	fg=ACC_LBL,
	font=("Arial", 14))

acc_var = tk.StringVar()
acc_combo = ttk.Combobox(
	acc_frame,
	textvariable=acc_var,
	state="readonly")

acc_combo.configure(values="Loading")
acc_combo.current(0)


progressbar = Custombar(
	progressbar_frame,
	relief=tk.FLAT,
	width=260,
	bg=PROGRESSBAR_BG,)

copy_btn = tk.Button(
	copy_btn_frame,
	relief=tk.FLAT,
	text="Copy code",
	width=100,
	height=10,
	bg=COPY_BUTTON_BG,
	fg=COPY_BUTTON,
	activebackground=COPY_BUTTON_ACTIVE_BG,
	activeforeground=COPY_BUTTON_ACTIVE,
	font=("Impact", 32),
	command=copy_code)

exit_btn = tk.Button(
	mainframe,
	relief=tk.FLAT,
	text=u"\u274C",
	width=300,
	height=10,
	bg=EXITBTN_BG,
	fg=EXITBTN,
	activebackground=EXTBTN_ACT_BG,
	activeforeground=EXTBTN_ACT,
	command=root.destroy)

setup_btn = tk.Button(
	setup_frame,
	relief=tk.FLAT,
	text="Add new account",
	width=260,
	height=10,
	bg=COPY_BUTTON_BG,
	fg=COPY_BUTTON,
	activebackground=COPY_BUTTON_ACTIVE_BG,
	activeforeground=COPY_BUTTON_ACTIVE,
	font=("Impact", 20),
	command=open_setup
	)



# packing
uplabel_frame.pack(side="top")
up_label.place(relx=0.06,rely=0.05)
code_entry.pack(side="top", padx=15, ipady=10)
progressbar_frame.pack(side="top")
progressbar.place(anchor="w", height=10)
copy_btn_frame.pack(side="top")
copy_btn.place(anchor="center", rely=0.46, relx=0.5)
acc_frame.pack(side="top")
acc_lbl.place(relx=0, rely=0.5, anchor="w")
acc_combo.place(relx=1, rely=0.5, anchor="e", height=30)
setup_frame.pack(side="top")
setup_btn.place(width=260,anchor="w",rely=0.5)

exit_btn.place(anchor="center", width=300, height=30, relx = 0.5, rely=0.97)

progressbar.set_positions(0, 260, 0)
progressbar.set_progress(100)

root.update()




# first time initializing guard

#getting all secrets
def get_all_secrets():
	global secrets_list
	global SECRETS_FOLDER
	secrets_list = []
	if not os.path.isdir(SECRETS_FOLDER):
		return
	index = 0
	log.debug("looking for secrets, getting files")
	for _, dirs, files in os.walk(SECRETS_FOLDER):
		for file in files:
			log.debug(f"FILE - {file}")
			with open(SECRETS_FOLDER+file,"r") as f:
				try:
					secrets = json.loads(f.read())
				except:
					pass
				else:
					if secrets.get("shared_secret", False):
						secrets_list.append(secrets)
					else:
						user = secrets.get("account_name", False)
						if user:
							show_error(f"Secrets file for {user} is corrupted: no shared_secret key")
		break


def get_last_update():
	global last_update
	if debug_mode:
		last_update = int(time.time()) - debug_offset
		return
	code_entry.configure(fg=CODELABEL_UPD)
	code_var.set("Updating")
	progressbar.configure(bg=PROGRESSBAR_UPD_BG)
	#getting when was last update
	log.debug("looking for last update")
	tempcode = get_code(secrets_list[0])
	work = True
	while work:
		for i in range(1,30):
			# tempauth.steam_time_offset = i
			if tempcode != get_code(secrets_list[0], offset=i):
				offset = 30 - (i+1)
				last_update = int(time.time()) - offset
				work = False
				break
		else:
			log.info("Exit")
			last_update = int(time.time())
			work = False
			break

setup = False
addacc = False
get_all_secrets()
while True:
	if not len(secrets_list):
		root.update()
		acc_combo.configure(values="-----")
		acc_combo.current(0)
		code_entry.configure(fg=CODELABEL_WARN)
		code_var.set("-----")
		progressbar.configure(bg=PROGRESSBAR_WARN_BG)

		if getattr(setup, "is_up", False):
			setup_login = setup.login_var.get()
			setup_password = setup.password_var.get()
			setup_tfa = setup.tfa_var.get()	
		else:
			setup_login = "None"
			setup_password = "None"
			setup_tfa = "None"

		if getattr(addacc, "is_up", False):
			add_smscode = addacc.smscode_entry_var.get()
		else:
			add_smscode = "None"
		get_all_secrets()
	else:
		get_last_update()
		break	


# custom mainloop
def updater():
	global last_update
	global progress
	global progresstime
	global user_list
	while getattr(loop, "do_run", True):
		loop_now = int(time.time())
		if not (loop_now + 1) - last_update > 30:
			time.sleep(1)
		

		if progresstime > 29:
			loop.updating = True
			last_update = loop_now
			get_tfa_list(secrets_list)
			progress = 0
			loop.updating = False
		pass
	pass
		

progresstime = time.time() - last_update
progress = progresstime // 0.3

get_tfa_list(secrets_list)
log.debug("Updating userlist")
user_list = update_user_list(secrets_list)
setup = False
addacc = False
setup_login = "None"
setup_password = "None"
setup_tfa = "None"
add_smscode = "None"
acc_combo.configure(values=user_list)
acc_var.set(user_list[0])

loop = threading.Thread(target=updater)
loop.do_run = True
loop.updating = False
loop.start()

while True:
	acc_combo.configure(values=user_list)
	progresstime = time.time() - last_update
	progress = progresstime // 0.3

	if getattr(setup, "is_up", False):
		setup_login = setup.login_var.get()
		setup_password = setup.password_var.get()
		setup_tfa = setup.tfa_var.get()	
	else:
		setup_login = "None"
		setup_password = "None"
		setup_tfa = "None"

	if getattr(addacc, "is_up", False):
		add_smscode = addacc.smscode_entry_var.get()
	else:
		add_smscode = "None"
	# print(add_smscode)
	

	if not loop.updating:
		code = get_code_by_username(acc_var, tfa_list, user_list)
		code_var.set(code)
		progress_forbar = 100 - progress
	else:
		progress_forbar = 100
		code = "-----"
		code_var.set("Updating")

		
	username = acc_var.get()
	try:
		root.update()
		if loop.updating:
			code_entry.configure(fg=CODELABEL_UPD)
			progressbar.configure(bg=PROGRESSBAR_UPD_BG)
		elif progress > 80:		
			code_entry.configure(fg=CODELABEL_CRIT)
			progressbar.configure(bg=PROGRESSBAR_CRT_BG)
		elif progress > 65:
			code_entry.configure(fg=CODELABEL_WARN)
			progressbar.configure(bg=PROGRESSBAR_WARN_BG)
		else:
			progressbar.configure(bg=PROGRESSBAR_BG)
			code_entry.configure(fg=CODELABEL)

		progressbar.set_progress(progress_forbar)
		
	except tk.TclError:
		loop.do_run = False
		exit()
		
