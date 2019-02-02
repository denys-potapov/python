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
    hive_pos = None

    def cell(self, pos, dir = False):
        x, y = pos
        if dir:
            dx, dy = DIRECTIONS[dir]
            x, y = x + dx, y + dy

        if x < 0 or x >= self.map['width'] or y < 0 or y >= self.map['height']:
            return {'wall': 'wall'}

        return self.map['cells'][y][x]

    # dirs = [(dir, probability)]
    def order(self, ant, act, dirs):
        choices = []
        for d, p in dirs:
            choices += [d] * p

        self.orders[ant['id']] = {
            'act': act,
            'dir': random.choice(choices)
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

        # load only on first turn
        if self.hive_pos is None:
            for y, row in enumerate(self.map['cells']):
                for x, cell in enumerate(row):
                    if cell.get('hive') == self.id:
                        self.hive_pos = (x, y)

    def unload_dir(self, pos):
        for dir in DIRECTIONS.keys():
            cell = self.cell(pos, dir)
            if (cell.get('hive') == self.id) and (cell.get('ant', 0) == 0):
                return dir

        return False

    def load_dirs(self, pos):
        food = []
        for dir in DIRECTIONS.keys():
            cell = self.cell(pos, dir)
            food.append((dir, cell.get('food', 0)))
        food = filter(lambda f: f[1] > 0, food)
        return sorted(food, key = lambda f: f[1])

    def move_dirs(self, pos, target):
        can_dirs = []
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        if dx != 0:
            can_dirs.append(('left' if dx > 0 else 'right', abs(dx)))
        if dy != 0:
            can_dirs.append(('bottom' if dy > 0 else 'up', abs(dy)))

        # only if we can
        move_dirs = []
        for (dir, p) in can_dirs:
            cell = self.cell(pos, dir)
            if ('food' in cell) or ('ant' in cell):
                continue
            if cell.get('hive', self.id) != self.id:
                continue
            move_dirs.append((dir, p))

        return move_dirs


    def do_loaded(self, ant):
        if ant['payload'] == 0:
            return True
        # can unload
        unload_dir = self.unload_dir(ant['pos'])
        if unload_dir:
            self.order(ant, 'unload', [(unload_dir, 1)])
            return False
        
        # can load
        load_dirs = self.load_dirs(ant['pos'])
        if (len(load_dirs) > 0) and ant['payload'] < 5:
            self.order(ant, 'unload', load_dirs)
            return False

        # go to hive
        move_dirs = self.move_dirs(ant['pos'], self.hive_pos)
        if len(move_dirs) > 0:
            self.order(ant, 'unload', move_dirs)
            return False
        else:
            self.order(ant, 'stay', ('left', 1))

        return False

    def do_turn(self, hive):
        self.load_hive(hive)
        self.orders = {}

        # loaded ants
        self.free_ants = filter(lambda a: self.do_loaded(a), self.free_ants)

        # Loop through ants and give orders
        # for ant in self.free_ants:
        #     self.order(
        #         ant,
        #         ACTIONS[random.randint(0, 4)],
        #         ['le'
        #     )
        # # json format sample:
        # {"1":{"act":"load","dir":"down"},"17":{"act":"load","dir":"up"}}

        return self.orders
