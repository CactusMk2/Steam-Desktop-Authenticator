from steam.guard import SteamAuthenticator
import json
from pyperclip import copy
import os
import binascii
import colorama as clr
clr.init()

SECRETS_FOLDER = "secrets/"
FILENAME = "secrets.json"
secrets_list = []
UNKNOWN_USER = "#UNKNOWN_USER"

def exit_with_error(error_text):
	print(clr.Fore.RED+error_text+clr.Fore.RESET)
	input("Hit enter to exit")
	exit()

def show_error(error_text):
	print(clr.Fore.RED+error_text+clr.Fore.RESET)
	input("Hit enter to continue")


def get_code(auth):
	try:
		code = auth.get_code()
	except AttributeError as er:
		user = auth.secrets.get("account_name",UNKNOWN_USER)
		exit_with_error(f"Secrets file for {user} is corrupted: {er}")
	except binascii.Error as er:
		user = auth.secrets.get("account_name")
		exit_with_error(f"Secrets file for {user} is corrupted: {er}")
	else:
		return code

def show_users(secrets_list):
	for index, user_secret in enumerate(secrets_list):
		user_name = user_secret.get("account_name",UNKNOWN_USER)
		print(str(index+1)+")",clr.Fore.CYAN+user_name+clr.Fore.RESET)


if not os.path.isdir(SECRETS_FOLDER):
	SECRETS_FOLDER = "./"
for _, _, files in os.walk(SECRETS_FOLDER):
	for file in files:
		with open(SECRETS_FOLDER+file,"r") as f:
			try:
				secrets = json.loads(f.read())
			except:
				if file.split(".")[-1] == "json":
					show_error(f"{file} skipped: file is corrupted")
			else:
				secrets_list.append(secrets)
if not len(secrets_list):
	exit_with_error("No secrets files found")


show_users(secrets_list)

try: user_index = int(input("\nChoose number: ")) - 1
except:
	exit()
secrets = secrets_list[user_index]
if not secrets:
	exit_with_error("Secrets for specified user wasn't found")

	
auth = SteamAuthenticator(secrets)
code = get_code(auth)


print("User: ",clr.Fore.CYAN+secrets.get("account_name",UNKNOWN_USER)+clr.Fore.RESET)
print(f"\n2FA CODE: {clr.Fore.GREEN+code+clr.Fore.RESET}")
copy(code)
input("Hit enter to exit")
exit()