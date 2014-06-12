#!/usr/bin/env python
import math, random
BACKGROUND = (175,175,175)
BLACK = (0,0,0)
GREEN = (50,255,50)
KING = (255,190,50)
SWEDES = (130,50,255)
MOSCUVITES = (255,50,50)
ESCAPE = (75,75,125)
THRONE = (66,66,66)
class Tile:
	def __init__ (self, coords=(0,0), tile_type="normal", occupied=False, tile_colour=BLACK):
		self.x = coords[0]
		self.y = coords[1]
		self.type = tile_type
		self.occ = occupied
		self.colour = tile_colour
# class Board:
# 	def __init__ (self, list_of_tiles)
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
def setup_board():
	#initialize empty squares
	grid = [[0 for x in range(9)] for x in range(9)]
	for row in range(9):
		for column in range(9):
			grid[row][column] = Tile((column,row))
	#initialze "king" piece
	grid[4][4].type = "throne"
	grid[4][4].colour = KING
	grid[4][4].occ = True
	#initialize "swedes" in throne adjacent
	for x in range (3,6):
		for y in range (3,6):
			if math.fabs(x-y) == 1:
				grid[x][y].type = "throne_adjacent"
				grid[x][y].colour = SWEDES
				grid[x][y].occ = True
	#initialize last 4 "swedes"
	grid[4][2].colour = SWEDES
	grid[4][2].occ = True
	grid[4][6].colour = SWEDES
	grid[4][6].occ = True
	grid[2][4].colour = SWEDES
	grid[2][4].occ = True
	grid[6][4].colour = SWEDES
	grid[6][4].occ = True
	#initialize "moscuvites"
	for x in range(9):
		for y in range(9):
			if ((x == 0 or x == 8) and (3 <= y and 5>= y)) or ((y == 0 or y == 8) and (3 <= x and 5 >= x)):
					grid[x][y].colour = MOSCUVITES
					grid[x][y].occ = True
	#initialize last 4 "moscuvites"
	grid[4][1].colour = MOSCUVITES
	grid[4][1].occ = True
	grid[4][7].colour = MOSCUVITES
	grid[4][7].occ = True
	grid[1][4].colour = MOSCUVITES
	grid[1][4].occ = True
	grid[7][4].colour = MOSCUVITES
	grid[7][4].occ = True
	#initialze escape tiles, NOTE: considered occupied because no piece will ever occupy or pass through
	grid[0][0].type = "escape"
	grid[0][0].colour = ESCAPE
	grid[0][0].occ = True
	grid[0][8].type = "escape"
	grid[0][8].colour = ESCAPE
	grid[0][8].occ = True
	grid[8][0].type = "escape"
	grid[8][0].colour = ESCAPE
	grid[8][0].occ = True
	grid[8][8].type = "escape"
	grid[8][8].colour = ESCAPE
	grid[8][8].occ = True
	return grid
def show_valid_moves(coords, grid):
	x = coords[0]
	y = coords[1]
	for i in range (x+1,9):
		if grid[i][y].occ == True:
			break
		if grid[i][y].type == "throne":
			continue
		else:
			grid[i][y].colour = GREEN
	for i in range (x-1,-1,-1):
		if grid[i][y].occ == True:
			break
		if grid[i][y].type == "throne":
			continue
		else:
			grid[i][y].colour = GREEN		
	for i in range (y+1,9):
		if grid[x][i].occ == True:
			break
		if grid[x][i].type == "throne":
			continue
		else:
			grid[x][i].colour = GREEN
	for i in range (y-1,-1,-1):
		if grid[x][i].occ == True:
			break
		if grid[x][i].type == "throne":
			continue
		else:
			grid[x][i].colour = GREEN
def show_valid_moves_KING(coords, grid):
	x = coords[0]
	y = coords[1]
	for i in range (x+1,9):
		if grid[i][y].type == "escape":
			return True
		elif grid[i][y].occ == True:
			break
		else:
			grid[i][y].colour = GREEN
	for i in range (x-1,-1,-1):
		if grid[i][y].type == "escape":
			return True
		elif grid[i][y].occ == True:
			break
		else:
			grid[i][y].colour = GREEN		
	for i in range (y+1,9):
		if grid[x][i].type == "escape":
			return True
		elif grid[x][i].occ == True:
			break
		else:
			grid[x][i].colour = GREEN
	for i in range (y-1,-1,-1):
		if grid[x][i].type == "escape":
			return True
		elif grid[x][i].occ == True:
			break
		else:
			grid[x][i].colour = GREEN
	return False
def hide_valid_moves(grid):
	for x in range(9):
		for y in range(9):
			if grid[x][y].colour == GREEN:
				grid[x][y].colour = BLACK
	#correct throne colour if king has left
	if grid[4][4].colour == BLACK:
		grid[4][4].colour = THRONE
def random_move_P1(grid):
	pieces_to_move = []
	places_to_move_it = []
	king = False
	for x in range(9):
		for y in range(9):
			if grid[x][y].colour == SWEDES:
				pieces_to_move.append( (x,y) )
	while True:
		i = random.randint(0,len(pieces_to_move)-1)
		x = pieces_to_move[i][0]
		y = pieces_to_move[i][1]
		for j in range (x+1,9):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				places_to_move_it.append( (j,y) )
		for j in range (x-1,-1,-1):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				places_to_move_it.append( (j,y) )	
		for j in range (y+1,9):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				places_to_move_it.append( (x,j) )
		for j in range (y-1,-1,-1):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				places_to_move_it.append( (x,j) )
		if places_to_move_it:
			k = random.randint(0,len(places_to_move_it)-1)
			return ( pieces_to_move[i][0], pieces_to_move[i][1], places_to_move_it[k][0], places_to_move_it[k][1])
def random_move_P2(grid):
	pieces_to_move = []
	places_to_move_it = []
	for x in range(9):
		for y in range(9):
			if grid[x][y].colour == MOSCUVITES:
				pieces_to_move.append( (x,y) )
	while True:
		i = random.randint(0,len(pieces_to_move)-1)
		x = pieces_to_move[i][0]
		y = pieces_to_move[i][1]
		for j in range (x+1,9):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				places_to_move_it.append( (j,y) )
		for j in range (x-1,-1,-1):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				places_to_move_it.append( (j,y) )	
		for j in range (y+1,9):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				places_to_move_it.append( (x,j) )
		for j in range (y-1,-1,-1):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				places_to_move_it.append( (x,j) )
		if places_to_move_it:
			k = random.randint(0,len(places_to_move_it)-1)
			return ( pieces_to_move[i][0], pieces_to_move[i][1], places_to_move_it[k][0], places_to_move_it[k][1])
#checks if moving to these coordinates causes a capture
def check_for_captured_MOSCUVITES(x,y,grid):
	if (x-2) >= 0 and grid[x-1][y].colour == MOSCUVITES and grid[x-2][y].colour != BLACK and grid[x-2][y].colour != MOSCUVITES:
		grid[x-1][y].colour = BLACK
		grid[x-1][y].occ = False
	if (x+2) <= 8 and grid[x+1][y].colour == MOSCUVITES and grid[x+2][y].colour != BLACK and grid[x+2][y].colour != MOSCUVITES:
		grid[x+1][y].colour = BLACK
		grid[x+1][y].occ = False
	if (y-2) >= 0 and grid[x][y-1].colour == MOSCUVITES and grid[x][y-2].colour != BLACK and grid[x][y-2].colour != MOSCUVITES:
		grid[x][y-1].colour = BLACK
		grid[x][y-1].occ = False
	if (y+2) <= 8 and grid[x][y+1].colour == MOSCUVITES and grid[x][y+2].colour != BLACK and grid[x][y+2].colour != MOSCUVITES:
		grid[x][y+1].colour = BLACK
		grid[x][y+1].occ = False
def check_for_captured_SWEDES(x,y,grid):
	if (x-2) >= 0 and grid[x-1][y].colour == SWEDES and (grid[x-2][y].colour == MOSCUVITES or grid[x-2][y].type == "escape" or grid[x-2][y].colour == THRONE):
		grid[x-1][y].colour = BLACK
		grid[x-1][y].occ = False
	if (x+2) <= 8 and grid[x+1][y].colour == SWEDES and (grid[x+2][y].colour == MOSCUVITES or grid[x+2][y].type == "escape" or grid[x+2][y].colour == THRONE):
		grid[x+1][y].colour = BLACK
		grid[x+1][y].occ = False
	if (y-2) >= 0 and grid[x][y-1].colour == SWEDES and (grid[x][y-2].colour == MOSCUVITES or grid[x][y-2].type == "escape" or grid[x][y-2].colour == THRONE):
		grid[x][y-1].colour = BLACK
		grid[x][y-1].occ = False
	if (y+2) <= 8 and grid[x][y+1].colour == SWEDES and (grid[x][y+2].colour == MOSCUVITES or grid[x][y+2].type == "escape" or grid[x][y+2].colour == THRONE):
		grid[x][y+1].colour = BLACK
		grid[x][y+1].occ = False
def check_for_captured_KING(x,y,grid):
	king_square = "normal"
	king_x = 0
	king_y = 0
	for xx in range (9):
		for yy in range(9):
			if grid[xx][yy].colour == KING:
				king_square = grid[xx][yy].type
				king_x = xx
				king_y = yy
				break
	#captured on throne
	if king_square == "throne":
		for xx in range (3,6):
			for yy in range (3,6):
				if math.fabs(xx-yy) == 1:
					if grid[xx][yy].colour != MOSCUVITES:
						return False
		return True
	#captured adjacent to throne
	if king_square == "throne_adjacent":
		for xx in range(king_x-1,king_x+2):
			for yy in range(king_y-1,king_y+2):
				if math.fabs(xx-yy) == 2:
					if grid[xx][yy].colour != MOSCUVITES and grid[xx][yy].colour != THRONE:
						return False
		return True
	#captured normally
	else:
		if (x-2) >= 0 and grid[x-1][y].colour == KING and grid[x-2][y].colour == MOSCUVITES:
			return True
		elif (x+2) <= 8 and grid[x+1][y].colour == KING and grid[x+2][y].colour == MOSCUVITES:
			return True
		elif (y-2) >= 0 and grid[x][y-1].colour == KING and grid[x][y-2].colour == MOSCUVITES:
			return True
		elif (y+2) <= 8 and grid[x][y+1].colour == KING and grid[x][y+2].colour == MOSCUVITES:
			return True

	return False