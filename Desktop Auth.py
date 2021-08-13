from steam.guard import SteamAuthenticator
import json
from pyperclip import copy
import os
import binascii
from tkinter import ttk
import tkinter as tk
from datetime import datetime
import time
import asyncio

print("starting tk")
root = tk.Tk()

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



#guard functions
def exit_with_error(error_text):
	print(error_text)
	input("Hit enter to exit")
	exit()


def show_error(error_text):
	print(error_text)

def get_code(secrets):
	auth = SteamAuthenticator(secrets)
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


async def get_tfa_list(secrets_list):
	global tfa_list
	tfa_list = []
	for secrets in secrets_list:
		usern = secrets.get("account_name")
		print(f"Getting tfa for {usern}")
		code = get_code(secrets)
		tfa_list.append(code)


def copy_code():
	global code_var
	code = code_var.get()
	copy(code)

#guard vars and consts
SECRETS_FOLDER = "secrets/"
FILENAME = "secrets.json"
secrets_list = []
tfa_list = []
last_update = 0
user_list = ["----"]
UNKNOWN_USER = "#UNKNOWN_USER"
INTERVAL = 1

# sizes and outlines
SIZEW = 300
SIZEH = 350
ALPHA = 0.95
MF_LOC = 0.01
W = root.winfo_screenwidth() // 2
H = root.winfo_screenheight() // 2
POSW = W-(SIZEW//2)
POSH = H-(SIZEH//2)

# colors
OUTLINE_BG = "slate gray"
MAINFRAME_BG = "gray14"
UPLABEL = "deep sky blue"
CODEFRAME_BG = "gray8"
CODELABEL = "green1"
PROGRESSBAR_BG = "green1"
SELECTED_CODE = "forest green"
CUR_BG = "white"
COPY_BUTTON_BG = "gray28"
COPY_BUTTON = "deep sky blue"
COPY_BUTTON_ACTIVE_BG="gray40"
COPY_BUTTON_ACTIVE="cyan2"
ACC_LBL = "deep sky blue"
EXITBTN="black"
EXITBTN_BG="firebrick1"
EXTBTN_ACT="black"
EXTBTN_ACT_BG="tomato"

# first time initializing guard

#getting all secrets
if not os.path.isdir(SECRETS_FOLDER):
	SECRETS_FOLDER = "./"
index = 0
print("looking for secrets, getting files")
for _, dirs, files in os.walk(SECRETS_FOLDER):
	for file in files:
		print(f"FILE - {file}")
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
if not len(secrets_list):
	exit_with_error("No secrets files found")

#getting when was last update
print("looking for last update")
tempauth = SteamAuthenticator(secrets_list[0])
tempcode = tempauth.get_code()
work = True
while work:
	for i in range(1,30):
		tempauth.steam_time_offset = i
		if tempcode != tempauth.get_code():
			offset = 30 - i
			last_update = int(time.time()) - offset
			work = False
			break
	else:
		last_update = int(time.time())
		work = False
		break



#main window configuration
root.geometry(f"{SIZEW}x{SIZEH}-{POSW}-{POSH}")
root.overrideredirect(True)
root.resizable(False, False)
root.attributes(
	'-topmost', 1,
	'-alpha',ALPHA,)
root.configure(bg=OUTLINE_BG)


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
# end


# creating widgets
up_label = tk.Label(
	uplabel_frame,
	text="Steam Guard Authenticator",
	bg=MAINFRAME_BG,
	fg=UPLABEL,
	height=1,
	font=("Arial", 16),)

code_var = tk.StringVar()
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
	state="readonly",
	values=user_list)
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
	command=root.destroy
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
exit_btn.place(anchor="center", width=300, height=30, relx = 0.5, rely=0.97)

progressbar.set_positions(0, 260, 0)
progressbar.set_progress(100)


# custom mainloop
async def apploop(loop):
	global last_update
	global tfa_list
	global user_list
	root.update()
	await get_tfa_list(secrets_list)
	print("Updating userlist")
	user_list = update_user_list(secrets_list)
	acc_combo.configure(values=user_list)
	acc_var.set(user_list[0])
	while True:
		task = loop.create_task(updater())
		progresstime = time.time() - last_update
		progress = progresstime // 0.3
		try:
			progressbar.set_progress(100-progress)
		except tk.TclError:
			pass
		if progresstime > 30:
			last_update = time.time()
			loop.create_task(get_tfa_list(secrets_list))
		code = get_code_by_username(acc_var, tfa_list, user_list)
		code_var.set(code)
		await task

async def updater():
	try:
		root.update()
	except tk.TclError:
		exit()


code_var.set("-----")

loop = asyncio.get_event_loop()
loop.run_until_complete(apploop(loop))


