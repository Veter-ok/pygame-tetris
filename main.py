import pygame
from constants import WIDTH, HEIGHT, SCORE
from board import Board
from tools import get_block, TimeChecker, FPS, TitleText, MainText

class App():
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((700, 720))
		self.score, self.rows, self.lvl = 0, 0, 1
		self.running = True
		self.gameIsStart, self.gameIsDefeat = False, False
		self.speedChecker = TimeChecker()
		self.title = TitleText(470, 60, "Tetris")
		self.score_text = MainText(435, 200, "Score:")
		self.lines_text = MainText(435, 250, "Lines:")
		self.lvl_text = MainText(435, 300, "Level:")
		self.label = TitleText(280, 200, "Tetris")
		self.tip = MainText(270, 350, "Tap space to play")
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
						self.score_text.setPosition(435, 200)
						self.lines_text.setPosition(435, 250)
						self.lvl_text.setPosition(435, 300)
						self.score, self.rows, self.lvl = 0, 0, 1
						self.gameIsStart, self.gameIsDefeat = True, False
				elif event.key == pygame.K_UP:
					self.block.rotate() 
		
	def update(self):
		self.screen.fill("black")
		if self.speedChecker.check_time():
			self.block.fall()
		block_positions = self.block.get_positions()
		min_points = self.board.minPoints(block_positions)
		if self.block.isFall(min_points):
			if min(min_points) <= 1:
				self.lines_text.setPosition(205, 300)
				self.score_text.setPosition(305, 300)
				self.lvl_text.setPosition(405, 300)
				self.tip.setPosition(270, 370)
				self.gameIsStart, self.gameIsDefeat = False, True
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
				self.label.render(self.screen)
				self.tip.render(self.screen)
				if self.gameIsDefeat:
					self.lines_text.render(self.screen, f"Lines: {self.rows}")
					self.score_text.render(self.screen,  f"Score: {self.score}")
					self.lvl_text.render(self.screen, f"Level: {self.lvl}")
			pygame.display.update()
			self.fps.clock.tick(60)



if __name__ == '__main__':
	app = App()
	app.run()