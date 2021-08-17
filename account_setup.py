from steam.client import SteamClient
from steam.guard import SteamAuthenticator
import json
import logging
from win10toast import ToastNotifier
from tkinter import ttk
import tkinter as tk
log = logging.getLogger("log")

#CONST VARS
USERNAME_ASD = "lethal_industrie15@hotmail.com"
PASSWORD_ASD = "tussca007"

class 

def logggin(username_asd, password_asd):
	client = SteamClient()
	client.login(username_asd, password_asd)
	if not client.logged_on:
		while not client.logged_on:
			code = input("Enter moblile 2FA code: ")
			client.login(username_asd, password_asd, two_factor_code=code)
			if client.logged_on:
				break
			print("Wrong 2FA code")
