import random

ACTIONS = ["stay", "move", "eat", "load", "unload"]
DIRECTIONS = ["up", "down", "right", "left"]

# (x, y)
DIRECTIONS = {
    'up': ()
    'right':
    'down':
    'left'
}

class Game():
    hive_id = ''

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

    def load_ants(self, ants):
        self.free_ants = []
        for i, ant in ants.items():
            ant['id'] = i
            self.free_ants.append(ant)

    def loaded_turn(self, ant):
        if ant['payload'] == 0:
            return True
        # can unload
        # can load

        return False

    def do_turn(self, hive):
        self.load_ants(hive['ants'])
        self.orders = {}

        # loaded ants
        self.free_ants = filter(lambda a: self.loaded_turn(a), self.free_ants)

        # Loop through ants and give orders
        for ant in self.free_ants:
            self.order(
                ant,
                ACTIONS[random.randint(0, 4)],
                DIRECTIONS
            )
        # json format sample:
        # {"1":{"act":"load","dir":"down"},"17":{"act":"load","dir":"up"}}

        return self.orders
