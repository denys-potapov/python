import json
from game import Game

def payload():
    return json.load(open('payload.json'))


def def_game():
    game = Game()
    game.load_hive(payload())
    return game

def test_game_load_hive():
    game = def_game()
    assert len(game.free_ants) == 2
    assert game.hive_pos == (0, 0)


def test_game_do_turn():
    hive = {
        'id': '1',
        'ants': {'1': {'x': 0, 'y': 0, 'payload': 1}},
        'map': {
            'height': 1,
            'width': 3,
            'cells': [[{}, {'food': 3}, {'hive': '1'}]]
        }
    }
    game = def_game()
    orders = game.do_turn(hive)
    print(orders)

def test_game_do_turn2():
    hive = {
        'id': '1',
        'ants': {'1': {'x': 1, 'y': 0, 'payload': 0}},
        'map': {
            'height': 1,
            'width': 3,
            'cells': [[{'hive': '1', 'food': 1}, {}, {}, {'food': 3}]]
        }
    }
    game = def_game()
    orders = game.do_turn(hive)
    print(orders)


def test_cell():
    game = def_game()
    assert game.cell((100, 100)) == {'wall': 'wall'}

def test_unload_dir():
    game = def_game()
    assert game.unload_dir((1, 0)) == 'left'

def test_load_dir():
    game = def_game()
    assert game.load_dirs((1, 1)) == [('left', 5)]

def test_move_dirs():
    game = def_game()
    assert game.move_dirs((2, 2), (0, 0)) ==  [('left', 2), ('up', 2)] 