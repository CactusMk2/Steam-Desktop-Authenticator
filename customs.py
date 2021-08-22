import tkinter as tk
from config import *
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
	def __init__(self, parent, geometry_setup):
		super().__init__(parent)
		self.geometry(geometry_setup)
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


		self.password_var.set(" Login")
		self.login_var.set("Password")

		setup_up_label.pack()
		login_frame.pack()
		login_entry.place(anchor="w",rely=0.3,height=35)
		password_entry.place(anchor="w", rely=0.8, height=35)
		tfa_frame.pack()
		# self.tfa_entry.place(anchor="w", rely=0.55, height=30,)
		# self.tfa_up_label.place(anchor="n",relx=0.5, rely=0.1)

		self.setup_account_btn.place(anchor="s",rely=0.97, relx=0.5, height=40, width=260)

class Add_account(tk.Toplevel):
	smscode_entry_var = None
	is_up = True
	ok_btn = None
	
	def on_closing(self):
		self.is_up = False
		self.destroy()
	
	def __init__(self, parent, geometry_setup):

		super().__init__(parent)
		self.geometry(geometry_setup)
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

		self.ok_btn = tk.Button(
			add_account_mainframe,
			text="OK",
			bg=SMSLABEL,
			fg="black",
			activebackground=OK_BTN_ACTIVE_BG,
			activeforeground=OK_BTN_ACTIVE,
			font=("Arial", 24),
			)

		up_smslabel.place(anchor="center", relx=0.5, rely=0.3)
		smscode_entry.place(anchor="center", relx=0.5, rely=0.55, width=200)
		self.ok_btn.place(anchor="center", relx=0.5, rely=0.75, width=100, height=40)