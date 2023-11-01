from warehouse_game import WarehouseGame, PLAYER, FLOOR, BAY_NO_ITEM, BAY_WITH_ITEM, PALLET

import numpy as np
from gymnasium import Env
from gymnasium.spaces import Box, Discrete
import pygame


# ### Action Space
# There are 4 discrete deterministic actions:
# - 0: up
# - 1: right
# - 2: down
# - 3: left

# ### Observation Space
# player_x:         x coordinate of the player
# player_y:         y coordinate of the player
# player_value:     number of items the player is holding
# (
# delta_x_i:        x distance from the ith item. Equals 0 if item is picked up
# delta_y_i:        y distance from the ith item. Equals 0 if item is picked up
# picked_up_i:      Equals 0 if ith item is in bay. Equals 1 if item has been picked up
# ) * i

# Colours for rendering
FLOOR_COL = (176, 176, 176)
PLAYER_COL = (255, 215, 0)
ITEM_COL = (255, 69, 0)
BAY_COL = (0, 100, 0)
PALLET_COL = (139, 69, 19)
BLACK = (0, 0, 0)


class WarehouseEnv(Env):
    def __init__(self, game_length=1000, render_mode="human", render_speed=20):
        super().__init__()
        self.game = WarehouseGame()
        self.game_length = game_length
        self.steps_left = self.game_length
        self.render_speed = render_speed

        # Spaces
        self.action_space = Discrete(4)
        self.observation_space = Box(
            low=-127, high=127, shape=(3 * (self.game.max_bays_to_stock + 1),), dtype=np.int8)

        self.render_mode = render_mode

        # pygame utils
        self.cols, self.rows = self.game.warehouse.shape
        self.window_width = self.rows * 40
        self.window_height = self.cols * 40
        self.window_size = (self.window_width, self.window_height)
        self.cell_width = self.window_width // self.rows
        self.cell_height = self.window_height // self.cols
        self.outline_thickness = 2
        self.window_surface = None
        self.clock = None
        self.font = None

    def step(self, action):
        player_val_before = self.game.player_value

        # Actions and how they affect stuff
        result = self.game.process_directional_input(action)
        self.steps_left -= 1
        if self.render_mode == "human":
            self.render()

        # Get the new observation
        obs = self.get_observation()

        # Reward scheme
        if result == "delivered":
            reward = round(100 * player_val_before *
                           (player_val_before / self.game.n_bays_to_stock))
        elif result == "picked up":
            reward = 100
        elif result == "nothing":
            reward = -2
        else:
            reward = -1

        # ### Debugging (lol)
        # print(self.game.warehouse)
        # print(obs)
        # print(reward)

        # Checking whether game is done / terminated
        terminated = self.get_terminated()

        # Truncated
        truncated = False

        # Info dictionary
        info = {}

        return obs, reward, terminated, truncated, info

    def reset(self, seed=None):
        self.game.reset_warehouse()
        self.steps_left = self.game_length
        obs = self.get_observation()
        info = {}
        return obs, info

    def render(self):
        if self.window_surface is None:
            pygame.init()

            if self.render_mode == "human":
                pygame.display.init()
                pygame.display.set_caption("Warehouse")
                self.window_surface = pygame.display.set_mode(
                    self.window_size)
            if self.clock is None:
                self.clock = pygame.time.Clock()
            if self.font is None:
                self.font = pygame.font.Font(None, 24)

        self.window_surface.fill(FLOOR_COL)

        # Iterate through the array and draw the cells
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.game.warehouse[col][row]

                if value == FLOOR:
                    self.draw_cell(row, col, FLOOR_COL)
                elif value == PLAYER:
                    self.draw_cell(row, col, PLAYER_COL)
                elif value > PLAYER:  # Player is holding item(s)
                    self.draw_cell(row, col, ITEM_COL, PLAYER_COL)
                    left = row * self.cell_width
                    top = col * self.cell_height
                    text_surface = self.font.render(str(value), True, BLACK)
                    text_rect = text_surface.get_rect(
                        center=(left + self.cell_width / 2,
                                top + self.cell_height / 2)
                    )
                    self.window_surface.blit(text_surface, text_rect)
                elif value == BAY_NO_ITEM:
                    self.draw_cell(row, col, BAY_COL)
                elif value == BAY_WITH_ITEM:
                    self.draw_cell(row, col, ITEM_COL, BAY_COL)
                elif value == PALLET:
                    self.draw_cell(row, col, PALLET_COL)

        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.render_speed)

    def close(self):
        pass

    def get_observation(self):

        obs = []
        obs.append(self.game.player_x)
        obs.append(self.game.player_y)
        obs.append(self.game.player_value)
        for i, (bay_x, bay_y) in enumerate(self.game.stocked_util):
            # item has been picked up
            if self.game.stocked_util[i] == (127, 127):
                obs.append(0)
                obs.append(0)
                obs.append(1)
            # item distance from player
            else:
                obs.append(self.game.player_x - bay_x)
                obs.append(self.game.player_y - bay_y)
                obs.append(0)

        return np.array(obs).astype(np.int8)

    def get_terminated(self):
        return self.steps_left < 1

    def draw_cell(self, row, col, inner_color, outer_color=None):
        # Positioning the rectangle
        left = row * self.cell_width
        top = col * self.cell_height

        # Drawing the inner color
        pygame.draw.rect(self.window_surface, inner_color,
                         (left, top, self.cell_width, self.cell_height))

        # Drawing the outer color (outline)
        if outer_color:
            pygame.draw.rect(self.window_surface, outer_color, (left, top,
                                                                self.cell_width, self.cell_height), self.outline_thickness)
