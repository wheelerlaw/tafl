from test_screen import test
import tafl

game = tafl.Game()
game.make_move((5,4), (5,3), 1)
test(game)