from pyautogui import size
from pyscreeze import screenshot
from os import path, remove
from tkinter import Tk, Button, messagebox
from tkinter.ttk import Combobox
from easygui import filesavebox
from string import digits
from random import choice

def screenshot_function():
	screenshot_format = choose_format.get()
	screenshot_now = False
	window.withdraw()
	screenshot_now = True
	while screenshot_now is False:
		pass
	screenshot_take = None
	screenshot_take = screenshot()
	while screenshot_take == None:
		pass
	window.deiconify()
	name = ''
	for _ in range(10):
		name += choice(digits)
	explorer = filesavebox(default = f'{name}.{screenshot_format}')
	if explorer != None:
		screenshot_path = f'{explorer}.{screenshot_format}'
		if path.exists(screenshot_path):
			try:
				remove(screenshot_path)
			except:
				messagebox.showerror(title='Error', message='An error occurred')
				return
		try:
			screenshot_take.save(f'{explorer}.{screenshot_format}')
		except:
			messagebox.showerror(title='Error', message='An error occurred')

x = size()[0]
y = size()[1]
window = Tk()
window['bg'] = '#3f3f3f'
window.title('Screened')
if x == 1920 and y == 1080:
	window.geometry('300x100')
elif x == 1680 and y == 1050:
	window.geometry('300x120')
else:
	window.geometry('300x100')
window.resizable(width=False, height=False)
screen = Button(window, text='Screenshot', height=2, width=10, command=screenshot_function)
screen.place(x=105, y=50)
choose_format = Combobox(window)
choose_format['values'] = ('png', 'jpg', 'jpeg', 'webp')
choose_format.current(0)
choose_format.pack()
window.mainloop()