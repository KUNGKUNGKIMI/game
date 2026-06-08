from collections import deque
from typing import List, Tuple
import pygame
from src.config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_COLS, GRID_ROWS,
    COLORS, INITIAL_SNAKE_LENGTH, INITIAL_SNAKE_X, INITIAL_SNAKE_Y,
    INITIAL_DIRECTION
)


class Snake:
    def __init__(self):
        # 蛇身: deque of (col, row), 头部在左
        body = deque()
        start_x, start_y = INITIAL_SNAKE_X, INITIAL_SNAKE_Y
        # 从右向左生长（默认向右移动）
        for i in range(INITIAL_SNAKE_LENGTH):
            body.appendleft((start_x - i, start_y))
        self.body = body
        self.direction = INITIAL_DIRECTION  # 当前方向
        self.direction_queue: List[Tuple[int, int]] = []  # 方向队列（缓冲输入）
        self.grow_flag = False  # 下次移动时增长

    def get_head_pos(self) -> Tuple[int, int]:
        return self.body[0]

    def change_direction(self, new_dir: Tuple[int, int]):
        """将方向加入队列，队列最大长度3"""
        if len(self.direction_queue) >= 3:
            return
        # 确定实际生效方向（检查队列尾或当前方向）
        last_dir = self.direction_queue[-1] if self.direction_queue else self.direction
        # 不能直接反向
        if (new_dir[0] + last_dir[0] == 0 and new_dir[1] + last_dir[1] == 0):
            return
        # 不能重复相同方向（连续同一方向浪费）
        if last_dir == new_dir:
            return
        self.direction_queue.append(new_dir)

    def move(self):
        """移动蛇：根据方向队列头部移动"""
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        head = self.get_head_pos()
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.appendleft(new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        """设置下次移动时增长"""
        self.grow_flag = True

    def check_wall_collision(self) -> bool:
        head = self.get_head_pos()
        return (head[0] < 0 or head[0] >= GRID_COLS or
                head[1] < 0 or head[1] >= GRID_ROWS)

    def check_self_collision(self) -> bool:
        head = self.get_head_pos()
        return head in list(self.body)[1:]  # 检查头部是否在身体中

    def check_collision_with(self, positions: List[Tuple[int, int]]) -> bool:
        head = self.get_head_pos()
        return head in positions

    def get_body_positions(self) -> List[Tuple[int, int]]:
        return list(self.body)

    def render(self, surface: pygame.Surface):
        """渲染蛇"""
        for i, (col, row) in enumerate(self.body):
            x = GRID_OFFSET_X + col * CELL_SIZE
            y = GRID_OFFSET_Y + row * CELL_SIZE
            color = COLORS["SNAKE_HEAD"] if i == 0 else COLORS["SNAKE_BODY"]
            rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            # 蛇头用圆角矩形
            if i == 0:
                pygame.draw.rect(surface, color, rect, border_radius=4)
            else:
                pygame.draw.rect(surface, color, rect, border_radius=2)
