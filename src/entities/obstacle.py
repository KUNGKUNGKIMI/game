import random
from typing import List, Tuple
import pygame
from src.config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_COLS, GRID_ROWS,
    COLORS, DIFFICULTIES
)


class Obstacle:
    def __init__(self):
        self.positions: List[Tuple[int, int]] = []

    def generate(self, difficulty: str,
                 snake_positions: List[Tuple[int, int]] | None = None,
                 food_positions: List[Tuple[int, int]] | None = None):
        """根据难度生成障碍物"""
        count = DIFFICULTIES.get(difficulty, DIFFICULTIES["easy"])["obstacles"]
        occupied = set(snake_positions or [])
        if food_positions:
            occupied.update(food_positions)

        center_x, center_y = GRID_COLS // 2, GRID_ROWS // 2
        center_zone = set()
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                cx, cy = center_x + dx, center_y + dy
                if 0 <= cx < GRID_COLS and 0 <= cy < GRID_ROWS:
                    center_zone.add((cx, cy))

        self.positions = []
        for _ in range(count):
            available = []
            for c in range(GRID_COLS):
                for r in range(GRID_ROWS):
                    pos = (c, r)
                    if (pos not in occupied and pos not in center_zone
                            and pos not in self.positions):
                        available.append(pos)
            if available:
                pos = random.choice(available)
                self.positions.append(pos)
                occupied.add(pos)

    def render(self, surface: pygame.Surface):
        for col, row in self.positions:
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(surface, COLORS["OBSTACLE"], rect, border_radius=3)
            inner_rect = pygame.Rect(x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10)
            pygame.draw.rect(surface, COLORS["DARK_GRAY"], inner_rect, border_radius=2)
