import json
from game import Game


def test_game_do_turn():
    f = open('payload.json')
    hive = json.load(f)
    game = Game()
    orders = game.do_turn(hive)
    print(orders)
