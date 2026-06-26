# map.py
import os
import pygame
from obstacle import Obstacle, Empty, Brick, Steel, Water, Forest, Base
from constants import ROWS, COLS, TILE_SIZE

TOTAL_LEVELS = 3
BASE_DIR = os.path.dirname(__file__)


class Map:
    def __init__(self, level=1):
        self.current_level = level
        self.grid = [[Empty() for _ in range(COLS)] for _ in range(ROWS)]
        self.load_level(os.path.join(BASE_DIR, "levels", f"level{level}.txt"))

        self.images = {
            Brick: pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "assets", "brick.png")),
                (TILE_SIZE, TILE_SIZE),
            ),
            Steel: pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "assets", "steel.png")),
                (TILE_SIZE, TILE_SIZE),
            ),
            Water: pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "assets", "water.png")),
                (TILE_SIZE, TILE_SIZE),
            ),
            Forest: pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "assets", "forest.png")),
                (TILE_SIZE, TILE_SIZE),
            ),
            Base: pygame.transform.scale(
                pygame.image.load(os.path.join(BASE_DIR, "assets", "base.png")),
                (TILE_SIZE, TILE_SIZE),
            ),
        }

    def load_level(self, filename):
        mapping = {
            ".": Empty,
            "B": Brick,
            "S": Steel,
            "W": Water,
            "F": Forest,
            "X": Base,
        }

        if not os.path.isabs(filename):
            filename = os.path.join(BASE_DIR, filename)

        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                self.grid[y][x] = mapping.get(char, Empty)()  # gọi constructor

    def next_level(self):
        next_num = (self.current_level % TOTAL_LEVELS) + 1
        self.current_level = next_num
        self.load_level(f"levels/level{next_num}.txt")

    def _load_default(self):
        base_x = COLS // 2
        base_y = ROWS - 1
        self.grid[base_y][base_x] = Base()

    def get_tile(self, x, y):
        if 0 <= x < COLS and 0 <= y < ROWS:
            return self.grid[y][x]
        return Steel()  # ngoài biên coi như Steel

    def is_passable(self, x, y):
        return self.get_tile(x, y).passable  

    def set_tile(self, x, y, tile_type):
        if 0 <= x < COLS and 0 <= y < ROWS:
            self.grid[y][x] = tile_type() if isinstance(tile_type, type) else tile_type

    def draw(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                tile = self.grid[row][col]
                img = self.images.get(type(tile))  

                if img:
                    screen.blit(img, (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    pygame.draw.rect(
                        screen,
                        tile.color,  
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )