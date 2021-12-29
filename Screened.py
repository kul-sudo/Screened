import pyautogui
import os
from tkinter import Tk, Button, messagebox
from tkinter.ttk import Combobox
from easygui import filesavebox
from string import digits
from random import choice

def screenshot_function():
	screenshot_format = choose_format.get()
	window.withdraw()
	screenshot = None
	screenshot = pyautogui.screenshot()
	while screenshot == None:
		pass
	window.deiconify()
	name = ''
	for _ in range(10):
		name += choice(digits)
	explorer = filesavebox(default = f'{name}.{screenshot_format}')
	if explorer == None:
		pass
	else:
		path = f'{explorer}.{screenshot_format}'
		if os.path.exists(path):
			try:
				os.remove(path)
			except:
				messagebox.showerror(title='Error', message='An error occurred')
				return
		try:
			screenshot.save(f'{explorer}.{screenshot_format}')
		except:
			messagebox.showerror(title='Error', message='An error occurred')

window = Tk()
window['bg'] = '#3f3f3f'
window.title('Screened')
window.geometry('300x90')
window.resizable(width=False, height=False)
screen = Button(window, text='Screenshot', height=2, width=10, command=screenshot_function)
screen.place(x=105, y=50)
choose_format = Combobox(window)
choose_format['values'] = ('png', 'jpg', 'jpeg')
choose_format.current(0)
choose_format.pack()
window.mainloop()