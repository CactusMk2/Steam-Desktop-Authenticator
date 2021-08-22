from config import *
log.debug("Starting app")
import json
from pyperclip import copy
from tkinter import ttk
import tkinter as tk
import time
import threading
from pathlib import Path
from customs import *

if debug_mode:
	log.warning("Engaged debug mode!")

def copy_code():
	global code
	copy(code)

def add_account():
	global tfa_type_new
	if debug_mode:
		result = 85
	else:
		client = SteamClient()
		log.debug("first login")
		result = client.login(setup_login, setup_password).value
	if result == 5:
		show_error("Invalid password")
		return
	elif result == 84:
		show_error("Try again later")
		return
	elif result == 85 or result == 63:
		tfa_type_new = result
		log.debug("w/o tfa failed")
		setup.setup_account_btn.configure(command=add_account_tfa)
		setup.tfa_entry.place(anchor="w", rely=0.55, height=30,)
		setup.tfa_up_label.place(anchor="n",relx=0.5, rely=0.1)
	elif not client.logged_on:
		show_error("Unknown error at first login")
		return
	else:
		setup_new_account(client)


def add_account_tfa():
	if debug_mode:
		setup.destroy()
		setup_new_account("lol")
		return
	client = SteamClient()
	log.debug("login w tfa")
	if tfa_type_new == 85:
		log.info("logging with mobile")
		result = client.login(setup_login, setup_password, two_factor_code=setup_tfa).value
	elif tfa_type_new == 63:
		log.info("logging with email")
		result = client.login(setup_login, setup_password, auth_code=setup_tfa).value
	else:
		show_error("Wrong tfa type")
		return
	print(result)
	if result == 88:
		show_error("Wrong tfa")
	elif result == 5:
		show_error("Invalid password")
		return
	elif result == 84:
		show_error("Try again later")
		return
	elif result == 85:
		show_error("Enter tfa")
		return
	elif not client.logged_on:
		show_error("Some error")
		return
	else:
		setup_new_account(client)


def setup_new_account(client):
	global new_auth
	global new_secrets
	if not client.logged_on:
		show_error("Client not logged on while setup")
		return
	open_addacc()
	setup.destroy()
	if debug_mode:
		print("logged in")
		new_auth = "debug"
		return
	new_auth = SteamAuthenticator(backend=client)
	try:
		log.info("adding tfa")
		new_auth.add()
	except SteamAuthenticatorError:
		show_error("TFA already exists")
		addacc.destroy()
		return
	except:
		show_error("Unknown error error")
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
		show_error("Input sms code")
		return
	try:
		new_auth.finalize(add_smscode)
	except:
		show_error("Error while finalizing")
		return
	username = new_secrets.get("account_name",UNKNOWN_USER)
	with open(SECRETS_FOLDER+username+".json", "w") as f:
		json.dump(new_secrets, f)

	log.debug("updating info about all 2FAs")
	get_all_secrets()
	user_list = update_user_list(secrets_list)
	get_last_update()
	addacc.destroy()


def open_setup():
	global setup
	log.debug("setup opened")
	setup = Setup_account(root, f"{SIZEW}x{SIZEH}-{POSW-SIZEW}-{POSH}")
	setup.setup_account_btn.configure(command=add_account)
	setup.grab_set()


def open_addacc():
	global addacc
	log.debug("addacc opened")
	addacc = Add_account(root, f"{SIZEW}x{SIZEH}-{POSW-SIZEW}-{POSH}")
	addacc.ok_btn.configure(command=finalize_new_account)
	addacc.grab_set()


def update_user_list(secrets_list):
	global user_list
	log.debug("updating users list")
	user_list = []
	for index, user_secret in enumerate(secrets_list):
		user_list.append(user_secret.get("account_name",UNKNOWN_USER))
	return user_list


#getting all secrets
def get_all_secrets():
	global secrets_list
	log.debug("updating secrets")
	all_secrets = extract_secrets_from_folder(SECRETS_FOLDER)
	if all_secrets:
		secrets_list = all_secrets
	else:
		return


def get_tfa_list(secrets_list):
	global tfa_list
	log.debug("getting tfa list")
	tfa_list = []
	for secrets in secrets_list:
		usern = secrets.get("account_name")
		log.info(f"Getting tfa for {usern}")
		code = get_code(secrets)
		tfa_list.append(code)


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

log.info("rendering main window")


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

def on_root_closing():
	root.destroy()
	exit()
root.protocol("WM_DELETE_WINDOW", on_root_closing)


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


log.info("starting steam API")
log.debug("Importing SteamClient")
from steam.client import SteamClient
log.debug("Importing SteamAuthenticator")
from steam.guard import SteamAuthenticator, SteamAuthenticatorError
from utils import *

setup = False
addacc = False
get_all_secrets()

if not len(secrets_list):
	log.debug("stuck in waiting for first tfa to appear loop")
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
	while getattr(loop, "do_run", True):
		if not (int(time.time()) + 1) - last_update > 30:
			time.sleep(1)
		
		if progresstime > 29:
			loop.updating = True
			last_update = int(time.time())
			get_tfa_list(secrets_list)
			progress = 0
			loop.updating = False
		pass
	pass
		

progresstime = time.time() - last_update
progress = progresstime // 0.3

get_tfa_list(secrets_list)
user_list = update_user_list(secrets_list)
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
		
