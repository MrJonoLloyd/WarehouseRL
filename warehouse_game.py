import numpy as np
import random

# Object mappings
PLAYER = 0
FLOOR = -1
BAY_NO_ITEM = -2
BAY_WITH_ITEM = -3
PALLET = -4


P = 0
_ = -1
B = -2
D = -4

# WAREHOUSE_LAYOUT = np.array([[_, _, _, _, _, _, _, _, _],
#                              [_, _, _, _, _, _, _, _, _],
#                              [_, B, B, _, _, _, B, B, _],
#                              [_, B, B, _, P, _, B, B, _],
#                              [_, _, _, _, _, _, _, _, _],
#                              [_, _, _, _, D, _, _, _, _]])

WAREHOUSE_LAYOUT = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -2, -2, -1, -2, -2, -1],
                             [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, 0, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -2, -2, -1, -1, -1, -1, -2, -2, -1],
                             [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                             [-1, -1, -1, -1, -4, -4, -1, -1, -1, -1]])


# player input mappings
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class WarehouseGame():
    def __init__(self):
        self.warehouse = WAREHOUSE_LAYOUT.copy()
        self.player_value = 0
        self.score = 0

        self.n_bays = 0
        self.bay_locations = []
        for (col, row), value in np.ndenumerate(self.warehouse):
            if value == PLAYER:
                self.starting_x = row
                self.starting_y = col
            if value == BAY_NO_ITEM:
                self.n_bays += 1
                self.bay_locations.append((row, col))

        self.player_x = self.starting_x
        self.player_y = self.starting_y

        self.max_bays_to_stock = 5
        self.stock_random_bays()

    def reset_warehouse(self):
        self.warehouse = WAREHOUSE_LAYOUT.copy()
        self.player_value = PLAYER
        self.player_x = self.starting_x
        self.player_y = self.starting_y
        self.stock_random_bays()

    def stock_random_bays(self):
        self.stocked_bays = []
        self.stocked_util = []
        self.n_bays_to_stock = random.randint(1, self.max_bays_to_stock)
        for i in range(self.max_bays_to_stock):
            rand_bay_location = self.bay_locations[random.randint(
                0, self.n_bays - 1)]
            bay_x, bay_y = rand_bay_location
            if i < self.n_bays_to_stock and self.warehouse[bay_y][bay_x] == BAY_NO_ITEM:
                self.warehouse[bay_y][bay_x] = BAY_WITH_ITEM
                self.stocked_bays.append(rand_bay_location)
                self.stocked_util.append(rand_bay_location)
            else:
                self.stocked_util.append((127, 127))

    def _handle_input(self, restriction, new_x, new_y):
        # Check player not moving outside of screen
        if restriction:
            return "nothing"

        # Pick up item from bay
        elif self.warehouse[new_y][new_x] == BAY_WITH_ITEM:
            self.warehouse[new_y][new_x] = BAY_NO_ITEM
            self.stocked_bays.remove((new_x, new_y))
            i = self.stocked_util.index((new_x, new_y))
            self.stocked_util[i] = (127, 127)
            self.player_value += 1
            self.warehouse[self.player_y][self.player_x] = self.player_value
            return "picked up"

        # Move to new position
        elif self.warehouse[new_y][new_x] == FLOOR:
            self.warehouse[self.player_y][self.player_x] = FLOOR
            self.player_x = new_x
            self.player_y = new_y
            self.warehouse[self.player_y][self.player_x] = self.player_value
            return "moved"

        # Deliver to pallet
        elif self.warehouse[new_y][new_x] == PALLET and self.player_value > 0:
            self.player_value = PLAYER
            self.warehouse[self.player_y][self.player_x] = self.player_value
            self.score += 1*self.player_value
            if len(self.stocked_bays) == 0:
                self.stock_random_bays()
            return "delivered"

        return "nothing"

    def process_directional_input(self, input):
        result = "nothing"
        max_y, max_x = self.warehouse.shape
        if input == UP:
            result = self._handle_input(self.player_y == 0,
                                        self.player_x, self.player_y - 1)
        elif input == RIGHT:
            result = self._handle_input(self.player_x == max_x - 1,
                                        self.player_x + 1, self.player_y)
        elif input == DOWN:
            result = self._handle_input(self.player_y == max_y - 1,
                                        self.player_x, self.player_y + 1)
        elif input == LEFT:
            result = self._handle_input(self.player_x == 0,
                                        self.player_x - 1, self.player_y)
        return result


# game = WarehouseGame()
# print(game.warehouse)
# game.process_directional_input(UP)
# print("up")
# print(game.warehouse)
# game.process_directional_input(LEFT)
# print("left")
# print(game.warehouse)
# game.process_directional_input(RIGHT)
# print("right")
# print(game.warehouse)
# game.process_directional_input(DOWN)
# print("down")
# print(game.warehouse)
# game.process_directional_input(DOWN)
# print("down")
# print(game.warehouse)
