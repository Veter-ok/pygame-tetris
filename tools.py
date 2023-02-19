import pygame
import os
from random import choice
from blocks import Cube, Rectangle, L_Block_1, L_Block_2, Z_Block_1, Z_Block_2, T_Block

BLOCKS = [Cube, Rectangle, L_Block_1, L_Block_2, Z_Block_1, Z_Block_2, T_Block]
Block = Rectangle | Cube | L_Block_1 | L_Block_2 | Z_Block_1 | Z_Block_2 | T_Block

def get_block() -> Block: 
	return choice(BLOCKS)()


class TitleText():
	def __init__(self, x:int, y:int, text:str):
		self.font = pygame.font.SysFont("Arial", 50)
		self.x = x
		self.y = y
		self.default_text = text

	def render(self, screen, text:str=None):
		if text:
			self.text = self.font.render(text, True, (255, 255, 255))
		else:
			self.text = self.font.render(self.default_text, True, (255, 255, 255))
		screen.blit(self.text, (self.x, self.y))


class MainText():
	def __init__(self, x:int, y:int, text:str):
		self.font = pygame.font.SysFont("Arial", 20)
		self.x = x
		self.y = y
		self.default_text = text

	def render(self, screen, text=None):
		if text:
			self.text = self.font.render(text, True, (255, 255, 255))
		else:
			self.text = self.font.render(self.default_text, True, (255, 255, 255))
		screen.blit(self.text, (self.x, self.y))
	
	def setPosition(self, x:int, y:int):
		self.x = x
		self.y = y


class TimeChecker():
	def __init__(self):
		self.prev_tick = 0
		self.sum_tick = 0
		self.clock = pygame.time.Clock()
		self.delay = 1000

	def check_time(self) -> bool:
		tick = self.clock.tick()
		if  (tick + self.sum_tick) - self.prev_tick >= self.delay:
			self.prev_tick = 0
			self.sum_tick = 0
			return True
		self.sum_tick += tick
		return False
	
	def increase_speed(self):
		self.delay = self.delay * 0.75


class FPS():
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.text = MainText(640, 680, str(round(self.clock.get_fps(),2)))

	def render(self, screen):
		self.text.render(screen, str(round(self.clock.get_fps(),2)))