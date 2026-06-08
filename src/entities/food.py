import random
from typing import Tuple, List
import pygame
from src.config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_COLS, GRID_ROWS,
    COLORS, SCORE_PER_FOOD, SPECIAL_FOOD_SCORE, SPECIAL_FOOD_CHANCE
)


class Food:
    def __init__(self, snake_positions: List[Tuple[int, int]],
                 obstacle_positions: List[Tuple[int, int]] | None = None):
        self.position = None
        self.value = SCORE_PER_FOOD
        self.is_special = False
        self.spawn(snake_positions, obstacle_positions or [])

    def spawn(self, snake_positions: List[Tuple[int, int]],
              obstacle_positions: List[Tuple[int, int]]):
        """在空闲位置随机生成食物"""
        occupied = set(snake_positions + obstacle_positions)
        available = [(c, r) for c in range(GRID_COLS) for r in range(GRID_ROWS)
                     if (c, r) not in occupied]
        if not available:
            return
        self.position = random.choice(available)
        self.is_special = random.random() < SPECIAL_FOOD_CHANCE
        self.value = SPECIAL_FOOD_SCORE if self.is_special else SCORE_PER_FOOD

    def render(self, surface: pygame.Surface, time_ms: int = 0):
        if not self.position:
            return
        col, row = self.position
        x = GRID_OFFSET_X + col * CELL_SIZE
        y = GRID_OFFSET_Y + row * CELL_SIZE
        color = COLORS["FOOD_GLOW"] if self.is_special else COLORS["FOOD_COLOR"]
        if self.is_special:
            alpha = abs(((time_ms // 200) % 4) - 2) * 60
            color = tuple(min(c + alpha, 255) for c in color)
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(surface, color, center, radius)
