import numpy as np
import cv2
from src.rectangle import rectangle
import csv

class formData():
	def __init__(self, image_path, csv_path):

		self.image = np.array(cv2.imread(image_path, 1))
		self.imageScale = 1000/np.shape(self.image)[1]
		self.image = cv2.resize(self.image, (1000, int(self.imageScale*np.shape(self.image)[0])))

		self.rectangles = []
		self.maxId = 0
		with open(csv_path, 'r', encoding='UTF-8') as file:
			contents = csv.DictReader(file, delimiter=',')
			for row in contents:
				self.rectangles.append(rectangle(row))
				if 'textno' in row and not row['textno'] == '' and int(row['textno']) > self.maxId:
					self.maxId = int(row['textno'])

		self.image_path = image_path
		self.csv_path = csv_path