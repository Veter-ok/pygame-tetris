import pygame
from constants import WIDTH, HEIGHT, SCORE
from board import Board
from tools import load_image, get_block, Input, TimeChecker, FPS, TitleText, MainText, DB_Controller

class App():
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Tetris")
		self.screen = pygame.display.set_mode((700, 720))
		self.record, self.score, self.rows, self.lvl = 0, 0, 0, 1
		self.running, self.gameIsStart, self.gameIsDefeat = True, False, False
		self.speedChecker = TimeChecker()
		self.dataBase = DB_Controller()
		self.logo_img = pygame.transform.scale(load_image('logo.jpg'), (700, 392))
		self.title = TitleText(470, 60, "Tetris")
		self.record_text = MainText(435, 200, "Record:")
		self.score_text = MainText(435, 250, "Score:")
		self.lines_text = MainText(435, 300, "Lines:") 
		self.lvl_text = MainText(435, 350, "Level:")
		self.tip = MainText(270, 350, "Tap space to play")
		self.input = Input(250, 290)
		self.fps = FPS()
		self.board = Board(WIDTH, HEIGHT)
		self.block = get_block()
	
	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				block_positions = self.block.get_positions()
				sideEdges = self.board.sidePoints(block_positions)
				if event.key == pygame.K_RIGHT:
					self.block.move("RIGHT", sideEdges)
				elif event.key == pygame.K_LEFT:
					self.block.move("LEFT", sideEdges)
				elif event.key == pygame.K_DOWN:
					self.block.move("DOWN")
				elif event.key == pygame.K_SPACE:
					if self.gameIsStart:
						min_points = self.board.minPoints(block_positions) 
						self.block.fast_down(min(min_points))
					else:
						self.board.reset_board()
						self.record_text.setPosition(435, 200)
						self.score_text.setPosition(435, 250)
						self.lines_text.setPosition(435, 300)
						self.lvl_text.setPosition(435, 350)
						self.score, self.rows, self.lvl = 0, 0, 1
						self.dataBase.addUser(self.input.get_text())
						self.record = self.dataBase.getRecord()
						self.gameIsStart, self.gameIsDefeat = True, False
				elif event.key == pygame.K_UP:
					self.block.rotate() 
				elif event.key == pygame.K_BACKSPACE and not self.gameIsStart and not self.gameIsDefeat:
					self.input.delete()
				elif not self.gameIsStart and not self.gameIsDefeat:
					self.input.add_symbol(event.unicode)
		
	def update(self):
		self.screen.fill("black")
		if self.speedChecker.check_time():
			self.block.fall()
		block_positions = self.block.get_positions()
		min_points = self.board.minPoints(block_positions)
		if self.block.isFall(min_points):
			if min(min_points) <= 1:
				self.record_text.setPosition(300, 300)
				self.lines_text.setPosition(300, 350)
				self.score_text.setPosition(300, 400)
				self.lvl_text.setPosition(300, 450)
				self.tip.setPosition(270, 520)
				self.gameIsStart, self.gameIsDefeat = False, True
				if self.score > self.dataBase.getRecord():
					self.dataBase.changeRecord(self.score)
					self.record = self.score
			self.board.add_block(block_positions, self.block.get_color())
			self.block = get_block()
			new_rows = self.board.update()
			if new_rows:
				self.rows += new_rows
				self.score += SCORE[new_rows]
				if self.lvl * 1000 <= self.score:
					self.lvl += 1
					self.speedChecker.increase_speed()

	def draw(self):
		self.block.render(self.screen)
		self.board.render(self.screen)
		self.fps.render(self.screen)
		self.title.render(self.screen)
		self.record_text.render(self.screen, f"Record: {self.record}")
		self.lines_text.render(self.screen, f"Lines: {self.rows}")
		self.score_text.render(self.screen,  f"Score: {self.score}")
		self.lvl_text.render(self.screen, f"Level: {self.lvl}")
	
	def run(self):
		while self.running:
			self.check_events()
			if self.gameIsStart and not self.gameIsDefeat:
				self.update()
				self.draw()
			else:
				self.screen.fill("black")
				self.screen.blit(self.logo_img, (0, 0))
				self.tip.render(self.screen)
				if self.gameIsDefeat:
					self.record_text.render(self.screen, f"Record: {self.record}")
					self.lines_text.render(self.screen, f"Lines: {self.rows}")
					self.score_text.render(self.screen,  f"Score: {self.score}")
					self.lvl_text.render(self.screen, f"Level: {self.lvl}")
				else:
					self.input.render(self.screen)
			pygame.display.update()
			self.fps.clock.tick(60)


if __name__ == '__main__':
	app = App()
	app.run()