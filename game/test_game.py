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

def test_do_long_turn():
    hive = {'tick': 34, 'id': 's3-1', 'ants': {'1': {'wasted': 0, 'age': 34, 'health': 6, 'payload': 0, 'x': 1, 'y': 4, 'event': 'good', 'id': '1', 'pos': (1, 4)}, '2': {'wasted': 0, 'age': 0, 'health': 9, 'payload': 0, 'x': 1, 'y': 3, 'event': 'birth', 'id': '2', 'pos': (1, 3)}}, 'map': {'width': 30, 'height': 10, 'cells': [[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 6}, {}, {}, {}, {'food': 8}, {'food': 4}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 7}, {}, {}, {}, {}], [{'hive': 's3-1'}, {}, {}, {}, {}, {}, {}, {'food': 1}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 7}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{}, {'hive': 's3-1', 'ant': 's3-1'}, {}, {}, {}, {}, {'food': 2}, {}, {'food': 6}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 2}, {}, {}, {'food': 2}, {}, {}, {}, {}], [{}, {'ant': 's3-1'}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 6}, {}, {}, {}, {}, {}, {}, {}, {'food': 3}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{'food': 9}, {'food': 2}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 1}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 9}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 6}, {}, {}, {}, {}, {}, {}, {}, {'food': 5}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}], [{}, {}, {'food': 8}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'food': 1}, {}, {}, {}, {}, {}, {}, {}]]}}
    game = def_game()
    orders = game.do_turn(hive)
    assert len(orders) == 2

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
    assert game.move_dirs((2, 2), (0, 0)) == [('left', 2), ('up', 2)]