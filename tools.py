import pygame
import os
import sqlite3
from random import choice
from blocks import Cube, Rectangle, L_Block_1, L_Block_2, Z_Block_1, Z_Block_2, T_Block

BLOCKS = [Cube, Rectangle, L_Block_1, L_Block_2, Z_Block_1, Z_Block_2, T_Block]
Block = Rectangle | Cube | L_Block_1 | L_Block_2 | Z_Block_1 | Z_Block_2 | T_Block

def get_block() -> Block: 
	return choice(BLOCKS)()

def load_image(name, color_key=None):
    fullname = os.path.join('imgs', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Input():
	def __init__(self, x:int, y:int):
		self.x = x
		self.y = y
		self.input_rect = pygame.Rect(x, y, 200, 42)
		self.base_font = pygame.font.SysFont("Arial", 24)
		self.text = ''
	
	def get_text(self) -> str:
		return self.text

	def add_symbol(self, symbol:str):
		if len(self.text) < 15:
			self.text += symbol
	
	def delete(self):
		self.text = self.text[:-1]
	
	def render(self, screen):
		pygame.draw.rect(screen, (255, 255, 0), self.input_rect, 1)
		if self.text == '':
			text_surface = self.base_font.render('Enter your name', True, (255, 255, 255))
		else:
			text_surface = self.base_font.render(self.text, True, (255, 255, 255))
		screen.blit(text_surface, (self.x + 9, self.y + 9))


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
	
	def setText(self, text:str):
		self.default_text = text


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


class DB_Controller:
	def __init__(self):
		self.connection = sqlite3.connect("Pygame.db")
		self.cursor = self.connection.cursor()
		self.__createTables()
		
	def __createTables(self):
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
								"nickname"	TEXT NOT NULL UNIQUE,
								"record" INTEGER  NOT NULL
							);""")
	
	def addUser(self, nickname:str):
		try:
			self.cursor.execute("""INSERT INTO users(nickname, record) VALUES(?, ?)""", (nickname, 0, ))
			self.nickname = nickname
			self.connection.commit()
		except sqlite3.IntegrityError:
			self.nickname = nickname
	
	def getRecord(self) -> int:
		record = self.cursor.execute("SELECT record FROM users WHERE nickname=?", (self.nickname, )).fetchall()
		return record[0][0]

	def changeRecord(self, new_record:int):
		self.cursor.execute("UPDATE users SET record=? WHERE nickname=?", (new_record, self.nickname))
		self.connection.commit()