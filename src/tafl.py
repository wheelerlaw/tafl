class GamePiece:
    def __init__(self, coords, player, king=False):
        self.x = coords[0]
        self.y = coords[1]
        self.player = player
        self.king = king
        
    def clone(self):
        copy = GamePiece((self.x,self.y), self.player, self.king)
        return copy
        
    def moveTo(self,coords):
        self.x=coords[0]
        self.y=coords[1]

class Board:
    def __init__(self,size=9):
        self.size=size
        self.gamePieces = self.createGamePieces()
        
    def clone(self):
        copy = Board(self.size)
        for old_piece in self.gamePieces:
            copy.gamePieces = old_piece.clone()
            
        return copy
    
    def __hashable__(self):
        token = ""
        for gamePiece in self.gamePieces:
            token = token + gamePiece.x + gamePiece.y + ""
            
        hash = gamePiece // 6
        return hash
    
    def _createGamePieces(self):
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
            
        return p1pieces + p2pieces
            
        
    
    def getPossibleNextMoves(self,selected_piece_coords):
        moves = {}
        for i in len(self.gamePieces):
            boardCopy = self.clone()
            boardCopy.gamePieces[i].moveTo((boardCopy.gamePieces[i].x,boardCopy.gamePieces[i].y+1))
            moves.append(boardCopy.hash(),boardCopy)
           
       
        
    
        
        
class Controller:
    def __init(self):
        pass
    
    def getMove(self,selected_piece_coords, destination_coords, player):
        
    

        
        