import pygame
from src.scenes.base_scene import Scene
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
from src.utils.helpers import draw_text_centered


class PauseScene(Scene):
    """暂停场景 - 覆盖层"""

    def __init__(self, play_scene: Scene):
        super().__init__()
        self.play_scene = play_scene  # 保留游戏场景引用

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_p):
                    # 继续游戏
                    self.play_scene.sound_mgr.play_music()
                    self.manager.go_to(self.play_scene)
                elif event.key == pygame.K_ESCAPE:
                    # 返回主菜单
                    self.play_scene.sound_mgr.stop_music()
                    from src.scenes.menu_scene import MenuScene
                    self.manager.go_to(MenuScene())

    def update(self, dt):
        pass  # 游戏暂停，不需要更新

    def render(self, screen):
        # 先绘制游戏画面（冻结状态）
        self.play_scene.render(screen)

        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # 半透明黑色
        screen.blit(overlay, (0, 0))

        # PAUSED 文本
        draw_text_centered(screen, "PAUSED",
                         (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40),
                         COLORS["GREEN"], 64)

        draw_text_centered(screen, "按 空格 继续  |  按 ESC 返回菜单",
                         (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30),
                         COLORS["WHITE"], 20)
