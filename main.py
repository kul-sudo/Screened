from tkinter import BOTTOM, LEFT, RIGHT, TOP, Tk, Frame, BooleanVar, Button, Checkbutton, Label, PhotoImage
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
from win32api import GetSystemMetrics
from keyboard import add_hotkey, unhook_all_hotkeys
from screenshot import screenshot_function
from json import load
import common

with open('settings.json', 'r') as json_settings:
	data = load(json_settings)

data_window = data['window'][0] # All the data related to the window
data_shortcuts = data['shortcuts'][0] # All the data related to shortcuts

# Screenshot maintenance
def take_screenshot():
	global screenshot_taking
	if screenshot_taking is False:
		screenshot_taking = True
		unhook_all_hotkeys()
		screenshot_function()
		if shortcuts_on.get():
			add_shortcuts()
		screenshot_taking = False

def window_deiconfiying():
	if common.window.state() == 'withdrawn':
		common.window.deiconify()

# Adding shortcuts
def add_shortcuts():
	add_hotkey(data_shortcuts['take-screenshot'], take_screenshot) # Determining the shortcut for taking screenshots 
	add_hotkey(data_shortcuts['window-withdraw'], common.window.withdraw) # Determining the shortcut for hiding the window
	add_hotkey(data_shortcuts['window-deiconify'], window_deiconfiying) # Determining the shortcut for show the window

# Handling shortcuts toggling
def shortcuts_toggle():
	if shortcuts_on.get(): # Check if the shortcuts checkbox is checked
		add_shortcuts()
	else: # Unhooking all of the shortcuts if the shortcuts checkbox is not checked
		unhook_all_hotkeys()

# Window creation & set window settings depending on the screen resolution
common.window = Tk()

BG_COLOR = data_window['bg-color']

common.window['bg'] = BG_COLOR # Window background
common.window.title(data_window['app-name']) # Window name

if GetSystemMetrics(0) == 1680 and GetSystemMetrics(1) == 1050: # Checking if the X of the window equals 1680 and Y equals 1050
	common.window.geometry(data_window['1680x1050-size'])
else:
	common.window.geometry(data_window['not-1680x1050-size'])
common.window.resizable(width=False, height=False) # Disabling the window resizability
common.window.iconphoto(False, PhotoImage(data=data_window['app-icon']))

# Top frame ('choose format' combobox and 'shortcuts' frame)
top_frame = Frame(master=common.window, bg=BG_COLOR)
top_frame.pack(side=TOP, pady=4)

# Creating the format selection 'Combobox'
common.choose_format = Combobox(master=top_frame, values=data_window['screenshot-formats'], width=6)
common.choose_format.pack(side=LEFT, padx=15)
common.choose_format.current(0)

# Shortcuts_frame frame to be mastered my 'top_frame' (shortcuts_label, shortcuts)
shortcuts_frame = Frame(master=top_frame, bg=BG_COLOR)
shortcuts_frame.pack(side=RIGHT, padx=24)

# Shortcut tip
shortcut_label = Label(master=shortcuts_frame, text='?', font=10, bg=BG_COLOR, fg='white')
shortcut_label.pack(side=RIGHT)
shortcut_label.bind(sequence='<Button-1>', func=lambda x: showinfo(title='Shortcuts', message='Ctrl+Alt - take a screenshot\nWin+Alt - hide the window\nWin+Ctrl - show the window'))

# Shortcuts checkbox
shortcuts_on = BooleanVar()
shortcut = Checkbutton(master=shortcuts_frame, text='shortcuts', variable=shortcuts_on, command=shortcuts_toggle)
shortcut.pack(side=RIGHT)

# Bottom frame (for everthing else)
bottom_frame = Frame(master=common.window, bg=BG_COLOR)
bottom_frame.pack(side=BOTTOM, pady=10)

# Current window screenshot feature
common.current_window_on = BooleanVar()
current_window = Checkbutton(master=bottom_frame, text='current window', variable=common.current_window_on)
current_window.pack(side=LEFT, padx=5)

# Creating the 'Screenshot' button
screen = Button(master=bottom_frame, text='Screenshot', height=2, width=10, command=take_screenshot)
screen.pack(side=LEFT, padx=6, pady=9)

# Current Window tip
current_window_label = Label(master=bottom_frame, text='Choose\nwindow', font=10, bg=BG_COLOR, fg='white')
current_window_label.pack(side=RIGHT, padx=1, pady=3)
current_window_label.bind('<Button-1>', lambda y: showinfo(title='Current Window', message='Click on the window you want to screenshot'))

# If-does-not-work checkbox
common.idnw_on = BooleanVar()
idnw = Checkbutton(master=bottom_frame, text='window hiding fix', variable=common.idnw_on)
idnw.pack(side=RIGHT, padx=5)

# Get the window HWND
common.window_hwnd = int(common.window.frame(), 16)

# Allow screenshot taking (saying that screenshot taking is not in progress)
screenshot_taking = False

# Shortcuts corrections
add_shortcuts()
unhook_all_hotkeys()

# Running the window
common.window.mainloop()

# top_frame (master is 'window') ->
	# choose_format (combobox), shortcuts_frame (frame)
		# shortcuts_frame (master is 'top_frame') ->
			# shortcut (shortcut feature checkbox), shortcut_label (tip)

# bottom_frame (master is 'window') ->
	# screen (screenshot button), current_window_label (the tip of the feature to screenshot a certain window),
	# current_window (feature to screenshot a certain window), idnw (If-does-not-work checkbox, then do a delay fix)