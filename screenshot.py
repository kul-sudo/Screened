from pygetwindow import getAllWindows, getActiveWindowTitle
from time import sleep
from PIL import ImageGrab
from pygetwindow import getAllWindows, getActiveWindowTitle
from win32gui import GetWindowRect, FindWindow
from datetime import datetime
from save import save_screenshot
import common

# Check if the window is hidden
def window_on(hwnd: str) -> bool:
	all_hwnd = f'{getAllWindows()}'.split() # Turning the array of all of the windows into a list to make the functions for lists appropriate
	hwnd_list = []
	for window in all_hwnd:
		hwnd_list.append(int(window[window.rfind('=')+1:window.rfind(')')])) # Appending hwnds of windows one by one
	return hwnd in hwnd_list # Returning if the the window with the hwnd which is stated as an argument is in the list of hwnds

# Function for taking the screenshot (called by the 'Screenshot' button)
def screenshot_function():
	# Hiding the window & waiting for it to really hide
	window_isvisible = window_on(hwnd=common.window_hwnd)
	withdrawer = None # 'withdrawer' is set to None to check if it has switched from None in the future to make sure the window has hidden
	withdrawer = common.window.withdraw() # Hiding the window for a while to make sure it is not visible while a screenshot is being taken
	while withdrawer is None or window_on(hwnd=common.window_hwnd): # Do not do anything until the window is not still on the screen, or until withdrawer does not equal None
		pass
	if common.idnw_on.get(): # If the 'window hiding fix' checkbox is checked, then do a one second delay to make sure the window actually hid before the screenshot was taken
		sleep(1) # Waiting one second for the window to hide

	# Taking the screenshot & waiting for it to be really taken 
	screenshot_take = None
	if common.current_window_on.get(): # If the 'current window' checkbox is checked, then take a screenshot of a certain area of the screen
		screenshot_take = ImageGrab.grab(bbox=tuple(list(GetWindowRect(FindWindow(None, getActiveWindowTitle()))))) # bbox is a certain area to be taken from the screen
	else: # If the 'current window' checkbox is not check, then take a screenshot of the whole screen
		screenshot_take = ImageGrab.grab()
	while screenshot_take is None: # Do not do anything while the 'screenshot_take' variable hasn't switched from None
		pass

	name = str(datetime.now()).replace(':', '-').replace('.', '-') # Determining the screenshot name
	save_screenshot(screenshot_take=screenshot_take, name=name, format=common.choose_format.get()) # Saving the screenshot (the 3rd argument is for getting the screenshot format)
	if window_isvisible: # Making the window visible again
		common.window.deiconify()