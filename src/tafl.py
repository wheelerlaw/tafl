class GamePiece:
    def __init__(self, coords, player):
        """ GamePiece class. 
        Coords: 2-tuple of the coordinates with the x coordinate as the first element and the
            y coordinate as the second coordinate. 
        Player: the number of the player of this piece. 
            Player 1: the swedes. 
            Player 2: the moscuvites
            Player 3: (special case) represents the king, who is on the swedes side. """
        self.x = coords[0]
        self.y = coords[1]
        self.player = player
        
    def clone(self):
        """clone
        Returns a copy of the game piece. """
        copy = GamePiece((self.x,self.y), self.player, self.king)
        return copy
        
    def move_to(self,coords):
        """move_to
        Moves this game piece to the coordinates passed into the parameters."""
        self.x=coords[0]
        self.y=coords[1]
        
                
class Tile:
    """ Board tile:
    The board tile, unlike the gamePiece, does not represent the pieces of the game. 
    Instead, it is simply just a container representing the spaces on the board. This is 
    necessary for now since we need to know what coordiantes of the special squares. 
    occupiedWith: the player number of the piece that the board is occupied with. 
        1 for player 1, 2 for player 2, and 3 for the king of pleyer 1. """
    def __init__(self, occupied_with=0, kind=None):
        self.occupied_with = occupied_with
        self.kind = kind


class Board:
    """Represents the board of the game. Contains the list of game pieces as wlll as a 
    two dimensional array of all the game tiles. Has various methods for initializing and 
    cloning the board for the AI. 
    size: the size of the sides of the board (all sides must be equal). Must be an odd number. 
    initialize_pieces: Whether or not create new game pieces for the board. ONLY SET TRUE ON 
        GAME STARTUP!!"""
    def __init__(self, initialize_pieces=False):
        if(initialize_pieces):
            self.game_pieces = self._create_game_pieces()
        else:
            self.game_pieces = []
        
    def clone(self):
        """CLONE
        Clones the board and returns a copy of it. Performs a deep clone so all the 
        tiles, game pieces, and everything are clones as well. """
        copy = Board(self.size)
        for old_piece in self.game_pieces:
            copy.game_pieces.append(old_piece.clone())
            
        return copy
    
    def __hashable__(self):
        """Hashable
        Implements and overrides the default __hashable__ method for objects to define 
        the boards algorithm for hashing. """
        token = ""
        for gamePiece in self.game_pieces:
            token = token + gamePiece.x + gamePiece.y + ""
            
        hash = int(gamePiece) // 6
        return hash
    
    def _create_game_pieces(self):
        """_creategame_pieces
        Initializes the game pieces for the board using the start configuration. ONLY CALL THIS
            METHOD AT GAME STARTUP!"""
        p1pieces=[]
        
        list_of_player_1_coords = [(4,2), (4,3), (4,5), (4,6),
                                   (2,4), (3,4), (5,4), (6,4)]
        
        for coord in list_of_player_1_coords:
            newPiece = GamePiece(coord,1)
            p1pieces.append(newPiece)
        
        p2pieces=[]
        
        list_of_player_2_coords = [(0,3), (0,4), (0,5), (1,4)
                                   (8,3), (8,4), (8,5), (7,4)
                                   (3,0), (4,0), (5,0), (4,1)
                                   (3,8), (4,8), (5,8), (4,7)]
        
        for coord in list_of_player_2_coords:
            newPiece = GamePiece(coord,2)
            p2pieces.append(newPiece)
            
        # 
        newPiece = GamePiece((4,4),3)
        p1pieces.append(newPiece)
            
        return p1pieces + p2pieces
    
    def is_piece(self,coords):
        """is_piece
        Goes through the list of pieces and determines if the coordinates that are passed
        refer to a location where a piece exists. 
        coords: the coordinates as a 2-tuple with the x coordinate as the first element and
            the y-coordinate as the second element."""
        for piece in self.game_pieces:
            if coords[0] == piece.x and coords[1] == piece.y:
                return True
        return False
            
    def get_possible_next_moves(self,selected_piece_coords):
        """get_possible_next_moves
        Returns a dictionary of the next possible moves based on the current configuration. 
        The key is the hash for the board configuration and the value is the board object itself. """
        moves = {}
        for i in len(self.game_pieces):
            boardCopy = self.clone()
            boardCopy.game_pieces[i].moveTo((boardCopy.game_pieces[i].x,boardCopy.game_pieces[i].y+1))
            moves.append(boardCopy.hash(),boardCopy)
           
    def move_piece(self, selected_piece_coords, destination_coords):
        for piece in self.game_pieces:
            if selected_piece_coords[0] == piece.x and selected_piece_coords[1] == piece.y:
                piece.x = destination_coords[0]
                piece.y = destination_coords[1]

                
class Game:
    def __init__(self,size=9):
        self.size = size
        self.throne_coords = (4,4)
        self.throne_adj_coords = [(3,4), (5,4)
                                  (4,3), (4,5)]
        self.escape_coords = [(0,0), (0,8),
                              (8,0), (8,8)]
        self.current_board = Board(True)
        self.prev_boards = None
        
    def get_current_board(self):
        return self.current_board
    
    class Controller:
        def __init(self):
            pass
    
        def _validate_coords(self,coords):
            if coords[0] >= self.size or coords[0] < 0:
                return False
            if coords[1] >= self.size or coords[1] < 0:
                return False
            return True
        
        def make_move(self,selected_piece_coords, destination_coords, player):
            
            # Verification of the coordinates. 
            if self._validate_coords(destination_coords) == False:
                return False
            if self._validate_coords(selected_piece_coords) == False:
                return False
            
            # Validation of the coordinate.
            if self.current_board.is_piece(selected_piece_coords) == False:
                return False
            if self.current_board.is_piece(destination_coords):
                return False
            
            # Verification player number:"
            if player < 0 or player > 3:
                return False
            
            board_copy = self.current_board.clone()
            board_copy.move_piece(selected_piece_coords, destination_coords)
            
            next_moves = self.current_board.get_possible_next_moves(selected_piece_coords)
            
            if not board_copy in next_moves:
                return False
            
            self.prev_boards.append(self.current_board)
            self.current_board = board_copy
            
            # notify
            
            return True
            



        
        