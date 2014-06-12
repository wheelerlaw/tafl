#!/usr/bin/env python
#Tested to be compatible with python 3.2 and 2.7 and pygame for those versions

import pygame,sys,math,random #tafl_ai
import pygame.locals as pygameLocals
import tafl_methods as methods 
#COLOUR and variable initialization
BACKGROUND = (175,175,175)
BLACK = (0,0,0)
GREEN = (50,255,50)
KING = (255,190,50)
SWEDES = (130,50,255)
MOSCUVITES = (255,50,50)
ESCAPE = (75,75,125)
THRONE = (66,66,66)

#create empty 9x9 grid
#grid = [[0 for x in range(9)] for x in range(9)]
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
valid_tile_selected = False
player_to_move = 1
player_1 = "human" # "human" or "machine"
player_2 = "human"
king_captured = False
king_escaped = False
game_over = False
#NOTE: Player1 = SWEDES Player2 = MOSCUVITES
def get_board():
	return grid
#same method as above but king may sit on throne and reaching an escape square returns "king_escape = True"
# initialize pygame
pygame.init( )
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
# setup the screen
screen = pygame.display.set_mode( scr_size )
pygame.display.set_caption( "Game Title" )
# load the background
background = pygame.Surface( scr_size )
background.fill(BACKGROUND)
screen.blit(background, (0,0) )
draw_legend(screen)
#visible mouse pointer
pygame.mouse.set_visible( True )
#start game clock
clock = pygame.time.Clock( )
#populate the board
grid = methods.setup_board()
#game loop
while True:  
	for event in pygame.event.get( ):
		if event.type == pygameLocals.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if grid[mouse_tile_x][mouse_tile_y].colour != BLACK or grid[mouse_tile_x][mouse_tile_y].colour != ESCAPE: # don't bother with empty squares
				if player_to_move == 1 and player_1 == "human": #PLAYER 1 TO MOVE
					#SWEDES SELECTED
					#tafl_ai.make_move(grid)
					if valid_tile_selected == False and grid[mouse_tile_x][mouse_tile_y].colour == SWEDES:
						grid[mouse_tile_x][mouse_tile_y].colour = methods.darken(grid[mouse_tile_x][mouse_tile_y].colour)
						methods.show_valid_moves( (mouse_tile_x,mouse_tile_y), grid )
						valid_tile_selected = True
						prev_x = mouse_tile_x
						prev_y = mouse_tile_y
					#KING SELECTED
					elif valid_tile_selected == False and grid[mouse_tile_x][mouse_tile_y].colour == KING:
						grid[mouse_tile_x][mouse_tile_y].colour = methods.darken(grid[mouse_tile_x][mouse_tile_y].colour)
						king_escaped = methods.show_valid_moves_KING( (mouse_tile_x,mouse_tile_y),grid )
						valid_tile_selected = True
						prev_x = mouse_tile_x
						prev_y = mouse_tile_y
					#UNSELECT TILE
					elif valid_tile_selected == True and prev_x == mouse_tile_x and prev_y == mouse_tile_y:
						grid[prev_x][prev_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						methods.hide_valid_moves(grid)
						valid_tile_selected = False
					#MOVE PIECE TO VALID SQUARE
					elif valid_tile_selected == True and grid[mouse_tile_x][mouse_tile_y].colour == GREEN:
						grid[mouse_tile_x][mouse_tile_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						grid[mouse_tile_x][mouse_tile_y].occ = True
						grid[prev_x][prev_y].colour = BLACK
						grid[prev_x][prev_y].occ = False
						methods.check_for_captured_MOSCUVITES(mouse_tile_x,mouse_tile_y,grid)
						prev_x = mouse_tile_x
						prev_y = mouse_tile_y
						valid_tile_selected = False
						methods.hide_valid_moves(grid)
						player_to_move = 2
					#MOVE PIECE TO INVALID SQUARE (same as UNSELECT TILE)
					elif valid_tile_selected == True and grid[mouse_tile_x][mouse_tile_y].colour != GREEN:
						grid[prev_x][prev_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						methods.hide_valid_moves(grid)
						valid_tile_selected = False
				elif player_to_move == 2 and player_2 == "human": #PLAYER 2 TO MOVE
					#MOSCUVITES SELECTED
					if valid_tile_selected == False and grid[mouse_tile_x][mouse_tile_y].colour == MOSCUVITES:
						grid[mouse_tile_x][mouse_tile_y].colour = methods.darken(grid[mouse_tile_x][mouse_tile_y].colour)
						methods.show_valid_moves( (mouse_tile_x,mouse_tile_y),grid )
						valid_tile_selected = True
						prev_x = mouse_tile_x
						prev_y = mouse_tile_y
					#UNSELECT TILE
					elif valid_tile_selected == True and prev_x == mouse_tile_x and prev_y == mouse_tile_y:
						grid[prev_x][prev_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						methods.hide_valid_moves(grid)
						valid_tile_selected = False
					#MOVE PIECE TO VALID SQUARE
					elif valid_tile_selected == True and grid[mouse_tile_x][mouse_tile_y].colour == GREEN:
						grid[mouse_tile_x][mouse_tile_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						grid[mouse_tile_x][mouse_tile_y].occ = True
						grid[prev_x][prev_y].colour = BLACK
						grid[prev_x][prev_y].occ = False
						king_captured = methods.check_for_captured_KING(mouse_tile_x,mouse_tile_y,grid)
						methods.check_for_captured_SWEDES(mouse_tile_x,mouse_tile_y,grid)
						prev_x = mouse_tile_x
						prev_y = mouse_tile_y
						valid_tile_selected = False
						methods.hide_valid_moves(grid)
						player_to_move = 1
					#MOVE PIECE TO INVALID SQUARE (same as UNSELECT TILE)
					elif valid_tile_selected == True and grid[mouse_tile_x][mouse_tile_y].colour != GREEN:
						grid[prev_x][prev_y].colour = methods.undarken(grid[prev_x][prev_y].colour)
						methods.hide_valid_moves(grid)
						valid_tile_selected = False
	#AI PLAYERS
		
	if player_to_move == 1 and player_1 == "machine":
		ai_move = methods.random_move_P1(grid)
		grid[ai_move[0]][ai_move[1]].colour = BLACK
		grid[ai_move[0]][ai_move[1]].occ = False
		grid[ai_move[2]][ai_move[3]].colour = SWEDES
		grid[ai_move[2]][ai_move[3]].occ = True
		#NEED TO ADD KING MOVEMENT
		methods.check_for_captured_MOSCUVITES(ai_move[2],ai_move[3],grid)
		player_to_move = 2
		
	if player_to_move == 2 and player_2 == "machine":
		# get move
		#tafl_ai.make_move(grid)
		ai_move = methods.random_move_P2(grid)
		grid[ai_move[0]][ai_move[1]].colour = BLACK
		grid[ai_move[0]][ai_move[1]].occ = False
		grid[ai_move[2]][ai_move[3]].colour = MOSCUVITES
		grid[ai_move[2]][ai_move[3]].occ = True
		king_captured = methods.check_for_captured_KING(ai_move[2],ai_move[3],grid)
		methods.check_for_captured_SWEDES(ai_move[2],ai_move[3],grid)
		player_to_move = 1
		
	if king_escaped:
		font = pygame.font.Font(None, 30)
		text = font.render("SWEDES win!", 1, SWEDES)
		screen.blit(text,( ((tile_width+tile_margin)*9 + 10),300) )
		game_over = True
		
	if king_captured:
		font = pygame.font.Font(None, 30)
		text = font.render("MOSCUVITES win!", 1, MOSCUVITES)
		screen.blit(text,( ((tile_width+tile_margin)*9 + 10),300) )
		game_over = True
	mouse_pos = pygame.mouse.get_pos()
	mouse_tile_x = mouse_pos[0] // (tile_width + tile_margin)
	mouse_tile_y = mouse_pos[1] // (tile_height + tile_margin)
	for x in range(9):
		for y in range(9):
			if y == mouse_tile_y and x == mouse_tile_x:
				pygame.draw.rect(screen,methods.undarken(grid[x][y].colour), [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])
			else:
				pygame.draw.rect(screen,grid[x][y].colour, [(tile_margin+tile_width)*x+tile_margin,(tile_margin+tile_height)*y+tile_margin,tile_width,tile_height])
	pygame.display.flip()
	time_passed = clock.tick( 60 )
