import logging
logging.basicConfig(level=logging.INFO) # , filename="log.txt"
log = logging.getLogger("mainlog")

debug_mode = False
debug_sleep_time = 0.5
debug_offset = 25


#guard vars and consts
SECRETS_FOLDER = "secrets/"
FILENAME = "secrets.json"
secrets_list = []
tfa_list = []
last_update = 0
user_list = ["----"]
UNKNOWN_USER = "#UNKNOWN_USER"
INTERVAL = 1

# colors
OUTLINE_BG = "slate gray"
MAINFRAME_BG = "gray14"
UPLABEL = "deep sky blue"
CODEFRAME_BG = "gray8"
CODELABEL = "green1"
CODELABEL_CRIT = "orange red"
CODELABEL_UPD = "deep sky blue"
CODELABEL_WARN = "yellow2"
PROGRESSBAR_BG = "green1"
PROGRESSBAR_CRT_BG = "red2"
PROGRESSBAR_WARN_BG = "yellow"
PROGRESSBAR_UPD_BG = "deep sky blue"
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

# sizes and outlines
SIZEW = 300
SIZEH = 350
ALPHA = 0.95
MF_LOC = 0.01