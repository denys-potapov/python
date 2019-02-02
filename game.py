import random

ACTIONS = ["stay", "move", "eat", "load", "unload"]

# (x, y)
DIRECTIONS = {
    'up':    (0, -1),
    'right': (1, 0),
    'down':  (0, 1),
    'left':  (-1, 0)
}


class Game():
    id = ''

    def cell(self, pos, dir = False):
        x, y = pos
        if dir:
            dx, dy = DIRECTIONS[dir]
            x, y = x + dx, y + dy

        if x < 0 or x >= self.map['width'] or y < 0 or y >= self.map['height']:
            return {'wall': 'wall'}

        return self.map['cells'][y][x]

    def order(self, ant, act, dirs, probs=None):
        dir = random.choice(dirs)
        if probs is not None:
            choices = []
            for i in len(probs):
                choices += [i] * probs[i]
            dir = dirs[random.choice(choices)]

        self.orders[ant['id']] = {
            'act': act,
            'dir': dir
        }

        return True

    def load_hive(self, hive):
        self.id = hive['id']
        self.free_ants = []
        for i, ant in hive['ants'].items():
            ant['id'] = i
            ant['pos'] = (ant['x'], ant['y'])
            self.free_ants.append(ant)

        self.map = hive['map']

    def unload_dir(self, pos):
        for dir in DIRECTIONS.keys():
            cell = self.cell(pos, dir)
            if (cell.get('hive') == self.id) and (cell.get('ant', 0) == 0):
                return dir

        return False

    def do_loaded(self, ant):
        if ant['payload'] == 0:
            return True
        # can unload
        unload_dir = self.unload_dir(ant['pos'])
        if unload_dir:
            return self.order(ant, [unload_dir], 'unload')
        # can load

        return False

    def do_turn(self, hive):
        self.load_hive(hive)
        self.orders = {}

        # loaded ants
        self.free_ants = filter(lambda a: self.do_loaded(a), self.free_ants)

        # Loop through ants and give orders
        for ant in self.free_ants:
            self.order(
                ant,
                ACTIONS[random.randint(0, 4)],
                list(DIRECTIONS.keys())
            )
        # json format sample:
        # {"1":{"act":"load","dir":"down"},"17":{"act":"load","dir":"up"}}

        return self.orders
