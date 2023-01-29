import pygame
from constants import WIDTH, HEIGHT
from board import Board
from tools import get_block, TimeChecker, FPS

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((450, 720))
	board = Board(WIDTH, HEIGHT)
	block = get_block()
	speedChecker = TimeChecker()
	fps = FPS()
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
		pygame.display.update()
		# fps.render()
		fps.clock.tick(60)
	pygame.quit()