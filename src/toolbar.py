from tkinter import *
from tkinter import filedialog

class toolbar():
	def __init__(self, main, root):
		self.main = main
		self.menu = Menu(root)

		self.fileMenu = Menu(self.menu, tearoff = 0)
		self.fileMenu.add_command(label = "Import", command = self.import_data)
		self.fileMenu.add_command(label = "Save", command = self.save)
		self.fileMenu.add_command(label = "Save as...", command = self.save_as)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label = "Exit", command = root.destroy)
		self.menu.add_cascade(label="File", menu = self.fileMenu)

		self.editMenu = Menu(self.menu, tearoff=0)
		self.editMenu.add_command(label = "Preferences", command = self.preferences)
		self.menu.add_cascade(label="Edit", menu = self.editMenu)

		self.helpMenu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Help", menu = self.helpMenu)

		root.config(menu=self.menu)

	def import_data(self):
		def fill_image():
			image.delete(0, END)
			image.insert(0, filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("image files","*.png"),("all files","*.*"))))
		def fill_csv():
			csv.delete(0, END)
			csv.insert(0, filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*"))))
		def submission():
			self.main.file_import(image.get(),csv.get())
			importWindow.grab_release()
			importWindow.destroy()
		importWindow = Toplevel()
		importWindow.grab_set()
		imageFrame = Frame(importWindow)
		imageLabel = Label(imageFrame, text = "Image: ")
		image = Entry(imageFrame)
		imageFilePicker = Button(imageFrame, command = fill_image)
		csvFrame = Frame(importWindow)
		csvLabel = Label(csvFrame, text = "CSV file: ")
		csv = Entry(csvFrame)
		csvFilePicker = Button(csvFrame, command = fill_csv)
		submit = Button(importWindow, command = submission, text = "Submit")

		imageFrame.pack()
		csvFrame.pack()
		imageLabel.pack(side=LEFT)
		image.pack(side=LEFT)
		imageFilePicker.pack(side=LEFT)
		csvLabel.pack(side=LEFT)
		csv.pack(side=LEFT)
		csvFilePicker.pack(side=LEFT)
		submit.pack()
		pass

	def preferences(self):
		pass

	def save(self):
		pass

	def save_as(self):
		pass