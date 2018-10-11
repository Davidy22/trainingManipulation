class rectangle:
	def __init__(self, row): #ix, iy, x, y, text=''):
		self.data = row
		for label in ['\ufefflevel', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text', 'label', 'textno']:
			if label not in row:
				row[label] = ''
		self.integerize()

	def integerize(self):
		self.data["height"] = int(self.data["height"])
		self.data["width"] = int(self.data["width"])
		self.data["top"] = int(self.data["top"])
		self.data["left"] = int(self.data["left"])

	def set_xy(self, x, y):
		self.integerize()
		self.data["width"] = x - self.data["left"]
		self.data["height"] = y - self.data["top"]

	def set_ixy(self, ix, iy):
		self.integerize()
		self.data["top"] = iy
		self.data["left"] = ix

	def get_xy(self):
		self.integerize()
		return (self.data["left"] + self.data["width"], self.data["top"] + self.data["height"])

	def get_ixy(self):
		self.integerize()
		return (self.data["left"], self.data["top"])

	def get_bottom_left(self, offset = 0):
		self.integerize()
		if self.data["width"] < 0:
			left = self.data["left"] + self.data["width"]
		else:
			left = self.data["left"]
		if self.data["height"] < 0:
			bottom = self.data["top"]
		else:
			bottom = self.data["top"] + self.data["height"]
		return (left + offset, bottom - offset)
		
	def get_top_left(self, offset = 0):
		self.integerize()
		if self.data["width"] < 0:
			left = self.data["left"] + self.data["width"]
		else:
			left = self.data["left"]
		if self.data["height"] < 0:
			top = self.data["top"] + self.data["height"]
		else:
			top = self.data["top"]
		return (left + offset,top - offset)

	def shift(self, dx, dy):
		self.integerize()
		self.data["left"] -= dx
		self.data["top"] -= dy

	def resize(self, dx, dy, mode):#3 = resizeTL, 4 = resizeTR, 5 = resizeBL, 6 = resizeBR,7=resizeL,8=resizeR,9=resizeT,10=resizeB
		self.integerize()
		if mode == 3:
			self.data["left"] -= dx
			self.data["top"] -= dy
			self.data["width"] += dx
			self.data["height"] += dy
		elif mode == 4:
			self.data["top"] -= dy
			self.data["width"] -= dx
			self.data["height"] += dy
		elif mode == 5:
			self.data["left"] -= dx
			self.data["width"] += dx
			self.data["height"] -= dy
		elif mode == 6:
			self.data["width"] -= dx
			self.data["height"] -= dy
		elif mode == 7:
			self.data["left"] -= dx
			self.data["width"] += dx
		elif mode == 8:
			self.data["width"] -= dx
		elif mode == 9:
			self.data["top"] -= dy
			self.data["height"] += dy
		elif mode == 10:
			self.data["height"] -= dy

	def check_handles(self, x, y, line_weight):
		self.integerize()
		right = self.data["left"] + self.data["width"]
		left = self.data["left"]
		bottom = self.data["top"] + self.data["height"]
		top = self.data["top"]

		if (left < x < right) and (top < y < bottom):
			return 2

		if left + line_weight > x > left - line_weight:
			if bottom + line_weight > y > bottom - line_weight:
				return 5
			if top + line_weight > y > top - line_weight:
				return 3
		if right + line_weight > x > right - line_weight:
			if bottom + line_weight > y > bottom - line_weight:
				return 6
			if top + line_weight > y > top - line_weight:
				return 4

		#Make these border handles
		if bottom > y > top:
			if left + line_weight > x > left - line_weight:
				return 7
			if right + line_weight > x > right - line_weight:
				return 8
		if right > x > left:
			if bottom + line_weight > y > bottom - line_weight:
				return 10
			if top + line_weight > y > top - line_weight:
				return 9

		return 0

	def is_valid(self):
		return not (self.data["textno"] == '')

	def ensure_correctness(self):
		self.integerize()
		if self.data["height"] < 0:
			self.data["top"] = self.data["height"] + self.data["top"]
			self.data["height"] = abs(self.data["height"])
		if self.data["width"] < 0:
			self.data["left"] = self.data["width"] + self.data["left"]
			self.data["width"] = abs(self.data["width"])