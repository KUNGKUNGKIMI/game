import sys
from typing import List
import pygame
from src.scenes.base_scene import Scene
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, DIFFICULTIES
from src.utils.helpers import draw_text_centered, draw_text


class MenuScene(Scene):
    """游戏主菜单场景，包含难度选择功能"""

    def __init__(self) -> None:
        super().__init__()
        self.state = "menu"
        self.selected = 0
        self.menu_items = ["开始游戏", "难度选择", "退出"]
        self.difficulties = list(DIFFICULTIES.keys())
        self.selected_difficulty = 1
        self.current_difficulty = "medium"
        self.sm = None  # type: ignore[assignment]

    def enter(self) -> None:
        """进入场景时加载最高分数据"""
        from src.managers.score_manager import ScoreManager
        self.sm = ScoreManager()

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self._handle_menu_input(event)
                elif self.state == "difficulty":
                    self._handle_difficulty_input(event)

    def _handle_menu_input(self, event: pygame.event.Event) -> None:
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.menu_items)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.menu_items)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_j):
            self._select_menu_item()

    def _handle_difficulty_input(self, event: pygame.event.Event) -> None:
        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected_difficulty = (self.selected_difficulty - 1) % len(self.difficulties)
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_difficulty = (self.selected_difficulty + 1) % len(self.difficulties)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_j):
            self.current_difficulty = self.difficulties[self.selected_difficulty]
            self.state = "menu"
        elif event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.state = "menu"

    def _select_menu_item(self) -> None:
        assert self.manager is not None
        if self.selected == 0:
            from src.scenes.play_scene import PlayScene  # type: ignore[import-untyped]
            self.manager.go_to(PlayScene(self.current_difficulty))
        elif self.selected == 1:
            self.state = "difficulty"
        elif self.selected == 2:
            pygame.quit()
            sys.exit()

    def update(self, dt: float) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        screen.fill(COLORS["BLACK"])

        if self.state == "menu":
            self._render_menu(screen)
        elif self.state == "difficulty":
            self._render_difficulty(screen)

    def _render_menu(self, screen: pygame.Surface) -> None:
        draw_text_centered(screen, "SNAKE", (WINDOW_WIDTH // 2, 100),
                          COLORS["GREEN"], 64)
        draw_text_centered(screen, "经典贪吃蛇", (WINDOW_WIDTH // 2, 150),
                          COLORS["GRAY"], 20)

        for i, item in enumerate(self.menu_items):
            y = 260 + i * 50
            color = COLORS["SNAKE_HEAD"] if i == self.selected else COLORS["GRAY"]
            prefix = "▶ " if i == self.selected else "  "
            draw_text_centered(screen, f"{prefix}{item}",
                             (WINDOW_WIDTH // 2, y), color, 28)

        diff_info = DIFFICULTIES[self.current_difficulty]
        draw_text_centered(screen,
            f"当前难度: {diff_info['label']} | 速度: {diff_info['speed']} | 障碍: {diff_info['obstacles']}",
            (WINDOW_WIDTH // 2, 430), COLORS["DARK_GREEN"], 16)

        self._render_high_scores(screen)
        self._render_snake_decoration(screen)

        draw_text_centered(screen, "↑ ↓ / WS 选择  |  Enter / 空格 确认",
                         (WINDOW_WIDTH // 2, 550), COLORS["DARK_GRAY"], 14)

    def _render_high_scores(self, screen: pygame.Surface) -> None:
        assert self.sm is not None
        y_start = WINDOW_HEIGHT - 100
        draw_text(screen, "最高分", (WINDOW_WIDTH - 180, y_start - 25),
                 COLORS["DARK_GREEN"], 16)
        for i, diff in enumerate(self.difficulties):
            top = self.sm.get_highest_score(diff)
            label = DIFFICULTIES[diff]["label"]
            score_color = COLORS["GREEN"] if top > 0 else COLORS["DARK_GRAY"]
            draw_text(screen, f"{label}: {top}",
                     (WINDOW_WIDTH - 180, y_start + i * 22),
                     score_color, 14)

    def _render_snake_decoration(self, screen: pygame.Surface) -> None:
        import math
        center_x = WINDOW_WIDTH // 2
        start_y = 460
        num_dots = 30
        wave_amplitude = 8
        wave_length = 60

        for i in range(num_dots):
            x = center_x - 200 + i * 14
            y = start_y + int(wave_amplitude * math.sin(i / wave_length * 2 * math.pi))
            color = COLORS["SNAKE_HEAD"] if i == 0 else COLORS["DARK_GREEN"]
            radius = 4 if i == 0 else 3
            pygame.draw.circle(screen, color, (x, y), radius)

    def _render_difficulty(self, screen: pygame.Surface) -> None:
        draw_text_centered(screen, "选择难度", (WINDOW_WIDTH // 2, 100),
                          COLORS["GREEN"], 48)

        for i, diff_key in enumerate(self.difficulties):
            diff = DIFFICULTIES[diff_key]
            y = 220 + i * 90
            is_selected = i == self.selected_difficulty
            color = COLORS["SNAKE_HEAD"] if is_selected else COLORS["GRAY"]
            prefix = "▶ " if is_selected else "  "

            draw_text_centered(screen, f"{prefix}{diff['label']}",
                             (WINDOW_WIDTH // 2, y), color, 32)
            draw_text_centered(screen,
                f"速度: {diff['speed']}  |  障碍物: {diff['obstacles']} 个",
                (WINDOW_WIDTH // 2, y + 30), COLORS["DARK_GREEN"], 16)

        draw_text_centered(screen, "ESC / ← 返回主菜单", (WINDOW_WIDTH // 2, 520),
                          COLORS["DARK_GRAY"], 16)
