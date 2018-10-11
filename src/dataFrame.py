from tkinter import *

#TODO: Make this actually do something.
#TODO: Performance enhancements very necessary
class dataFrame():
	def __init__(self, form, root):
		self.form = form
		self.frame = Frame(root)
		self.canvas = Canvas(self.frame)
		self.spreadsheet = Frame(self.canvas)
		self.yscrollbar = Scrollbar(self.frame, orient = "vertical", command = self.canvas.yview)
		self.xscrollbar = Scrollbar(self.frame, orient = "horizontal", command = self.canvas.xview)
		self.canvas.configure(yscrollcommand = self.yscrollbar.set, xscrollcommand = self.xscrollbar.set)

		self.yscrollbar.pack(side="right", fill=Y)
		self.xscrollbar.pack(side="bottom", fill=X)
		self.canvas.pack(side="left", fill='both', expand=True)
		self.canvas.create_window((0, 0), window=self.spreadsheet, anchor='nw')
		self.spreadsheet.bind("<Configure>", self.resize)

		table(form.rectangles, self.spreadsheet)
	def resize(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def get_frame(self):
		return self.frame

class cell():
	def __init__(self, view, x, y, parent, val = ""):
		self.x = x
		self.y = y
		self.val = StringVar()
		self.val.set(val)
		self.parent = parent

		self.entry = Entry(view, textvariable = self.val, justify = "right")
		self.entry.bind("<FocusOut>", self.update)
		self.entry.bind("<Return>", self.update)
		self.entry.bind("<Left>", self.move(-1, 0))
		self.entry.bind("<Right>", self.move(1, 0))
		self.entry.bind("<Up>", self.move(0, -1))
		self.entry.bind("<Down>", self.move(0, 1))
		self.entry.grid(row = self.y, column = self.x)

	def update(self, event):
		self.parent.update(self.x, self.y, self.val.get())

	def move(self, dx, dy):
		def focus(event):
			self.parent.move(self.x + dx, self.y + dy)

		return focus

class table():
	def __init__(self, rectangles, view):
		self.labels = []
		self.table = [[]]
		self.x = 0
		self.y = 1
		self.rectangles = rectangles
		for label in rectangles[0].data:
			self.labels.append(label)
			self.table[0].append(cell(view, self.x, 0, self, label))
			self.x += 1

		for rect in rectangles:
			self.x = 0
			self.table.append([])
			for label in self.labels:
				if label in rect.data:
					self.table[self.y].append(cell(view, self.x, self.y, self, rect.data[label]))
				else:
					self.table[self.y].append(cell(view, self.x, self.y, self))
				self.x += 1
			self.y += 1

	def move(self, x, y):
		if 0 <= x < self.x and 0<= y < self.y:
			self.table[y][x].entry.focus()

	def update(self, x, y, data):
		self.table[y][x] = data
		self.rectangles[y-1].data[self.labels[x]] = data