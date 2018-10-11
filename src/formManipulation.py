import cv2
import numpy as np
from src.rectangle import rectangle


class formManipulation: # TODO: Seperate viewport/scale code from domain specific code at some point
	'''Carries out basic actions on tesseract boxes and returns image representing it'''
	def __init__(self, form):
		self.original = form.image.copy()
		self.img_cache = form.image.copy()
		self.imageScale = form.imageScale
		self.dimensions = np.shape(form.image)
		self.rectangles = form.rectangles
		self.scaling = 1
		self.view = 0

		self.ix = 0
		self.iy = 0
		# TODO: farm these out to a conf file
		# TODO: enumerate self.mode later
		self.mode = 0  # 0 = none, 1 = draw, 2 = drag, 3 = resizeTL, 4 = resizeTR, 5 = resizeBL, 6 = resizeBR,7=resizeL,8=resizeR,9=resizeT,10=resizeB,11=typing
		self.input_mode = 0 # 0 = default, 1 = deletion, 2 = text, 3 = grouping
		self.id = None
		self.nextId = form.maxId
		self.line_weight = 4

	def mouse_click(self, x, y):
		x = int(x * self.scaling)
		y = int(y* self.scaling)

		self.ix, self.iy = x, y

		for rect in self.rectangles:
			if not (rect.data["textno"] == ""):
				self.mode = rect.check_handles(x, y, self.line_weight)
			if self.mode != 0:
				if self.input_mode == 0:
					self.id = rect
					return self.redraw(cache_after=True, cache_mode=1)
				elif self.input_mode == 1:
					self.mode = 0
					self.rectangles.remove(rect)
					return self.redraw(cache_after=True, cache_mode=0)
				elif self.input_mode == 2:
					self.id = rect
					self.mode = 11
					return self.redraw(cache_after=True, cache_mode=1)
				elif self.input_mode == 3: #TODO: Implement later
					return self.redraw(cache_after=True, cache_mode=1)
		if self.input_mode == 0:
			self.mode = 1
			self.id = rectangle({"top": y, "left": x, "height": 0, "width": 0, "textno": self.nextId})
			self.nextId += 1
			self.rectangles.append(self.id)  # Update here
			return self.redraw(cache_after=True, cache_mode=1)

	def mouse_drag(self, xin, yin):
		x = int(xin * self.scaling)
		y = int(yin * self.scaling)

		if self.mode == 1:
			self.id.set_xy(x, y)
			return self.redraw(cache_after = False, cache_mode=1)
		elif self.mode == 2:
			self.id.shift(self.ix - x, self.iy - y)
			self.ix, self.iy = x, y
			return self.redraw(cache_after = False, cache_mode=1)
		elif 3 <= self.mode <= 10:
			self.id.resize(self.ix - x, self.iy - y, self.mode)
			self.ix, self.iy = x, y
			return self.redraw(cache_after = False, cache_mode=1)
		else:
			return None

	def mouse_button_up(self):
		if self.view == 1 and self.mode == 1:
			self.mode = 11
		if self.mode != 11:
			self.mode = 0
			try:
				self.id.ensure_correctness()
			except AttributeError:
				pass
			return self.redraw(cache_after=True, cache_mode=0)

	def delete(self, xin, yin):
		x = int(xin * self.scaling)
		y = int(yin * self.scaling)
		for rect in self.rectangles:
			if not (rect.data["textno"] == "") and rect.check_handles(x, y, self.line_weight) != 0:
				self.rectangles.remove(rect)
				return self.redraw(cache_after=True, cache_mode=0)
		return self.redraw(cache_after=False, cache_mode=2)

	def type(self, key):
		if self.mode == 11:
			self.id.data["text"] = self.id.data["text"] + key
			return self.redraw(cache_after=False, cache_mode=1)
		else:
			return None

	def enter(self):
		if self.mode == 11:
			self.mode = 0
			return self.redraw(cache_after=True, cache_mode=0)
		else:
			return None

	def double_click(self, xin, yin):
		x = int(xin * self.scaling)
		y = int(yin * self.scaling)
		for rect in self.rectangles:
			if not (rect.data["textno"] == "") and rect.check_handles(x, y, self.line_weight) == 2:
				self.id = rect
				self.mode = 11
				return self.redraw(cache_after=False, cache_mode=1)

	def set_scaling(self, scaling):
		self.scaling = scaling / self.imageScale
		return self.redraw(cache_after=False, cache_mode=2)

	def toggle_view(self):
		if self.view == 1:
			self.view = 0
		else:
			self.view = 1

	def set_input_mode(self, mode):
		if mode != 0 and self.input_mode == mode:
			self.input_mode = 0
		else:
			self.input_mode = mode
		return self.input_mode

	def redraw(self, cache_after=True, cache_mode=0): # cache_modes: 0 = redraw all, 1= redraw id (omits id if used with cache_after), 2 = redraw none,
		# TODO: Make this faster and cleaner
		if cache_mode == 2:
			img = cv2.resize(self.img_cache, (int(self.dimensions[1]/self.scaling), int(self.dimensions[0]/self.scaling)), interpolation=cv2.INTER_NEAREST)
			return img

		if self.view == 0:
			if cache_mode == 1:
				if cache_after:
					img = np.copy(self.original)
					for rect in self.rectangles:
						if not (rect is self.id) and rect.is_valid():
							self.draw_rect(img, rect)
					self.img_cache = np.copy(img)
				else:
					img = np.copy(self.img_cache)
				self.draw_rect(img)
			elif cache_mode == 0:
				img = np.copy(self.original)
				for rect in self.rectangles:
					if rect.is_valid():
						self.draw_rect(img, rect)
				if cache_after:
					self.img_cache = np.copy(img)
			img = cv2.resize(img, (int(self.dimensions[1]/self.scaling), int(self.dimensions[0]/self.scaling)), interpolation=cv2.INTER_NEAREST)
			return img

		elif self.view == 1: #write caches for this  # cache_modes: 0 = redraw all, 1= redraw id (omits id if used with cache_after), 2 = redraw none,
			if cache_mode == 1:
				if cache_after:
					img = np.full(self.dimensions, 255, np.uint8)
					for rect in self.rectangles:
						if not (rect is self.id) and rect.is_valid():
							self.draw_rect(img, rect, labelled=True)
					self.img_cache = np.copy(img)
				else:
					img = np.copy(self.img_cache)
				self.draw_rect(img, labelled=True)
			elif cache_mode == 0:
				img = np.full(self.dimensions, 255, np.uint8)
				for rect in self.rectangles:
					if rect.is_valid():
						self.draw_rect(img, rect, labelled = True)
				if cache_after:
					self.img_cache = np.copy(img)

			img = cv2.resize(img, (int(self.dimensions[1] /self.scaling), int(self.dimensions[0]/self.scaling)), interpolation=cv2.INTER_NEAREST)

			return img

	def draw_rect(self, img, rect = None, labelled = False):
		if labelled:
			if rect is None:
				cv2.rectangle(img, self.id.get_ixy() / self.imageScale, self.id.get_xy() / self.imageScale, (0, 255, 0), self.line_weight)
				cv2.putText(img, self.id.data["text"], self.scale(self.id.get_bottom_left(self.line_weight)),
				            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), self.line_weight)
				cv2.putText(img, str(self.id.data["textno"]), self.scale(self.id.get_top_left(self.line_weight)),
				            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), self.line_weight)
			else:
				cv2.rectangle(img, rect.get_ixy() / self.imageScale, rect.get_xy() / self.imageScale, (255, 0, 0), self.line_weight)
				cv2.putText(img, rect.data["text"], self.scale(rect.get_bottom_left(self.line_weight)),
				            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), self.line_weight)
				cv2.putText(img, str(rect.data["textno"]), self.scale(rect.get_top_left(self.line_weight)),
				            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), self.line_weight)
		else:
			if rect is None:
				cv2.rectangle(img, self.scale(self.id.get_ixy()), self.scale(self.id.get_xy()), (0, 255, 0), self.line_weight)
			else:
				cv2.rectangle(img, self.scale(rect.get_ixy()), self.scale(rect.get_xy()), (255, 0, 0), self.line_weight)

	def scale(self, coord):
		return tuple(int(i/2) for i in coord)