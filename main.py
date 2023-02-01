import pygame
from constants import WIDTH, HEIGHT, SCORE
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
	score_text = MainText(435, 200, "Score:")
	lines_text = MainText(435, 250, "Lines:")
	lvl_text = MainText(435, 300, "Level:")
	score, rows, lvl = 0, 0, 0
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				block_positions = block.get_positions()
				sideEdges = board.sidePoints(block_positions)
				if event.key == pygame.K_RIGHT:
					block.move("RIGHT", sideEdges)
				elif event.key == pygame.K_LEFT:
					block.move("LEFT", sideEdges)
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
			new_rows = board.update()
			if new_rows:
				rows += new_rows
				score += SCORE[new_rows]
		block.render(screen)
		board.render(screen)
		fps.render(screen)
		title.render(screen)
		lines_text.render(screen, f"Lines: {rows}")
		score_text.render(screen,  f"Score: {score}")
		lvl_text.render(screen, f"Level: {lvl}")
		pygame.display.update()
		fps.clock.tick(60)
	pygame.quit()