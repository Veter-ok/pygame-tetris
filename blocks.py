import pygame
from constants import MARGIN_LEFT, MARGIN_TOP, CELL_SIZE, HEIGHT, WIDTH

def boardPosToPixels(pos):
	left, top, cell_size = MARGIN_LEFT, MARGIN_TOP, CELL_SIZE
	x, y = pos
	return (x * cell_size + left, y * cell_size + top)

def minY(positions):
	miny = 0
	for position in positions:
		if position[1] > miny:
			miny = position[1]
	return miny

def leftX(positions):
	leftx = WIDTH
	for position in positions:
		if position[0] < leftx:
			leftx = position[0]
	return leftx

def rightX(positions):
	rightx = 0
	for position in positions:
		if position[0] > rightx:
			rightx = position[0]
	return rightx

class MainBlock():
	def __init__(self, color):
		self.color = color

	def get_positions(self):
		return self.positions
	
	def get_color(self):
		return self.color

	def render(self, screen):
		for position in self.positions:
			pos = boardPosToPixels(position)
			pygame.draw.rect(screen, self.color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

	def move(self, pos):
		if pos == "RIGHT" and rightX(self.positions) + 1 < WIDTH:
			for index in range(len(self.positions)):
				x, y = self.positions[index]
				self.positions[index] = (x + 1, y)
		elif pos == "LEFT" and leftX(self.positions) > 0:
			for index in range(len(self.positions)):
				x, y = self.positions[index]
				self.positions[index] = (x - 1, y)
		elif pos == "DOWN" and minY(self.positions) + 1 < HEIGHT:
			for index in range(len(self.positions)):
				x, y = self.positions[index]
				self.positions[index] = (x, y + 1)	

	def fall(self):
		if minY(self.positions) + 1 < HEIGHT:
			for index in range(len(self.positions)):
				x, y = self.positions[index]
				self.positions[index] = (x, y + 1)
	
	def isFall(self, y):
		if minY(self.positions) == y:
			return True
		return False


class Cube(MainBlock):
	def __init__(self, color): 
		super().__init__(color)
		self.positions = [(3, 0), (4, 0), (3, 1), (4, 1)]

	def rotate(self):
		pass


class Rectangle(MainBlock):
	def __init__(self, color):
		super().__init__(color) 
		self.positions = [(3, 0), (4, 0), (5, 0), (6, 0)]
		self.direction = 1

	def rotate(self):
		if self.direction == 1:
			x = self.positions[2][0]
			for index, pos in enumerate(self.positions):
				self.positions[index] = [x, pos[1] + index]
			self.direction = 2
		elif self.direction == 2:
			y = self.positions[2][1]
			for index, pos in enumerate(self.positions):
				if index < 2:
					self.positions[index] = [pos[0] - index, y]
				else:
					self.positions[index] = [pos[0] + index - 1, y]
			self.direction = 3