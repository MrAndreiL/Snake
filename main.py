#!\usr\bin\env python3
import pygame
import sys
import os
import random
import snake
import button
import food
import tail
pygame.init()



def main():

	# ------- Pre-sets --------.

	# Window settings.
	windowWidth = 1100
	windowHeigth = 800
	end_game_label = pygame.transform.scale(pygame.image.load("end_game.png"), (500, 500))
	start_screen = pygame.transform.scale(pygame.image.load("start_screen.png"), (300, 300))
	fireflake_logo = pygame.transform.scale(pygame.image.load("logo_fireflake.png"), (180, 180))
	start_logo = pygame.transform.scale(pygame.image.load("start_logo.png"), (300, 300))
	start_logo2 = pygame.transform.scale(pygame.image.load("start_logo2.png"), (300, 300))
	start_screenx = 400
	start_screeny = 50

	# Border settings.
	borderx = 235
	bordery = 85
	borderWidth = 630
	borderHeight = 630

	# Tile settings.
	tileWidth  = 35
	tileHeight = 35

	# Player settings.
	speed = 5
	foodobj = False
	foodobjx = 655
	foodobjy = 400

	score_font = pygame.font.SysFont("comicsansms", 45)

	# Frame settings.
	FPS = 60 # Recommended.
	clock = pygame.time.Clock()

	# COLORS.
	WHITE   = (255, 255, 255)
	BGC     = ( 20,  20,  23)
	FRUITC  = (255,   0,   0)
	PLAYERC = (  0, 153,   0)
	ODDC    = (255, 255, 255)
	EVENC   = ( 0,    0,   0)
	EXITB   = (255,   0,  64)

	# ------------------------.

	# Creating the surface.
	surface = pygame.display.set_mode((windowWidth, windowHeigth))
	pygame.display.set_caption("Snake game!")

	# Data structure for movement management.
	positions = []
	tails = []
	tail_goal_positions = []
	snake_body_xy = []
	player = snake.Snake(PLAYERC, 270, 400, tileWidth, tileHeight)
	food_NPC = food.Food(foodobjx, foodobjy, tileWidth, tileHeight, surface, FRUITC)
	food_NPC.add_pos(foodobjx, foodobjy)


	# Tile Creating.
	def draw_tiles():
		tile = 1
		for y in range(bordery, (bordery + borderHeight), tileHeight):
			tile -=1 # to prevent color bars TODO.
			for x in range(borderx, (borderx + borderWidth), tileWidth):
				positions.append([x, y])
				if tile % 2 == 0:
					pygame.draw.rect(surface, EVENC, (x, y, tileWidth, tileHeight))
				else:
					pygame.draw.rect(surface, ODDC, (x, y, tileWidth, tileHeight))
				tile += 1

	def score_label(score):
		score_text = score_font.render(f"Score: {score}", 1, WHITE)
		surface.blit(score_text, (0, 10))


	# Redraw function in main scope.
	def redraw(tail_nr = 0,score = 0,text = None):
		surface.fill(BGC) # fills the screen with background color.
		draw_tiles()
		score_label(score)
		player.draw(surface, positions)
		for e in range(0, tail_nr):
			tails[e].move(tail_goal_positions[e])
			tails[e].draw(surface)
		food_NPC.draw()
		pygame.draw.rect(surface, WHITE, (borderx, bordery, borderWidth, borderHeight), 1)
		if text is not None:
			surface.blit(text, (windowWidth // 2 - text.get_width() // 2, windowHeigth // 2 - text.get_height() // 2))
		clock.tick(FPS)
		pygame.display.update()


	def quit_event():
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


	def start_game_screen():
		run = True
		surface.fill(WHITE)
		font = pygame.font.Font("Purisa.ttf", 45)
		text = font.render("Classic Snake", 1, (0 , 0, 0))
		font = pygame.font.Font("Purisa.ttf", 30)
		name = font.render("by Lungu Andrei Sebastian", 1, (0 , 0, 0))
		while run:
			quit_event()
			surface.blit(text, (400, 350))
			surface.blit(name, (0, 730))
			surface.blit(start_screen, (start_screenx, start_screeny))
			surface.blit(fireflake_logo, (900, 600))
			if mouse_over_start():
				surface.blit(start_logo2, (415, 320))
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN:
						run = False
			else:
				surface.blit(start_logo, (415, 320))
			pygame.display.update()
		start()

	
	def mouse_over_start():
		mouse_pos = pygame.mouse.get_pos()
		if (415 <= mouse_pos[0] and mouse_pos[0] <= 715) and (420 <= mouse_pos[1] and mouse_pos[1] <= 520):
			return True
		return False 


	def mouse_over(buttonx, buttony, buttonWidth, buttonHeight):
		for event in pygame.event.get():
			mouse_pos = pygame.mouse.get_pos()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if buttonx <= mouse_pos[0] and mouse_pos[0] <= buttonx + buttonWidth:
					if buttony <= mouse_pos[1] and mouse_pos[1] <= buttony + buttonHeight:
						return True
			return False


	def move_tails(direction, tail_nr):
		for e in range(tail_nr - 1, 0, -1):
			tail_goal_positions[e] = tail_goal_positions[e - 1]
		tail_goal_positions[0] = direction


	def mark_positions(tail_nr):
		for e in range(0, tail_nr):
			pos = tails[e].get_tail_relative_pos()
			snake_body_xy[e].append(pos)
		print(snake_body_xy)


	def move(direction, currentx, currenty, run):
		if direction == 1:
			if currentx + tileWidth + speed > (borderx + borderWidth):
				run = False
			currentx += speed
			player.add_head(currentx, currenty)
		elif direction == 2:
			if currenty - speed < bordery:
				run = False
			currenty -= speed
			player.add_head(currentx, currenty)
		elif direction == 3:
			if currentx - speed < borderx:
				run = False
			currentx -= speed
			player.add_head(currentx, currenty)
		else:
			if currenty + tileHeight + speed > (bordery + borderHeight):
				run = False
			currenty += speed
			player.add_head(currentx, currenty)
		return run


	def fruit_collision(playerx, playery,direction, tail_nr, tailx, taily, taildirection, score = 0):
		foodx,foody = food_NPC.get_pos()
		if playerx == foodx and playery == foody:
			score += 10
			tail_nr += 1
			#print(taildirection)
			add_tail(tailx, taily, taildirection, tail_nr)
			respawn_food()
		return score,tail_nr

	def body_collision(run , playerx, playery):
		if [playerx, playery] in snake_body_xy:
			run = False
		return run


	def add_tail(tailx, taily, taildirection, tail_nr):
		if taildirection == 1:
			offsety = 0
			offsetx = -tileWidth
		elif taildirection == 2:
			offsetx = 0
			offsety = tileHeight
		elif taildirection == 3:
			offsety = 0
			offsetx = tileWidth
		else:
			offsetx = 0
			offsety = -tileHeight
		newx = tailx + offsetx
		newy = taily + offsety
		tail_obj = tail.Tail(newx, newy, PLAYERC, tileWidth, tileHeight, speed)
		tails.append(tail_obj)
		if tail_nr == 1:
			tail_goal_positions.append(taildirection)
		else:
			tail_goal_positions.append(tail_goal_positions[-1])
		

	def respawn_food():
		player_body = player.get_body()
		foodobjx,foodobjy = random.choice(positions)
		while [foodobjx,foodobjy] in player_body or [foodobjx, foodobjy] in snake_body_xy:
			foodobjx,foodobjy = random.choice(positions)
		food_NPC.add_pos(foodobjx, foodobjy)


	def start():
		positions = []
		player = snake.Snake(PLAYERC, 270, 400, tileWidth, tileHeight)
		start_font = pygame.font.SysFont("comicsansms", 50)
		score = 0
		run = True
		while run:
			text = start_font.render("Press -> to start....", 1, (255, 0, 0))
			redraw(score, text)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				k = pygame.key.get_pressed()
				if k[pygame.K_RIGHT]:
					run = False
		Food = True
		main_loop()


	def end_game():
		# Labels and buttons.
		end_gamex = end_game_label.get_width() // 2
		end_gamey = end_game_label.get_height() // 2

		# Exit button.
		exitx 	  = windowWidth // 2 + 80
		exity     = end_gamey + 180
		exitWidth = 100
		exitHeight = 50
		exit_button = button.Button(exitx, exity, exitWidth, exitHeight, EXITB, surface, "Exit!")

		# Replay button.
		replayx = windowWidth // 2 - 190
		replayy = exity
		replayWidth = 180
		replayHeight = 50
		replay_button = button.Button(replayx, replayy, replayWidth, replayHeight, EXITB, surface, "Play again!")

		run = True
		while run:
			quit_event()
			surface.blit(end_game_label, (windowWidth // 2 - end_gamex, windowHeigth // 2 - end_gamey))
			exit_button.draw_button()
			if mouse_over(exitx, exity, exitWidth, exitHeight):
				pygame.quit()
				sys.exit()
			pygame.display.update()


	def main_loop():
		# set direction.
		# 1 - right
		# 2 - up
		# 3 - left
		# 4 - down
		score = 0
		tail_nr = 0
		run = True
		direction = nextDirection = prevdirection = 1
		tailx = taily = 0
		while run:
			# Set directions based on key pressed.
			quit_event()
			currentx = player.get_headx()
			currenty = player.get_heady()
			keys = pygame.key.get_pressed()
			if tail_nr < 1:
				tailx,taily = currentx,currenty
				taildirection = prevdirection
			if direction == nextDirection:
				if keys[pygame.K_RIGHT] and direction != 3:
					nextDirection = 1
				elif keys[pygame.K_UP] and direction != 4:
					nextDirection = 2
				elif keys[pygame.K_LEFT] and direction != 1:
					nextDirection = 3
				elif keys[pygame.K_DOWN] and direction != 2:
					nextDirection = 4
			if [currentx, currenty] in positions:
				prevdirection = direction
				direction = nextDirection
				if tail_nr > 0:
					move_tails(prevdirection,tail_nr)
					tailx,taily = tails[-1].get_tail_pos()
					taildirection = tail_goal_positions[-1]
			score,tail_nr = fruit_collision(currentx, currenty,direction, tail_nr, tailx, taily, taildirection, score)
			run = move(direction, currentx, currenty, run)
			run = body_collision(run , currentx, currenty)
			redraw(tail_nr, score)
		end_game()
	start_game_screen()

if __name__ == "__main__":
	main()