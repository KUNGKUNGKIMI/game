import sys
from typing import Optional
import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, FPS
from src.scenes.base_scene import Scene


class SceneManager:
    """场景管理器 - 状态机"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.scene: Optional[Scene] = None
        self.clock = pygame.time.Clock()
        self.running = False

    def go_to(self, scene: Scene) -> None:
        """切换到新场景"""
        if self.scene:
            self.scene.exit()
        self.scene = scene
        self.scene.manager = self
        self.scene.enter()

    def run(self, initial_scene: Scene) -> None:
        """主循环"""
        self.go_to(initial_scene)
        self.running = True

        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # 秒

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            if self.scene:
                self.scene.handle_events(events)
                self.scene.update(dt)
                self.scene.render(self.screen)

            pygame.display.flip()


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.scene_manager = SceneManager(self.screen)

    def setup(self):
        """设置初始场景"""
        # 延迟导入避免循环依赖
        from src.scenes.menu_scene import MenuScene
        self.scene_manager.go_to(MenuScene())

    def run(self):
        """运行游戏"""
        if self.scene_manager.scene is None:
            self.setup()
        if self.scene_manager.scene is None:
            raise RuntimeError("无法初始化场景")
        self.scene_manager.run(self.scene_manager.scene)
        pygame.quit()
        sys.exit()
