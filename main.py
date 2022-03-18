from PIL import ImageGrab
from os import path, remove
from tkinter import BOTTOM, LEFT, RIGHT, TOP, Tk, Frame, BooleanVar, Button, Checkbutton, Label, PhotoImage
from tkinter.messagebox import askokcancel, showerror, showinfo, WARNING
from tkinter.ttk import Combobox
from easygui import filesavebox
from pygetwindow import getAllWindows, getActiveWindowTitle
from win32api import GetSystemMetrics
from win32gui import GetWindowRect, FindWindow
from datetime import datetime
from time import sleep
from keyboard import add_hotkey, unhook_all_hotkeys
from icondata import icondata

# Check if the window is hidden
def window_on(hwnd):
	all_hwnd = f'{getAllWindows()}'.split()
	hwnd_list = []
	for i in all_hwnd:
		hwnd_list.append(int(i[i.rfind('=')+1:i.rfind(')')]))
	return hwnd in hwnd_list

# Function for taking the screenshot (called by the 'Screenshot' button)
def screenshot_function():
	# Hiding the window & waiting for it to really hide
	window_isvisible = window_on(hwnd=window_hwnd)
	withdrawer = None
	withdrawer = window.withdraw()
	while withdrawer is None:
		pass
	while window_on(hwnd=window_hwnd):
		pass
	if idnw_on.get():
		sleep(1) # Goofy fix
	# Taking the screenshot & waiting for it to really be taken
	if current_window_on.get() is False:
		screenshot_take = None
		screenshot_take = ImageGrab.grab()
		while screenshot_take is None:
			pass
	else:
		screenshot_take = None
		screenshot_take = ImageGrab.grab(bbox=tuple(list(GetWindowRect(FindWindow(None, getActiveWindowTitle())))))
		while screenshot_take is None:
			pass
		# bbox - area to be taken from the screen and its size further
	# Determining the screenshot name
	name = str(datetime.now()).replace(':', '-').replace('.', '-')
	save(screenshot_take=screenshot_take, name=name, format=choose_format.get()) # 3rd argument - getting the screenshot format
	# Restoring the window
	if window_isvisible:
		window.deiconify()

def save(screenshot_take, name, format):
	# Requesting the save path & saving
	# explorer = filesavebox(default=f'Screenshot {name}.{format}')
	explorer = filesavebox(default=f'Screenshot {name}')
	if explorer is not None:
		explorer = f'{explorer}.{format}'
		if path.exists(explorer):
			if askokcancel(title='File already exists', message='Do you want to replace this file?', icon=WARNING):
				try:
					remove(explorer)
				except:
					showerror(title='Error', message='Could not replace the file')
					return
		while path.exists(explorer):
			pass
		try:
			screenshot_take.save(explorer)
		except:
			showerror(title='Error', message='Could not save')

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

# Adding shortcuts
def add_shortcuts():
	add_hotkey('ctrl+alt', take_screenshot)
	add_hotkey('win+alt', window.withdraw)
	add_hotkey('win+ctrl', window.deiconify)

# Shortcuts toggle
def shortcuts_toggle():
	if shortcuts_on.get():
		add_shortcuts()
	else:
		unhook_all_hotkeys()


# Window creation & set window settings depending on the screen resolution
BG_COLOR = '#3f3f3f'
window = Tk()
window['bg'] = BG_COLOR
window.title('Screened')
if GetSystemMetrics(0) == 1680 and GetSystemMetrics(1) == 1050:
	window.geometry('420x120')
else:
	window.geometry('420x100')
window.resizable(width=False, height=False)
window.iconphoto(False, PhotoImage(data=icondata))

# Top frame ('choose format' combobox and 'shortcuts' frame)
top_frame = Frame(master=window, bg=BG_COLOR)
top_frame.pack(side=TOP, pady=4)

# Creating the format selection 'Combobox'
choose_format = Combobox(master=top_frame, values=('png', 'jpg', 'jpeg', 'webp'), width=6)
choose_format.pack(side=LEFT, padx=15)
choose_format.current(0)

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
bottom_frame = Frame(master=window, bg=BG_COLOR)
bottom_frame.pack(side=BOTTOM, pady=10)

# Current window screenshot feature
current_window_on = BooleanVar()
current_window = Checkbutton(master=bottom_frame, text='current window', variable=current_window_on)
current_window.pack(side=LEFT, padx=5)

# Creating the 'Screenshot' button
screen = Button(master=bottom_frame, text='Screenshot', height=2, width=10, command=take_screenshot)
screen.pack(side=LEFT, padx=6, pady=9)

# Current Window tip
current_window_label = Label(master=bottom_frame, text='Choose\nwindow', font=10, bg=BG_COLOR, fg='white')
current_window_label.pack(side=RIGHT, padx=1, pady=3)
current_window_label.bind('<Button-1>', lambda y: showinfo(title='Current Window', message='Click on the window you want to screenshot'))

# If-does-not-work checkbox
idnw_on = BooleanVar()
idnw = Checkbutton(master=bottom_frame, text='window hiding fix', variable=idnw_on)
idnw.pack(side=RIGHT, padx=5)

# Get the window HWND
window_hwnd = int(window.frame(), 16)

# Allow screenshot taking (saying that screenshot taking is not in progress)
screenshot_taking = False

# Shortcuts corrections
add_shortcuts()
unhook_all_hotkeys()

# Run the window
window.mainloop()

# top_frame - 108 line
# shortcuts_frame - 117 line
# bottom_frame - 131 line

# top_frame (master is 'window') ->
	# choose_format (combobox), shortcuts_frame (frame)
		# shortcuts_frame (master is 'top_frame') ->
			# shortcut (shortcut feature checkbox), shortcut_label (tip)

# bottom_frame (master is 'window') ->
	# screen (screenshot button), current_window_label (the tip of the feature to screenshot a certain window),
	# current_window (feature to screenshot a certain window), idnw (If-does-not-work checkbox, delay fix)