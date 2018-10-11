from tkinter import *
from tkinter.ttk import *


class fileFrame():
	def __init__(self, main, root):
		self.main = main
		self.frame = Frame(root)
		self.files = Treeview(self.frame)
		self.files.pack(fill='both', expand=True)
		self.files.bind("<Double-1>", self.selection)

	def add_form(self, imageName):
		self.files.insert('', 'end', text=imageName)

	def selection(self, event):
		self.main.switch_form(self.files.item(self.files.selection()[0],"text"))

	def get_frame(self):
		return self.frame
