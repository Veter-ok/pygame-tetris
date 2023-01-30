import pygame
from constants import WIDTH, HEIGHT
from board import Board
from tools import get_block, TimeChecker, FPS, TitleText, MainText

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((700, 720))
	board = Board(WIDTH, HEIGHT)
	block = get_block()
	speedChecker = TimeChecker()
	fps = FPS()
	title = TitleText(470, 60, "Tetris")
	points_text = MainText(435, 200, "Points:")
	lines_text = MainText(435, 250, "Lines:")
	lvl_text = MainText(435, 300, "Level:")
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
		if speedChecker.check_time():
			block.fall()
		block_positions = block.get_positions()
		if block.isFall(board.minPoints(block_positions)):
			board.add_block(block_positions, block.get_color())
			block = get_block()
			board.update()
		block.render(screen)
		board.render(screen)
		fps.render(screen)
		title.render(screen)
		lines_text.render(screen)
		lvl_text.render(screen)
		points_text.render(screen)
		pygame.display.update()
		fps.clock.tick(60)
	pygame.quit()