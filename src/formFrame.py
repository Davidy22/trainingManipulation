from tkinter import *
from src.formManipulation import formManipulation
from PIL import ImageTk, Image

class formFrame():
	def __init__(self, form, root):
		self.frame = Frame(root)
		self.controlFrame = Frame(self.frame)
		self.controlFrame.place(relwidth = 1, height = 40)
		self.scale = Scale(self.controlFrame, from_=10, to=100, orient = HORIZONTAL, command = self.scaling_event, showvalue=0, label="Scale")
		self.scale.set(100)
		self.blank = Checkbutton(self.controlFrame, text="Blank", command = self.blankwords)
		self.deleteButton = Button(self.controlFrame, text = "Delete", command = self.delete_button)
		self.textButton = Button(self.controlFrame, text = "Change Text", command = self.text_button)
		self.groupButton = Button(self.controlFrame, text = "Group", command = self.group_button)

		self.scale.pack(side=LEFT)
		self.blank.pack(side=LEFT)
		self.deleteButton.pack(side=LEFT)
		self.textButton.pack(side=LEFT)
		self.groupButton.pack(side=LEFT)

		self.imgframe = Frame(self.frame)
		self.imgframe.place(x=0,y = 40, rely=0, relwidth = 1, relheight = 1, height = -40)
		self.canvas = Canvas(self.imgframe)
		self.yscrollbar = Scrollbar(self.imgframe, orient="vertical", command=self.canvas.yview)
		self.xscrollbar = Scrollbar(self.imgframe, orient="horizontal", command=self.canvas.xview)
		self.canvas.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

		self.yscrollbar.pack(side=RIGHT, fill=Y)
		self.xscrollbar.pack(side=BOTTOM, fill=X)
		self.canvas.pack(side=LEFT, fill='both', expand=True)

		self.form = formManipulation(form)

		self.canvas.bind("<Button-1>", self.left_click)
		self.canvas.bind("<B1-Motion>", self.mouse_drag)
		self.canvas.bind("<Motion>", self.mouse_move)
		self.canvas.bind("<ButtonRelease-1>", self.button_release)
		self.canvas.bind("<MouseWheel>", self.mousewheel)
		self.canvas.bind("<Configure>", self.resize)
		self.canvas.bind("<Delete>", self.delete)
		self.canvas.bind("<Return>", self.enter)
		self.canvas.bind("<Double-Button-1>", self.double_click)
		self.canvas.bind("<Key>", self.keyboard)

		self.mousePos = (0,0)

		self.draw(self.form.redraw())

	def keyboard(self, event):
		self.draw(self.form.type(event.char))

	def enter(self, event):
		self.draw(self.form.enter())

	def double_click(self, event):
		self.draw(self.form.double_click(event.widget.canvasx(event.x),event.widget.canvasy(event.y)))

	def left_click(self, event):
		self.draw(self.form.mouse_click(event.widget.canvasx(event.x),event.widget.canvasy(event.y)))
		self.canvas.focus_set()

	def mouse_move(self, event):
		self.mousePos = (event.widget.canvasx(event.x), event.widget.canvasy(event.y))

	def mouse_drag(self, event):
		self.draw(self.form.mouse_drag(event.widget.canvasx(event.x),event.widget.canvasy(event.y)))

	def button_release(self, event):
		self.draw(self.form.mouse_button_up())

	def scaling_event(self, event):
		self.canvas.configure(width = int(100 * self.imgframe.winfo_width() / int(event)),
		                      height = int(100 * self.imgframe.winfo_height() / int(event)),
		                      scrollregion=self.canvas.bbox("all"))
		self.draw(self.form.set_scaling((int(event)*self.form.dimensions[1])/(self.canvas.winfo_width()*100)))

	def mousewheel (self, event):
		new = self.scale.get() + event.delta/60
		if new > 100:
			new = 100
		elif new < 10:
			new = 10
		self.scale.set(new)

	def blankwords(self):
		self.form.toggle_view()
		self.draw(self.form.redraw())

	def resize(self, event):
		self.canvas.configure(width = int(100 * self.imgframe.winfo_width() / int(self.scale.get())),
		                      height = int(100 * self.imgframe.winfo_height() / int(self.scale.get())),
		                      scrollregion=self.canvas.bbox("all"))
		#self.form.set_view(event.width, event.height)
		self.draw(self.form.set_scaling((int(self.scale.get())*self.form.dimensions[1])/(self.canvas.winfo_width()*100)))

	def draw(self, img):
		if img is None:
			return
		self.im = Image.fromarray(img)
		self.photo = ImageTk.PhotoImage(image=self.im)
		self.canvas.delete(ALL)
		self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

	def redraw(self):
		self.draw(self.form.redraw(cache_after=False, cache_mode=2))

	def delete(self, event):
		self.draw(self.form.delete(self.mousePos[0], self.mousePos[1]))

	def delete_button(self):
		if self.form.set_input_mode(1) == 0:
			self.deleteButton.configure(relief = RAISED)
		else:
			self.groupButton.configure(relief=RAISED)
			self.textButton.configure(relief=RAISED)
			self.deleteButton.configure(relief = SUNKEN)

	def text_button(self):
		if self.form.set_input_mode(2) == 0:
			self.textButton.configure(relief = RAISED)
		else:
			self.deleteButton.configure(relief=RAISED)
			self.groupButton.configure(relief=RAISED)
			self.textButton.configure(relief = SUNKEN)

	def group_button(self):
		if self.form.set_input_mode(3) == 0:
			self.groupButton.configure(relief = RAISED)
		else:
			self.deleteButton.configure(relief=RAISED)
			self.textButton.configure(relief=RAISED)
			self.groupButton.configure(relief = SUNKEN)

	def get_frame(self):
		return self.frame