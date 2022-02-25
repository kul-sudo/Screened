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

# Check if the window is hidden
def window_on(hwnd):
	all_hwnd = f'{getAllWindows()}'.split(',')
	hwnd_list = []
	for i in all_hwnd:
		hwnd_list.append(int(i[i.rfind('=')+1:i.rfind(')')]))
	return hwnd in hwnd_list

# Function for taking the screenshot (called by the 'Screenshot' button)
def screenshot_function():
	# Hiding the window & waiting for it to really hide
	window_isvisible = window_on(window_hwnd)
	withdrawer = None
	withdrawer = window.withdraw()
	while withdrawer is None:
		pass
	while window_on(window_hwnd):
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
	explorer = filesavebox(default=f'Screenshot {name}.{format}')
	if explorer is not None:
		screenshot_path = f'{explorer}.{format}'
		if path.exists(screenshot_path):
			if askokcancel(title='File already exists', message='Do you want to replace this file?', icon=WARNING):
				try:
					remove(screenshot_path)
				except:
					showerror(title='Error', message='Could not replace the file')
					return
		try:
			print(explorer)
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
window.iconphoto(False, PhotoImage(data='iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAAAXNSR0IArs4c6QAAGzVJREFUeF7tnQnUlsP7xyeypahQlC0JKdGi7C1KyVpCdYqkUrIm+5pdSIgsRZSlEFJUllRCSlqPEi2oONlLRPifz/z+r1+/Tm89z/s+z9wz93yvczrE/dwz873m/s7MNddSomHDhv8YiRAQAlEiUEIEEKXeNWghYBEQAWgiCIGIERABRKx8DV0IiAA0B4RAxAiIACJWvoYuBEQAmgNCIGIERAARK19DFwIiAM0BIRAxAiKAiJWvoQsBEYDmgBCIGAERQMTK19CFgAhAc0AIRIyACCBi5WvoQkAEoDkgBCJGQAQQsfI1dCEgAtAcEAIRIyACiFj5GroQEAFoDgiBiBEQAUSsfA1dCIgANAeEQMQIiAAiVr6GLgREAJoDQiBiBEQAEStfQxcCIgDNASEQMQIigIiVr6ELARGA5oAQiBgBEUDEytfQhYAIQHNACESMgAggYuVr6EJABKA5IAQiRkAEELHyNXQhIALQHBACESMgAohY+Rq6EBABaA4IgYgREAFErHwNXQiIADQHhEDECIgAIla+hi4ERACaA0IgYgREABErX0MXAiIAzQEhEDECIoCIla+hCwERgOaAEIgYARFAxMrX0IWACEBzQAhEjIAIIGLla+hCQASgOSAEIkZABBCx8jV0ISAC0BwQAhEjIAKIWPkauhAQAWgOCIGIERABRKx8DV0IiAA0B4RAxAiIACJWvoYuBEQAmgNCIGIERAARK19DFwIiAM0BIRAxAiKAiJWvoQsBEYDmgBCIGAERQMTK19CFgAhAc0AIRIyACCBi5WvoQkAEoDkgBCJGQAQQsfI1dCEgAtAcEAIRIyACiFj5GroQEAFoDgiBiBEQAUSsfA1dCIgANAeEQMQIiAAiVr6GLgREAJoDQiBiBEQAEStfQxcCURPATjvtZHbbbTfzxRdfmN9++02zQQhEh0DUBNC3b19z6KGHmnXr1pm33nrLPP/882bp0qXRTQINOF4EoiWAww47zNxyyy1mq622+lf7EMHXX39tnn32WTNlyhTz66+/xjszNPIoEIiSALbZZhvz5JNPmkqVKm1UyX///beZNWuWGTdunHn33XfN77//HsVk0CDjQyBKAjjhhBPM5ZdfnpG2v/zySzNq1CjzxhtvaEeQEWJ6KCQEoiOAHXfc0dx5552mevXqWenp559/NmPGjDETJ040CxYsyOq3elgI+IpAdARw5plnmh49ehRZHz/++KM1GEIGy5YtM3/++WeR3xXzD7fbbjtTunRpU7FiRcORbIsttrBwVKlSxf6dY9j68s8//5hvv/3WrF692qxdu9be2vz000/27/z7hs/HjG02Y4+KALbffnvz2GOPmcqVK2eD0UafXbNmjfnwww/t0WDmzJkiggwQLVOmjKlatao58MADrQ72339/+/cSJUpk8Ov/PgIZ8MEvX77czJ8/36xcudJMnz7dfPbZZ5YQJJkjEBUBtGrVylx44YX/rjaZw1T4k0zGRYsWmeHDh5upU6cajgqS/yKw3377mSOOOMLUrl3bfvDbbrtt3uBhNzZhwgQzadIkM23aNLtTkGwagWgIYOutt7Yfably5fIyJ/766y/zyy+/WBvBiBEj7OoUo4AzvhXHHnus2XPPPU2FChXMDjvs4BSKP/74w3BUw6dj9OjR9kZHxLxxFURDAM2aNTPXXnutk4nIx//222+b8ePHW78CdgkxyN57723atm1rmjdvnvW2Pl/4cFSYN2+eefXVV61OYtFFpnhGQQClSpUyDzzwgNl3330zxSUnzzHZJk+ebIYNG2bPp2kV3Knbt29vWrZsabbccktvh8lOYODAgdZuIPkPAlEQQJs2bcwFF1yQmM4hgrlz51oD5Jw5cxLrRy4bxnBXrVo1g13lyCOPdL7NL+pYOKZhuIWUV61aVdTXpOZ3qSeAsmXLmnvuucf56r/hDGErOmDAADNy5MjgJ0/58uXNqaeeak466aS82VTyCRKEvHDhQnPfffdZn46YrxBTTwBJr/4FE5k77GuuucZGHoYsXN/17t3bWvVDF4gAf47Bgwdbo2GMkmoC4Dz60ksvGXYBSQvb/+eeey5oI1S9evXMVVddZXbeeeek4cxp+5Dy7bffHjw5FwWUVBMA1uirr766KLjk9DdLliwxl156adCrTOvWra0H5frRkzkFKeGX4dh18803W+eumCS1BFCyZEnz6KOPWk+zpIXYg7FjxybdjSK3j4W/S5cuOXWgKnJn8vhDwr9vvfVW88EHH+SxFb9enVoCYNv/yiuvJI42qz8fD7kGQhOcpnr27GmaNm0aWteL3F8Mgr169bLu3TFIagmguEE/uVA+eQRY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'))

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
shortcut_label.bind('<Button-1>', lambda x: showinfo(title='Shortcuts', message='Ctrl+Alt - take a screenshot\nWin+Alt - hide the window\nWin+Ctrl - show the window'))

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

# top_frame - 110 line
# shortcuts_frame - 119 line
# bottom_frame - 133 line

# top_frame (master is 'window') ->
	# choose_format (combobox), shortcuts_frame (frame)
		# shortcuts_frame (master is 'top_frame') ->
			# shortcut (shortcut feature checkbox), shortcut_label (tip)
	
# bottom_frame (master is 'window') ->
	# screen (screenshot button), current_window_label (the tip of the feature to screenshot a certain window), 
	# current_window (feature to screenshot a certain window), idnw (If-does-not-work checkbox, delay fix)