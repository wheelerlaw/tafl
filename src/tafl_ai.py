#!/usr/bin/env python

from tafl_methods import Tile

BACKGROUND = (175,175,175)

BLACK = (0,0,0)

GREEN = (50,255,50)

KING = (255,190,50)

SWEDES = (130,50,255)

MOSCUVITES = (255,50,50)

ESCAPE = (75,75,125)

THRONE = (66,66,66)

#plan: minimax. 


#input: current grid in which AI needs to make a move. output: grid after AI has made move (includes checks for pieces captured)
def make_move(grid):
	list_of_moves = get_list_of_moves_P1(grid)

class WeightedBoard:
	"""a board with a score"""
	def __init__(self,grid,score):
		self.grid = grid
		self.score = score

def get_list_of_moves_P1(grid):
	moves = [] #list of player 1's pieces
	for x in range(9):
		for y in range(9):
			if grid[x][y].colour == SWEDES or grid[x][y].colour == KING:
				moves.append( (x,y) )		
	
	weighted_boards = [] #list of all possible grids after AI makes a move, each with a score
	
	for i in range(len(moves)):
		x = moves[i][0]
		y = moves[i][1]
		king = False
		if grid[x][y].colour == KING:
			king = True
		for j in range (x+1,9):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne" or  grid[j][y].type == "escape":
				if king:
					grid_copy = list(grid) #make a copy of the grid
					score = move_P1(grid_copy,(x,y),(j,y)) #update grid to represent the move, returns score for board
					weighted_boards.append(WeightedBoard(grid_copy,score)) #add this to the list of boards
				continue
			else:
				grid_copy = list(grid)
				score = move_P1(grid_copy,(x,y),(j,y))
				weighted_boards.append(WeightedBoard(grid_copy,score))
		for j in range (x-1,-1,-1):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne" or  grid[j][y].type == "escape":
				if king:
					grid_copy = list(grid)
					score = move_P1(grid_copy,(x,y),(j,y))
					weighted_boards.append(WeightedBoard(grid_copy,score))
				continue
			else:
				grid_copy = list(grid)
				score = move_P1(grid_copy,(x,y),(j,y))
				weighted_boards.append(WeightedBoard(grid_copy,score))	
		for j in range (y+1,9):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne" or  grid[x][j].type == "escape":
				if king:
					grid_copy = list(grid)
					score = move_P1(grid_copy,(x,y),(x,j))
					weighted_boards.append(WeightedBoard(grid_copy,score))
				continue
			else:
				grid_copy = list(grid)
				score = move_P1(grid_copy,(x,y),(x,j))
				weighted_boards.append(WeightedBoard(grid_copy,score))	
		for j in range (y-1,-1,-1):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne" or  grid[x][j].type == "escape":
				if king:
					grid_copy = list(grid)
					score = move_P1(grid_copy,(x,y),(x,j))
					weighted_boards.append(WeightedBoard(grid_copy,score))
				continue
			else:
				grid_copy = list(grid)
				score = move_P1(grid_copy,(x,y),(x,j))
				weighted_boards.append(WeightedBoard(grid_copy,score))

	return(weighted_boards)


def get_list_of_moves_P2(grid):
	moves = [] #list of player 1's pieces
	for x in range(9):
		for y in range(9):
			if grid[x][y].colour == MOSCUVITES:
				moves.append( (x,y) )		
	
	weighted_boards = [] #list of all possible grids after AI makes a move, each with a score
	
	for i in range(len(moves)):
		x = moves[i][0]
		y = moves[i][1]

		for j in range (x+1,9):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				grid_copy = list(grid)
				score = move_P2(grid_copy,(x,y),(j,y))
				weighted_boards.append(WeightedBoard(grid_copy,score))
		for j in range (x-1,-1,-1):
			if grid[j][y].occ == True:
				break
			if grid[j][y].type == "throne":
				continue
			else:
				grid_copy = list(grid)
				score = move_P2(grid_copy,(x,y),(j,y))
				weighted_boards.append(WeightedBoard(grid_copy,score))	
		for j in range (y+1,9):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				grid_copy = list(grid)
				score = move_P2(grid_copy,(x,y),(x,j))
				weighted_boards.append(WeightedBoard(grid_copy,score))	
		for j in range (y-1,-1,-1):
			if grid[x][j].occ == True:
				break
			if grid[x][j].type == "throne":
				continue
			else:
				grid_copy = list(grid)
				score = move_P2(grid_copy,(x,y),(x,j))
				weighted_boards.append(WeightedBoard(grid_copy,score))

	return(weighted_boards)


def move_P1(grid,(xo,yo),(x,y)):  #xx,yy is origin coordinates, x,y is destination coordinates
	

	if grid[xo][yo].colour == KING:
		grid[x][y].colour = KING
	else:
		grid[x][y].colour = SWEDES
	grid[x][y].occ = True
	grid[xo][yo].colour = BLACK
	grid[xo][yo].occ = False


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



def move_P2(grid,(xo,yo),(x,y)): #xo,yo is origin coordinates, x,y is destination coordinates
	score = 0
	grid[xo][yo].colour = BLACK
	grid[xo][yo].occ = False
	grid[x][y].colour = MOSCUVITES
	grid[x][y].occ = True


	#first we check for a captured king, then we check for captured swedes
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

def check_king_capture(grid,xx,yy): pass
