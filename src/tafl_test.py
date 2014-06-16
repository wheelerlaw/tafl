from test_screen import test
import tafl

game = tafl.Game()
game.current_board.move_piece((0,4), (2,4))

test(game)


test(game)