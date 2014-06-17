

class GamePiece:
    def __init__(self, location_coords, player):
        """ GamePiece class. 
        Coords: 2-tuple of the coordinates with the x coordinate as the first element and the
            y coordinate as the second coordinate. 
        Player: the number of the player of this piece. 
            Player 1: the swedes. 
            Player 2: the moscuvites
            Player 3: (special case) represents the king, who is on the swedes side. """
        self.x = location_coords[0]
        self.y = location_coords[1]
        self.player = player
        return
        
    def clone(self):
        """clone
        Returns a copy of the game piece. """
        copy = GamePiece((self.x, self.y), self.player)
        return copy
        
    def move_to(self, destination_coords):
        """move_to
        Moves this game piece to the coordinates passed into the parameters."""
        self.x = destination_coords[0]
        self.y = destination_coords[1]
        return
        
                
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
        return


class Board:
    """Represents the board of the game. Contains the list of game pieces as wlll as a 
    two dimensional array of all the game tiles. Has various methods for initializing and 
    cloning the board for the AI. 
    size: the size of the sides of the board (all sides must be equal). Must be an odd number. 
    initialize_pieces: Whether or not create new game pieces for the board. ONLY SET TRUE ON 
        GAME STARTUP!!"""
    def __init__(self, game, initialize_pieces=False):
        if initialize_pieces:
            self.game_pieces = self._create_game_pieces()
        else:
            self.game_pieces = []
            
        self.game = game
        return
        
    def clone(self):
        """CLONE
        Clones the board and returns a copy of it. Performs a deep clone so all the 
        tiles, game pieces, and everything are clones as well. """
        copy = Board(self.game)
        for old_piece in self.game_pieces:
            copy.game_pieces.append(old_piece.clone())
            
        return copy
    
    def __hash__(self):
        """Hash
        Implements and overrides the default __hashable__ method for objects to define 
        the boards algorithm for hashing. """
        token = ""
        for gamePiece in self.game_pieces:
            token = token + str(gamePiece.x) + str(gamePiece.y)
            
        hash_ = int(token) % 100000
        return hash_
    
    def __eq__(self, other):
        """eq
        Establishes the equivalence between the boards. Compares the x and y coordinates of all the 
        pieces of both boards. """

        if isinstance(other, Board):
            if len(self.game_pieces) != len(other.game_pieces):
                return False
            for i in range(len(self.game_pieces)):
                if self.game_pieces[i].x != other.game_pieces[i].x or self.game_pieces[i].y != other.game_pieces[i].y:
                    return False
            return True
        else:
            if hash(self) == other:
                return True
            return False
           
    def _create_game_pieces(self):
        """_creategame_pieces
        Initializes the game pieces for the board using the start configuration. ONLY CALL THIS
            METHOD AT GAME STARTUP!"""
        p1pieces = []
        
        list_of_player_1_coords = [(4, 2), (4, 3), (4, 5), (4, 6),
                                   (2, 4), (3, 4), (5, 4), (6, 4)]
        
        for coord in list_of_player_1_coords:
            new_piece = GamePiece(coord, 1)
            p1pieces.append(new_piece)
        
        p2pieces = []
        
        list_of_player_2_coords = [(0, 3), (0, 4), (0, 5), (1, 4),
                                   (8, 3), (8, 4), (8, 5), (7, 4),
                                   (3, 0), (4, 0), (5, 0), (4, 1),
                                   (3, 8), (4, 8), (5, 8), (4, 7)]
        
        for coord in list_of_player_2_coords:
            new_piece = GamePiece(coord, 2)
            p2pieces.append(new_piece)
            
        # 
        new_piece = GamePiece((4, 4), 3)
        p1pieces.append(new_piece)
            
        return p1pieces + p2pieces
    
    def is_piece(self, piece_coords):
        """is_piece
        Goes through the list of pieces and determines if the coordinates that are passed
        refer to a location where a piece exists. 
        coords: the coordinates as a 2-tuple with the x coordinate as the first element and
            the y-coordinate as the second element."""
        for piece in self.game_pieces:
            if piece_coords[0] == piece.x and piece_coords[1] == piece.y:
                return True
        return False
            
    def get_possible_next_moves(self, selected_piece_coords):
        """get_possible_next_moves
        Returns a dictionary of the next possible moves based on the current configuration. 
        The key is the hash for the board configuration and the value is the board object itself. """
        moves = {}
        next_move_coords = self.get_possible_next_coords(selected_piece_coords)
        for next_move in next_move_coords:
            board_copy = self.clone()
            board_copy.move_piece(selected_piece_coords, next_move)            
            moves[hash(board_copy)] = board_copy
        return moves
    
    def get_possible_next_coords(self, selected_piece_coords):
        """get_possible_next_coords
        Returns a list of 2-tuples as coordinates of the places that the selected piece can go. """
        next_coords = []
        if selected_piece_coords[0] < 9:
            for i in range(selected_piece_coords[0]+1, 9):
                temp_coords = (i, selected_piece_coords[1])
                if self.is_piece(temp_coords):
                    break
                next_coords.append(temp_coords)
                
        if selected_piece_coords[0] > 0:
            for i in range(selected_piece_coords[0]-1, 0, -1):
                temp_coords = (i, selected_piece_coords[1])
                if self.is_piece(temp_coords):
                    break
                next_coords.append(temp_coords)
        
        if selected_piece_coords[1] < 9:
            for i in range(selected_piece_coords[1]+1, 9):
                temp_coords = (selected_piece_coords[0], i)
                if self.is_piece(temp_coords):
                    break
                next_coords.append(temp_coords)
                
        if selected_piece_coords[1] > 0:
            for i in range(selected_piece_coords[1]-1, 0, -1):
                temp_coords = (selected_piece_coords[0], i)
                if self.is_piece(temp_coords):
                    break
                next_coords.append(temp_coords)
        return next_coords
    
    def move_piece(self, selected_piece_coords, destination_coords):
        """move_piece
        Moves the pieces as the selected coordinates. If the piece does not exist at that coordinate, 
        this method returns false. Otherwise, it returns true. Also checks to make sure that there is no piece
        at the destinatio coordinates. 
        selected_piece_coords: 2-tuple of the piece coordinates, where the x coordinate is the first element, and 
            the y-coordinate is the second element. 
        destination_coords: 2-tuple of the destination coordinates to move the piece. Checks to see if the 
            destination does not contain a piece and will return true if valid or false is not."""
            
        if selected_piece_coords[0] < 0 or destination_coords[0] < 0:
            return False
        if selected_piece_coords[1] >= 9 or destination_coords[1] >= 9:
            return False
        
        if self.is_piece(destination_coords):
            return False
            
        for piece in self.game_pieces:
            if selected_piece_coords[0] == piece.x and selected_piece_coords[1] == piece.y:
                piece.x = destination_coords[0]
                piece.y = destination_coords[1]
                break
        return True
    
    def get_piece(self, selected_piece_coords):
        """get_piece
        Given a coordinate, returns a copy of a given piece. """
        for piece in self.game_pieces:
            if selected_piece_coords[0] == piece.x and selected_piece_coords[1] == piece.y:
                return piece.clone()
        return None
    
    def check_for_captures(self, selected_piece_coords, player):
        """check_for_captures
        given a coordinate of a piece, checks for captures pieces in its vicinity. """
        neighbor_coords = [(selected_piece_coords[0]+1, selected_piece_coords[1]),
                           (selected_piece_coords[0]-1, selected_piece_coords[1]),
                           (selected_piece_coords[0], selected_piece_coords[1]+1),
                           (selected_piece_coords[0], selected_piece_coords[1]-1)]
        
        neighbor_of_neighbor_coords = [(selected_piece_coords[0]+2, selected_piece_coords[1]),
                                       (selected_piece_coords[0]-2, selected_piece_coords[1]),
                                       (selected_piece_coords[0], selected_piece_coords[1]+2),
                                       (selected_piece_coords[0], selected_piece_coords[1]-2)]
        
        for i in range(4):
            neighbor_piece = self.get_piece(neighbor_coords[i])
            neighbor_of_neighbor_piece = self.get_piece(neighbor_of_neighbor_coords[i])
            
            if neighbor_piece is None and neighbor_of_neighbor_piece is None and \
                neighbor_of_neighbor_piece not in self.game.escape_coords and \
                    neighbor_of_neighbor_piece != self.game.throne_coords:
                break
            
            if player == 1:
                if neighbor_piece.player == 2 and (neighbor_of_neighbor_piece.player == 1 or
                                                   neighbor_of_neighbor_piece.player == 3 or
                                                   neighbor_of_neighbor_coords[i] in
                                                   self.game.escape_coords or
                                                   neighbor_of_neighbor_coords[i] == self.game.throne_coord):
                    pass
                    
            else:
                pass


class Game:
    """game
    The main game class containing the state and the controller class for all the interaction with the state. 
    initialization autumatically creates a new board with starting congfiguration. """
    def __init__(self, size=9):
        self.size = size
        self.throne_coords = (4, 4)
        self.throne_adj_coords = [(3, 4), (5, 4),
                                  (4, 3), (4, 5)]
        self.escape_coords = [(0, 0), (0, 8),
                              (8, 0), (8, 8)]
        self.current_board = Board(self, True)
        self.prev_boards = []
        
        self.player = 1
        self.over = False
        return
        
    def get_current_board(self):
        return self.current_board
    
    def verify_coords(self, piece_coords):
        """verify_coords
        Does a simple coordinate verification to ensure that they are within the bounds defined in the game
        class. 
        coords: 2-tuple of the coordinates to be verified. first element is the x-coordinate, second element 
            is the y-coordinate. 
        Returns false if the coordinates are not within the bounds. Otherwise, returns true. """
        if piece_coords[0] >= self.size or piece_coords[0] < 0:
            return False
        if piece_coords[1] >= self.size or piece_coords[1] < 0:
            return False
        return True
    
    def make_move(self, selected_piece_coords, destination_coords, player):
            """make_move
            The main method of the controller class.
            Takes in the selected piece coords, destination coords, and the player number and attempts to move
            the piece. Performs some simple verification and validation of the coordinates.
            Generates a list of valid moves and sees if the selected move is among them. Returns false if not valid,
            otherwise returns true.
            selected_piece_coords: 2-tuple of the coords. First element: x-coordinate, second element: y-coordinate."""

            # Verification player number:"
            if player < 0 or player > 3:
                return False

            board_copy = self.current_board.clone()

            # move_piece handled move verification and validation.
            board_copy.move_piece(selected_piece_coords, destination_coords)

            next_moves = self.current_board.get_possible_next_moves(selected_piece_coords)

            if not board_copy in next_moves:
                return False

            self.prev_boards.append(self.current_board)
            self.current_board = board_copy

            # notify

            if player == 1 or player == 3:
                self.player = 2
            if player == 2:
                self.player = 1
            return True