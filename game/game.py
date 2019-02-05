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
        self.food = []
        for y, row in enumerate(self.map['cells']):
            for x, cell in enumerate(row):
                # load hive pos on firts turn
                if (self.hive_pos is None) and (cell.get('hive') == self.id):
                    self.hive_pos = (x, y)
                # fill food
                f = cell.get('food', 0)
                if (f > 0) and (len(cell) == 1):
                    self.food.append(((x, y), f))

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
            # don't load from hive
            if (not cell.get('hive')):
                food.append((dir, cell.get('food', 0)))
        food = filter(lambda f: f[1] > 0, food)
        return sorted(food, key = lambda f: f[1])

    def dist(self, pos, target):
        return abs(target[0] - pos[0]) + abs(target[1] - pos[1])

    def move_dirs(self, pos, target):
        can_dirs = []
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        if dx != 0:
            can_dirs.append(('right' if dx > 0 else 'left', abs(dx)))
        if dy != 0:
            can_dirs.append(('down' if dy > 0 else 'up', abs(dy)))

        # only if we can
        move_dirs = []
        for (dir, p) in can_dirs:
            cell = self.cell(pos, dir)
            if ('food' in cell) or ('ant' in cell) or ('wall' in cell):
                continue
            if cell.get('hive', self.id) != self.id:
                continue
            move_dirs.append((dir, p))

        return move_dirs

    def move_to(self, ant, target):
        move_dirs = self.move_dirs(ant['pos'], target)
        if len(move_dirs) > 0:
            self.order(ant, 'move', move_dirs)
        else:
            self.order(ant, 'stay', [('left', 1)])

    def do_loaded(self, ant):
        # can unload
        unload_dir = self.unload_dir(ant['pos'])
        if unload_dir and (ant['payload'] > 0):
            self.order(ant, 'unload', [(unload_dir, 1)])
            return False
        
        # can load
        load_dirs = self.load_dirs(ant['pos'])
        if (len(load_dirs) > 0) and ant['payload'] < 5:
            self.order(ant, 'load', load_dirs)
            return False

        if ant['payload'] == 0:
            return True

        # go home
        self.move_to(ant, self.hive_pos)
        return False

    def do_food(self):
        self.food.sort(key = lambda f: self.dist(f[0], self.hive_pos))
        print(food[:5])
        for pos, _ in self.food:
            min_ant = None
            min_d = 1000000
            min_i = None
            for i, ant in enumerate(self.free_ants):
                d = self.dist(pos, ant['pos'])
                if d < min_d:
                    min_ant = ant
                    min_d = d
                    min_i = i

            if min_ant is None:
                return
            self.move_to(ant, pos)
            del(self.free_ants[min_i])
        

    def do_turn(self, hive):
        self.load_hive(hive)
        self.orders = {}

        # loaded ants
        self.free_ants = list(filter(lambda a: self.do_loaded(a), self.free_ants))

        # find food
        self.do_food()

        # stay still
        for ant in self.free_ants:
            self.order(ant, 'stay', [('left', 1)])

        return self.orders
