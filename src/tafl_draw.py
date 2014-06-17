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
mouse_coords = ()
selected_coords = ()

class Player:
	def __init__(self, player, human=True):
		self.player = player # 1 or 2
		self.human = human # true or false

def darken(colour):
	r = colour[0]
	g = colour[1]
	b = colour[2]
	return (max(r-50,0),max(g-50,0),max(b-50,0))
def undarken(colour):
	r = colour[0]
	g = colour[1]
	b = colour[2]
	return (min(r+50,255),min(g+50,255),min(b+50,255))

def draw_board(screen,game,hover_coords,selected_coords):
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
		piece_coords = (x,y)
		colour = MOSCUVITES
		if pieces[i].player == 1:
			colour = SWEDES
		elif pieces[i].player == 3:
			colour = KING
		# selected piece colouring
		if selected_coords == piece_coords:
			colour = darken(colour)
		# hovered piece colouring
		if hover_coords == piece_coords:
			colour = undarken(colour)
		pygame.draw.rect(screen, colour, [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])

def draw_valid_moves(screen,game,hover_coords,selected_coords):
	valid_moves = game.current_board.get_possible_next_coords(selected_coords)
	for i in range(len(valid_moves)):
		x = valid_moves[i][0]
		y = valid_moves[i][1]
		colour = GREEN
		# hover colouring
		if valid_moves[i] == hover_coords:
			colour = undarken(GREEN)
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
pygame.display.set_caption( "Tafl" )

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
while not game.over:

	for event in pygame.event.get( ):
		if event.type == QUIT:
			sys.exit() # window closed, quit
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# move or unselect the piece
			if selected_coords:
				# if valid move, do it
				valid_moves = game.current_board.get_possible_next_coords(selected_coords)
				for i in range(len(valid_moves)) :
					if mouse_coords == valid_moves[i]:
						print(game.make_move(selected_coords, mouse_coords, game.player))
				# if any click is made, the piece should be unselected
				selected_coords = ()

			# try to select a piece
			elif game.current_board.is_piece(mouse_coords):
					# if it is a piece, check if its the correct player. if so, select it
					piece = game.current_board.get_piece(mouse_coords)
					if piece.player == game.player or (piece.player == 3 and game.player == 1):
						selected_coords = mouse_coords

	#AI PLAYERS
	if game.player == 1 and not player_1.human:
		timer = time.clock()
		# DO AI MOVE HERE
		timer = time.clock()-timer
		print("Seconds to calculate: ",timer)
		game.player = 2

	if game.player == 2 and not player_2.human:
		time1 = time.clock()
		# DO AI MOVE HERE
		time2 = time.clock()
		think_time = time2 - time1
		print("Seconds to calculate: ", think_time)
		game.player = 1

	# get mouse position
	mouse_pos = pygame.mouse.get_pos()
	mouse_coords = (mouse_pos[0] // (tile_width + tile_margin), mouse_pos[1] // (tile_height + tile_margin))

	# draw board
	draw_board(screen, game, mouse_coords, selected_coords)
	if selected_coords:
		draw_valid_moves(screen, game, mouse_coords, selected_coords)
	
	# refresh
	pygame.display.flip()

	# tick the clock at FPS
	time_passed = clock.tick( FPS )

print("game over")
sys.exit()