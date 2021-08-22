from config import *
from win10toast import ToastNotifier
from random import randint
from steam.guard import SteamAuthenticator
import binascii
from time import sleep
import os
import json

def exit_with_error(error_text):
	log.critical(error_text)
	toast = ToastNotifier()
	toast.show_toast("Fatal Error", error_text, duration=3)
	exit()

def show_error(error_text):
	log.warning(error_text)
	toast = ToastNotifier()
	toast.show_toast("Error", error_text, duration=2, threaded=True)

def get_code(secrets, offset=0):
	if debug_mode:
		code = randint(10000,99999)
		log.debug(f"sleeping {debug_sleep_time}")
		sleep(debug_sleep_time)
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

def get_code_by_username(acc_var, tfa_list, user_list):
	username = acc_var.get()
	index = user_list.index(username)
	return tfa_list[index]

def extract_secrets_from_folder(secrets_folder):
	secrets_list = []
	if not os.path.isdir(secrets_folder):
		return False
	index = 0
	log.debug("looking for secrets, getting files")
	for _, dirs, files in os.walk(secrets_folder):
		for file in files:
			log.debug(f"FILE - {file}")
			with open(secrets_folder+file,"r") as f:
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
	return secrets_list