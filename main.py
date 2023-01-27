import pygame
from random import choice
from board import Board
from blocks import Cube, Rectangle

class TimeChecker():
	def __init__(self):
		self.prev_tick = 0
		self.sum_tick = 0

	def check_time(self, tick):
		if  (tick + self.sum_tick) - self.prev_tick >= 1000:
			self.prev_tick = 0
			self.sum_tick = 0
			return True
		self.sum_tick += tick
		return False

if __name__ == '__main__':
	colors = ["red", "green", "yellow"]
	blocks = [Cube, Rectangle]
	block = choice(blocks)(choice(colors))
	pygame.init()
	screen = pygame.display.set_mode((450, 720))
	clock = pygame.time.Clock()
	board = Board(10, 20)
	speedChecker = TimeChecker()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					block.move("RIGHT")
				elif event.key == pygame.K_LEFT:
					block.move("LEFT")
				elif event.key == pygame.K_DOWN:
					block.move("DOWN")
				elif event.key == pygame.K_UP:
					block.rotate()
		screen.fill("black")
		tick = clock.tick()
		if speedChecker.check_time(tick):
			block.fall()
		block_positions = block.get_positions()
		if block.isFall(board.minPoint(block_positions)):
			board.add_block(block_positions, block.get_color())
			block = choice(blocks)(choice(colors))
			board.update()
		block.render(screen)
		board.render(screen)
		pygame.display.flip()
	pygame.quit()