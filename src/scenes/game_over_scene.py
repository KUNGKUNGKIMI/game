import pygame
from src.scenes.base_scene import Scene
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, DIFFICULTIES
from src.managers.score_manager import ScoreManager
from src.utils.helpers import draw_text_centered


class GameOverScene(Scene):
    def __init__(self, score: int, difficulty: str):
        super().__init__()
        self.score = score
        self.difficulty = difficulty
        self.score_mgr = ScoreManager()
        self.is_new_high = self.score_mgr.is_new_high_score(score, difficulty)
        self.elapsed = 0.0

    def enter(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_r, pygame.K_RETURN):
                    from src.scenes.play_scene import PlayScene
                    self.manager.go_to(PlayScene(self.difficulty))
                elif event.key == pygame.K_ESCAPE:
                    from src.scenes.menu_scene import MenuScene
                    self.manager.go_to(MenuScene())

    def update(self, dt):
        self.elapsed += dt

    def render(self, screen):
        screen.fill(COLORS["BLACK"])

        draw_text_centered(screen, "GAME OVER",
                         (WINDOW_WIDTH // 2, 120),
                         COLORS["RED"], 64)

        draw_text_centered(screen, "最终分数",
                         (WINDOW_WIDTH // 2, 220),
                         COLORS["GRAY"], 24)
        draw_text_centered(screen, str(self.score),
                         (WINDOW_WIDTH // 2, 270),
                         COLORS["WHITE"], 48)

        diff_label = DIFFICULTIES[self.difficulty]["label"]
        draw_text_centered(screen, f"难度: {diff_label}",
                         (WINDOW_WIDTH // 2, 320),
                         COLORS["DARK_GREEN"],                          20)

        high = self.score_mgr.get_highest_score(self.difficulty)
        draw_text_centered(screen, f"最高分: {high}",
                         (WINDOW_WIDTH // 2, 360),
                         COLORS["GRAY"], 20)

        if self.is_new_high:
            alpha = abs(((int(self.elapsed * 3)) % 4) - 2)  # 0,1,2,1,0...
            color_intensity = min(255, 128 + alpha * 64)
            flash_color = (255, color_intensity, 0)
            draw_text_centered(screen, "✦ NEW HIGH SCORE! ✦",
                             (WINDOW_WIDTH // 2, 410),
                             flash_color,                              28)

        draw_text_centered(screen, "按 空格 重新开始  |  按 ESC 返回菜单",
                         (WINDOW_WIDTH // 2, 500),
                         COLORS["DARK_GRAY"], 18)
