from tkinter import *
from src.fileFrame import fileFrame
from src.dataFrame import dataFrame
from src.toolbar import toolbar
from src.formFrame import formFrame
from src.formData import formData
from src.statusbar import statusbar

class mainWindow():
	def __init__(self):
		self.files = {}

		self.root = Tk()
		self.root.iconbitmap(default="icon.ico")
		self.root.geometry("%dx%d+0+0" % (self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
		self.statusbar = statusbar(self, self.root)
		self.panedWindow = PanedWindow(self.root)
		self.panedWindow.config(relief=RAISED, showhandle = True)
		self.fileFrameContainer = fileFrame(self, self.panedWindow)
		self.fileFrame = self.fileFrameContainer.get_frame()
		#self.dataFrameContainer = dataFrame(self, self.panedWindow)
		#self.dataFrame = self.dataFrameContainer.get_frame()
		#self.formFrameContainer = formFrame(self, self.panedWindow)
		#self.formFrame = self.formFrameContainer.get_frame()
		self.toolbar = toolbar(self, self.root)

		self.statusbar.get_frame().place(relx = 0, rely = 1, y = -20, relwidth = 1, height = 20)
		self.panedWindow.place(relx = 0, rely = 0, relwidth = 1, relheight = 1, height = -20)
		self.panedWindow.add(self.fileFrame)
		#self.panedWindow.add(self.dataFrame)
		#self.panedWindow.add(self.formFrame)

		self.root.update()
		self.root.mainloop()

	def file_import(self, image_path, csv_path):
		#seperate file loading
		self.files[image_path] = formData(image_path, csv_path)
		self.currentForm = self.files[image_path]
		self.fileFrameContainer.add_form(image_path)

		#TODO: Store in memory, don't destroy
		try:
			self.panedWindow.forget(self.dataFrame)
			self.dataFrame.destroy()
		except AttributeError:
			pass #ignore if already closed

		try:
			self.panedWindow.forget(self.formFrame)
			self.formFrame.destroy()
		except AttributeError:
			pass #ignore if already closed

		self.dataFrameContainer = dataFrame(self.files[image_path], self.panedWindow)
		self.dataFrame = self.dataFrameContainer.get_frame()
		self.panedWindow.add(self.dataFrame)
		self.panedWindow.paneconfigure(self.dataFrame, width = int(2*self.panedWindow.winfo_width()/3))

		self.formFrameContainer = formFrame(self.files[image_path], self.panedWindow)
		self.formFrame = self.formFrameContainer.get_frame()
		self.panedWindow.add(self.formFrame)
		self.panedWindow.paneconfigure(self.formFrame, width = int(self.panedWindow.winfo_width()/3))

	def switch_form(self, form_name):
		try:
			self.panedWindow.forget(self.dataFrame)
			self.dataFrame.destroy()
		except AttributeError:
			pass #ignore if already closed

		try:
			self.panedWindow.forget(self.formFrame)
			self.formFrame.destroy()
		except AttributeError:
			pass #ignore if already closed

		self.dataFrameContainer = dataFrame(self.files[form_name], self.panedWindow)
		self.dataFrame = self.dataFrameContainer.get_frame()
		self.panedWindow.add(self.dataFrame)
		self.panedWindow.paneconfigure(self.dataFrame, width = int(2*self.panedWindow.winfo_width()/3))

		self.formFrameContainer = formFrame(self.files[form_name], self.panedWindow)
		self.formFrame = self.formFrameContainer.get_frame()
		self.panedWindow.add(self.formFrame)
		self.panedWindow.paneconfigure(self.formFrame, width = int(self.panedWindow.winfo_width()/3))