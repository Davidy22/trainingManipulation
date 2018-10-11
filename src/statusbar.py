from tkinter import *

class statusbar():
	def __init__(self, main, root):
		self.main = main
		self.frame = Frame(root)
		self.text = StringVar()
		self.label = Label(self.frame, bd=1, relief= SUNKEN, anchor=W, textvariable=self.text, font=('arial',16,'normal'))
		self.text.set("Statusbar placeholder")
		self.label.pack(fill = X)

	def get_frame(self):
		return self.frame