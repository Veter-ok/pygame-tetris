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


class MainBlock():
	def __init__(self, color:str):
		self.color = color
		self.direction = 1

	def get_positions(self) -> list:
		return self.positions
	
	def get_color(self) -> str:
		return self.color

	def render(self, screen):
		for position in self.positions:
			pos = boardPosToPixels(position)
			pygame.draw.rect(screen, self.color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

	def __is_edge(self, direction:str, edges:list[list[int]]):
		for index, edge in enumerate(edges):
			if direction == "LEFT" and abs(self.positions[index][0] - edge[0]) == 1:
				return False
			elif direction == "RIGHT" and abs(self.positions[index][0] - edge[1]) == 1:
				return False
		return True

	def move(self, pos:str, edges:list[list[int]]=[]):
		if pos == "RIGHT" and self.__is_edge(pos, edges):
			for index in range(len(self.positions)):
				x, y = self.positions[index]
				self.positions[index] = (x + 1, y)
		elif pos == "LEFT" and self.__is_edge(pos, edges):
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
	
	def isFall(self, all_y:list) -> bool:
		for index, pos in enumerate(self.positions):
			if all_y[index] == pos[1]:
				return True
		return False


class Cube(MainBlock):
	color = (242, 240, 0)

	def __init__(self): 
		super().__init__(Cube.color)
		self.positions = [(3, 0), (4, 0), (3, 1), (4, 1)]

	def rotate(self):
		pass


class Rectangle(MainBlock):
	color = (4, 241, 229)

	def __init__(self):
		super().__init__(Rectangle.color) 
		self.positions = [(3, 0), (4, 0), (5, 0), (6, 0)]

	def rotate(self):
		if self.direction == 1:
			x = self.positions[2][0]
			self.positions[0] = [x, self.positions[0][1] - 2]
			self.positions[1] = [x, self.positions[1][1] - 1]
			self.positions[2] = [x, self.positions[2][1]]
			self.positions[3] = [x, self.positions[3][1] + 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[2]
			if x + 1 == WIDTH:
				self.positions[0] = [x - 3, y]
				self.positions[1] = [x - 2, y] 
				self.positions[2] = [x - 1, y]
				self.positions[3] = [x, y]
			elif x == 0:
				self.positions[0] = [x, y]
				self.positions[1] = [x + 1, y] 
				self.positions[2] = [x + 2, y]
				self.positions[3] = [x + 3, y]
			else:
				self.positions[0] = [x - 2, y]
				self.positions[1] = [x - 1, y] 
				self.positions[2] = [x, y]
				self.positions[3] = [x + 1, y]
			self.direction = 3
		elif self.direction == 3:
			x = self.positions[1][0]
			self.positions[0] = [x, self.positions[0][1] - 1]
			self.positions[1] = [x, self.positions[1][1]]
			self.positions[2] = [x, self.positions[2][1] + 1]
			self.positions[3] = [x, self.positions[3][1] + 2]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[1]
			if x + 1 == WIDTH:
				self.positions[0] = [x - 3, y]
				self.positions[1] = [x - 2, y] 
				self.positions[2] = [x - 1, y]
				self.positions[3] = [x, y]
			elif x == 0:
				self.positions[0] = [x, y]
				self.positions[1] = [x + 1, y] 
				self.positions[2] = [x + 2, y]
				self.positions[3] = [x + 3, y]
			else:
				self.positions[0] = [x - 1, y]
				self.positions[1] = [x, y] 
				self.positions[2] = [x + 1, y]
				self.positions[3] = [x + 2, y]
			self.direction = 1


class L_Block_1(MainBlock):
	color = (26, 0, 217)

	def __init__(self):
		super().__init__(L_Block_1.color)
		self.positions = [(3, 0), (3, 1), (4, 1), (5, 1)]
	
	def rotate(self):
		if self.direction == 1:
			x, y = self.positions[2]
			self.positions[0] = [x + 1, y - 1]
			self.positions[1] = [x, y - 1]
			self.positions[3] = [x, y + 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[2]
			if x == 0:
				self.positions[0] = [x + 2, y + 1]
				self.positions[1] = [x + 2, y]
				self.positions[2] = [x + 1, y]
				self.positions[3] = [x, y]
			else:
				self.positions[0] = [x + 1, y + 1]
				self.positions[1] = [x + 1, y]
				self.positions[3] = [x - 1, y]
			self.direction = 3
		elif self.direction == 3:
			x, y = self.positions[2]
			self.positions[0] = [x - 1, y + 1]
			self.positions[1] = [x, y + 1]
			self.positions[3] = [x, y - 1]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[2]
			if x == WIDTH - 1:
				self.positions[0] = [x - 2, y - 1]
				self.positions[1] = [x - 2, y]
				self.positions[2] = [x - 1, y]
				self.positions[3] = [x, y]
			else:
				self.positions[0] = [x - 1, y - 1]
				self.positions[1] = [x - 1, y]
				self.positions[3] = [x + 1, y]
			self.direction = 1


class L_Block_2(MainBlock):
	color = (214, 144, 5)

	def __init__(self):
		super().__init__(L_Block_2.color)
		self.positions = [(3, 1), (4, 1), (5, 1), (5, 0)]

	def rotate(self):
		if self.direction == 1:
			x, y = self.positions[1]
			self.positions[0] = [x + 1, y + 1]			
			self.positions[2] = [x, y + 1]
			self.positions[3] = [x, y - 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[1]
			if x == 0:
				self.positions[0] = [x + 2, y]
				self.positions[1] = [x + 1, y]
				self.positions[2] = [x, y]
				self.positions[3] = [x, y + 1]
			else:
				self.positions[0] = [x + 1, y]	 
				self.positions[2] = [x - 1, y]
				self.positions[3] = [x - 1, y + 1]
			self.direction = 3
		elif self.direction == 3:
			x, y = self.positions[1]
			self.positions[0] = [x, y - 1]
			self.positions[2] = [x, y + 1]
			self.positions[3] = [x - 1, y - 1]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[1]
			if x == WIDTH - 1:
				self.positions[0] = [x - 2, y]
				self.positions[1] = [x - 1, y]
				self.positions[2] = [x, y]
				self.positions[3] = [x, y - 1]
			else:
				self.positions[0] = [x - 1, y]
				self.positions[2] = [x + 1, y]
				self.positions[3] = [x + 1, y - 1]
			self.direction = 1


class Z_Block_1(MainBlock):
	color = (240, 1, 1)

	def __init__(self):
		super().__init__(Z_Block_1.color)
		self.positions = [(3, 0), (4, 0), (4, 1), (5, 1)]
	
	def rotate(self):
		if self.direction == 1:
			x, y = self.positions[2]
			self.positions[0] = [x + 1, y - 1]
			self.positions[1] = [x + 1, y]
			self.positions[3] = [x, y + 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[2]
			if x == 0:
				self.positions[0] = [x, y - 1]
				self.positions[1] = [x + 1, y - 1]
				self.positions[2] = [x + 1, y]
				self.positions[3] = [x + 2, y]
			else:
				self.positions[0] = [x - 1, y - 1]
				self.positions[1] = [x, y - 1]
				self.positions[3] = [x + 1, y]
			self.direction = 3
		elif self.direction == 3:
			x, y = self.positions[1]
			self.positions[0] = [x, y - 1]
			self.positions[2] = [x - 1, y]
			self.positions[3] = [x - 1, y + 1]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[1]
			if x == WIDTH - 1:
				self.positions[0] = [x - 2, y]
				self.positions[1] = [x - 1, y]
				self.positions[2] = [x - 1, y + 1]
				self.positions[3] = [x, y + 1]
			else:
				self.positions[0] = [x - 1, y]
				self.positions[2] = [x, y + 1]
				self.positions[3] = [x + 1, y + 1]
			self.direction = 1


class Z_Block_2(MainBlock):
	color = (0, 242, 1)

	def __init__(self):
		super().__init__(Z_Block_2.color)
		self.positions = [(3, 1), (4, 1), (4, 0), (5, 0)]

	def rotate(self):
		if self.direction == 1:
			x, y = self.positions[1]
			self.positions[0] = [x, y - 1]
			self.positions[2] = [x + 1, y]
			self.positions[3] = [x + 1, y + 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[1]
			if x == 0:
				self.positions[0] = [x, y]
				self.positions[1] = [x + 1, y]
				self.positions[2] = [x + 1, y - 1]
				self.positions[3] = [x + 2, y - 1]
			else:
				self.positions[0] = [x - 1, y]
				self.positions[2] = [x, y - 1]
				self.positions[3] = [x + 1, y - 1]
			self.direction = 3
		elif self.direction == 3:
			x, y = self.positions[2]
			self.positions[0] = [x - 1, y - 1]
			self.positions[1] = [x - 1, y]
			self.positions[3] = [x, y + 1]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[2]
			if x == WIDTH - 1:
				self.positions[0] = [x - 2, y + 1]
				self.positions[1] = [x - 1, y + 1]
				self.positions[2] = [x - 1, y]
				self.positions[3] = [x, y]
			else:
				self.positions[0] = [x - 1, y + 1]
				self.positions[1] = [x, y + 1]
				self.positions[3] = [x + 1, y]
			self.direction = 1


class T_Block(MainBlock):
	color = (152, 2, 241)

	def __init__(self):
		super().__init__(T_Block.color)
		self.positions = [(3, 1), (4, 1), (4, 0), (5, 1)]

	def rotate(self):
		if self.direction == 1:
			x, y = self.positions[1]
			self.positions[0] = [x, y - 1]
			self.positions[2] = [x + 1, y]
			self.positions[3] = [x, y + 1]
			self.direction = 2
		elif self.direction == 2:
			x, y = self.positions[1]
			if x == 0:
				self.positions[0] = [x, y]
				self.positions[1] = [x + 1, y]
				self.positions[2] = [x + 1, y + 1]
				self.positions[3] = [x + 2, y]
			else:
				self.positions[0] = [x - 1, y]
				self.positions[2] = [x, y + 1]
				self.positions[3] = [x + 1, y]
			self.direction = 3
		elif self.direction == 3:
			x, y = self.positions[1]
			self.positions[0] = [x, y - 1]
			self.positions[2] = [x - 1, y]
			self.positions[3] = [x, y + 1]
			self.direction = 4
		elif self.direction == 4:
			x, y = self.positions[1]
			if x == WIDTH - 1:
				self.positions[0] = [x - 2, y + 1]
				self.positions[1] = [x - 1, y]
				self.positions[2] = [x - 1, y + 1]
				self.positions[3] = [x, y + 1]
			else:
				self.positions[0] = [x - 1, y + 1]
				self.positions[2] = [x, y + 1]
				self.positions[3] = [x + 1, y + 1]
			self.direction = 1