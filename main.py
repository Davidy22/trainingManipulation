import csv
from src.mainWindow import mainWindow

#TODO: Make conf file
#TODO: Make l10n file
#TODO: Make file handler it's own module
if __name__ == '__main__':
	win = mainWindow()
	if win.status == 1:
		out = []
		for rect in win.rectangles:
			found = False
			for row in rows:
				if not row['textno'] == '':
					if rect == int(row['textno']):
						row['top'] = win.rectangles[rect].iy
						row['left'] = win.rectangles[rect].ix
						row['width'] = abs(win.rectangles[rect].x-win.rectangles[rect].ix)
						row['height'] = abs(win.rectangles[rect].y-win.rectangles[rect].iy)
						row['text'] = win.rectangles[rect].text
						found = True
						break
			if found:
				out.append(row)
			else:
				out.append({
					'top':win.rectangles[rect].iy,
					'left':win.rectangles[rect].ix,
					'width': abs(win.rectangles[rect].x-win.rectangles[rect].ix),
					'height':abs(win.rectangles[rect].y-win.rectangles[rect].iy),
					'textno':rect,
					'text':win.rectangles[rect].text
				})
		with open('test.csv', 'w', encoding='UTF-8', newline='') as file:
			writer = csv.DictWriter(file, ['\ufefflevel', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text', 'label', 'textno'])
			for row in out:
				writer.writerow(row)