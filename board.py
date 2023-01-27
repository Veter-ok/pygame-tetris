import pygame
from constants import MARGIN_TOP, MARGIN_LEFT, CELL_SIZE

def boardPosToPixels(pos):
	left, top, cell_size = MARGIN_LEFT, MARGIN_TOP, CELL_SIZE
	x, y = pos
	return (x * cell_size + left, y * cell_size + top)


class Board():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.board = [[0] * width for _ in range(height)]
		self.board_colors = [[0] * width for _ in range(height)]
		self.symbol = 0
		self.left = MARGIN_LEFT
		self.top = MARGIN_TOP
		self.cell_size = CELL_SIZE

	def set_view(self, left, top, cell_size):
		self.left = left
		self.top = top
		self.cell_size = cell_size

	def get_cell(self, mouse_pos):
		x, y = mouse_pos
		x -= self.left
		y -= self.top
		width = self.cell_size * self.width
		height = self.cell_size * self.height
		if x > width or x < 0 or y > height or y < 0:
			return None
		return x // self.cell_size, y // self.cell_size

	def render(self, screen):
		for y in range(self.height):
			for x in range(self.width):
				if self.board[y][x] == 1:
					self.fill_cell(screen, (x, y), self.board_colors[y][x])
				pygame.draw.rect(screen, "white", (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

	def update(self):
		while [1] * self.width in self.board:
			full_row = 0
			for y, row in enumerate(self.board):
				if row == [1] * self.width:
					full_row = y
					break
			index = full_row
			while index != 0:
				self.board[index] = self.board[index - 1].copy()
				index -= 1

					
	def add_block(self, postions, color):
		for postion in postions:
			x, y = postion
			self.board[y][x] = 1
			self.board_colors[y][x] = color
	
	def minPoint(self, postions):
		min_points = []
		for y in range(self.height):
			for pos in postions:
				if self.board[y][pos[0]] == 1:
					min_points.append(y)
		if len(min_points) == 0:
			return self.height - 1
		return min(min_points) - 1
	
	def fill_cell(self, screen, pos, color):
		pos = boardPosToPixels(pos)
		pygame.draw.rect(screen, color, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))