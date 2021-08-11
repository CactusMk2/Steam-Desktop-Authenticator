from tkinter import *
from tkinter import ttk
class Custombar(Frame):
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


user_list = ["Account name","Account name 2"]

root = Tk()

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

#main window configuration
root.geometry(f"{SIZEW}x{SIZEH}-{POSW}-{POSH}")
root.overrideredirect(True)
root.resizable(False, False)
root.attributes(
	'-topmost', 1,
	'-alpha',ALPHA,)
root.configure(bg=OUTLINE_BG)


# creating frames
mainframe = Frame(
	root,
	relief=FLAT,
	bg=MAINFRAME_BG)
mainframe.place(relx=MF_LOC, rely=MF_LOC, relwidth=0.98, relheight=0.98)

uplabel_frame = Frame(
	mainframe,
	relief=FLAT,
	width=300,
	bg=MAINFRAME_BG,
	height=45
	)

progressbar_frame = Frame(
	mainframe,
	relief=FLAT,
	width=260,
	height=22,
	bg=MAINFRAME_BG,
	)

copy_btn_frame = Frame(
	mainframe,
	relief=FLAT,
	width=240,
	height=43,
	bg="white")

acc_frame = Frame(
	mainframe,
	relief=FLAT,
	width=240,
	height=43,
	bg=MAINFRAME_BG)
# end


# creating widgets
up_label = Label(
	uplabel_frame,
	text="Steam Guard Authenticator",
	bg=MAINFRAME_BG,
	fg=UPLABEL,
	height=1,
	font=("Arial", 16),)

code_var = StringVar()
code_entry = Entry(
	mainframe,
	readonlybackground=CODEFRAME_BG,
	relief=FLAT,
	textvariable=code_var,
	bg=CODEFRAME_BG,
	fg=CODELABEL,
	justify=CENTER,
	width=260,
	font=("Impact", 50),
	selectbackground=SELECTED_CODE,
	selectforeground=CODELABEL
	)
code_entry.configure(state="readonly")

acc_lbl = Label(
	acc_frame,
	text="Account:",
	bg=MAINFRAME_BG,
	fg=ACC_LBL,
	font=("Arial", 14))

acc_var = StringVar()
acc_combo = ttk.Combobox(
	acc_frame,
	textvariable=acc_var,
	state="readonly",
	values=user_list)
acc_combo.current(0)

progressbar = Custombar(
	progressbar_frame,
	relief=FLAT,
	width=260,
	bg=PROGRESSBAR_BG,)

copy_btn = Button(
	copy_btn_frame,
	relief=FLAT,
	text="Copy code",
	width=100,
	height=10,
	bg=COPY_BUTTON_BG,
	fg=COPY_BUTTON,
	activebackground=COPY_BUTTON_ACTIVE_BG,
	activeforeground=COPY_BUTTON_ACTIVE,
	font=("Impact", 32))

exit_btn = Button(
	mainframe,
	relief=FLAT,
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
acc_combo.place(relx=1, rely=0.5, anchor="e",)
exit_btn.place(anchor="center", width=300, height=30, relx = 0.5, rely=0.97)

progressbar.set_positions(0, 260, 0)
progressbar.set_progress(68)
# custom mainloop
def apploop():
	while True:
		# print(acc_var.get())
		try:
			root.update()
		except TclError:
			exit()

code_var.set("GHBW2")
apploop()
	