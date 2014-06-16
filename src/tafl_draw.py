#!/usr/bin/env python
#Tested to be compatible with python 3.2 and 2.7 and pygame for those versions
import pygame,sys,math,random, time, tafl
from pygame.locals import *

#COLOUR and variable initialization
BACKGROUND = (175,175,175)
BLACK = (0,0,0)
GREEN = (50,255,50)
KING = (255,190,50)
SWEDES = (130,50,255)
MOSCUVITES = (255,50,50)
ESCAPE = (75,75,125)
THRONE = (66,66,66)

# FPS
FPS = 60

#tile dimensions (visual purposes)
tile_height = 64
tile_width = 64
tile_margin = 1
legend_size = 200

#screen size based on tile dimensions
scr_size = ( (tile_width+tile_margin)*9 + legend_size, (tile_height+tile_margin)*9)

#initialize mouse pos
mouse_tile_x = 0 
mouse_tile_y = 0
valid_selected = False

class Player:
	def __init__(self, player, human=True):
		self.player = player # 1 or 2
		self.human = human # true or false

def draw_board(screen,game,selected_coords):
	xx = selected_coords[0]
	yy = selected_coords[1]

	# draw empty board
	for x in range(game.size):
		for y in range(game.size):
			pygame.draw.rect(screen, BLACK, [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])
	
	# draw escape squares
	for i in range((len(game.escape_coords))):
		x = game.escape_coords[i][0]
		y = game.escape_coords[i][1]
		pygame.draw.rect(screen, ESCAPE, [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])

	# draw throne
	pygame.draw.rect(screen, THRONE, [(tile_margin+tile_width)*4+tile_margin,(tile_margin+tile_height)*4+tile_margin,tile_width,tile_height])	
	
	# draw pieces
	pieces = game.current_board.game_pieces
	for i in range((len(pieces))):
		x = pieces[i].x
		y = pieces[i].y
		colour = MOSCUVITES
		if pieces[i].player == 1:
			colour = SWEDES
		elif pieces[i].player == 3:
			colour = KING
		# hover colour
		if xx == x and yy == y:
			colour = undarken(colour)
		pygame.draw.rect(screen, colour, [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])


def draw_legend(screen):
	x_value = (tile_width+tile_margin)*9 + legend_size//6
	font = pygame.font.Font(None, 24)
	text = font.render("Empty", 1, BLACK)
	screen.blit(text,(x_value + 30,72))
	pygame.draw.rect(screen,BLACK, (x_value, 70, 20, 20))
	text = font.render("Legal Move", 1, GREEN)
	screen.blit(text,(x_value + 30,102))
	pygame.draw.rect(screen,GREEN, (x_value, 100, 20, 20))
	text = font.render("King", 1, KING)
	screen.blit(text,(x_value + 30,132))
	pygame.draw.rect(screen,KING, (x_value, 130, 20, 20))
	text = font.render("Swede", 1, SWEDES)
	screen.blit(text,(x_value + 30,162))
	pygame.draw.rect(screen,SWEDES, (x_value, 160, 20, 20))
	text = font.render("Moscuvite", 1, MOSCUVITES)
	screen.blit(text,(x_value + 30,192))
	pygame.draw.rect(screen,MOSCUVITES, (x_value, 190, 20, 20))
	text = font.render("Escape", 1, ESCAPE)
	screen.blit(text,(x_value + 30,222))
	pygame.draw.rect(screen,ESCAPE, (x_value, 220, 20, 20))
	text = font.render("Throne", 1, THRONE)
	screen.blit(text,(x_value + 30,252))
	pygame.draw.rect(screen,THRONE, (x_value, 250, 20, 20))

# initialize pygame
pygame.init()

# setup the screen
screen = pygame.display.set_mode( scr_size )
pygame.display.set_caption( "Game Title" )

# load the background and legend
background = pygame.Surface( scr_size )
background.fill(BACKGROUND)
screen.blit(background, (0,0) )
draw_legend(screen)

 # visible mouse pointer
pygame.mouse.set_visible( True )

# start a new game
game = tafl.Game()

# create players (add "False" argument to use ai)
player_1 = Player(1)
player_2 = Player(2)

# start game clock
clock = pygame.time.Clock( )

#GAME LOOP
while True:

	for event in pygame.event.get( ):
		if event.type == QUIT:
			sys.exit() # window closed, quit
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if player_1.human and game.player == 1:
				pass
			elif player_2.human and game.player == 2:
				pass
				

	#AI PLAYERS
	if game.player == 1 and not player_1.human:
		timer = time.clock()
		# DO AI MOVE HERE
		timer = time.clock()-timer
		print("Seconds to calculate: ",timer)
		player_2.to_move = False
		player_1.to_move = True

	if game.player == 2 and not player_2.human:
		time1 = time.clock()
		# DO AI MOVE HERE
		time2 = time.clock()
		think_time = time2 - time1
		print("Seconds to calculate: ", think_time)
		player_2.to_move = False
		player_1.to_move = True
	
	# game over
	if game.over:
		pass

	# get mouse position
	mouse_pos = pygame.mouse.get_pos()
	mouse_tile_x = mouse_pos[0] // (tile_width + tile_margin)
	mouse_tile_y = mouse_pos[1] // (tile_height + tile_margin)

	# draw board
	draw_board(screen, game, (mouse_tile_x,mouse_tile_y))
	
	# refresh
	pygame.display.flip()

	# tick the clock at FPS
	time_passed = clock.tick( FPS )
