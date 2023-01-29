import pygame
from random import choice
from blocks import Cube, Rectangle, L_Block_1

BLOCKS = [Cube, Rectangle, L_Block_1]
Block = Rectangle | Cube | L_Block_1

def get_block() -> Block: 
	return choice(BLOCKS)()


class TimeChecker():
	def __init__(self):
		self.prev_tick = 0
		self.sum_tick = 0
		self.clock = pygame.time.Clock()

	def check_time(self) -> bool:
		tick = self.clock.tick()
		if  (tick + self.sum_tick) - self.prev_tick >= 1000:
			self.prev_tick = 0
			self.sum_tick = 0
			return True
		self.sum_tick += tick
		return False

class FPS():
	def __init__(self):
		self.clock = pygame.time.Clock()

	def render(self):
		print(self.clock.get_fps())