from tkinter.messagebox import askokcancel, showerror, WARNING
from easygui import filesavebox
from os import path, remove

def save_screenshot(screenshot_take, name: str, format: str): # Determining the screenshot saving function
	explorer = None # 'explorer' is set to None to check if it has switched from None in the future to make sure the explorer has actually opened
	explorer = filesavebox(default=f'Screenshot {name}') # Calling the explorer with the default name of the file being 'Screenshot' and the current date
	if explorer is not None: # Making sure the explorer has actually opened
		explorer = f'{explorer}.{format}' # Set 'explorer' to the path where to screenshot should be saved and the format it should be saved with
		if path.exists(explorer): # Checking if this file already exists
			if askokcancel(title='File already exists', message='Do you want to replace this file?', icon=WARNING): # Warning that this file already exists
				try:
					remove(explorer) # Removing the file
				except: # Checking if the removing caused an error
					showerror(title='Error', message='Could not replace the file') # Showing an error that says that the file could not be replaced
					return
			while path.exists(explorer): # The file might not have been replaced at this point
				pass # Do not do anything while the file is not replaced
		try: # Saving the screenshot with the path stated in 'explorer'
			screenshot_take.save(explorer)
		except: # If the saving caused an error, then show it
			showerror(title='Error', message='Could not save')