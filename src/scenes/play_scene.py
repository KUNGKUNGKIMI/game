import pygame

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, DIFFICULTIES,
    SPEED_BOOST_INTERVAL, MAX_SPEED_MULTIPLIER,
)
from src.entities.snake import Snake
from src.entities.food import Food
from src.entities.obstacle import Obstacle
from src.managers.score_manager import ScoreManager
from src.managers.sound_manager import SoundManager
from src.scenes.base_scene import Scene
from src.utils.helpers import draw_grid, draw_text


class PlayScene(Scene):
    """游戏核心场景 — 包含所有游戏逻辑"""

    def __init__(self, difficulty: str = "medium"):
        super().__init__()
        self.difficulty = difficulty
        self.diff_config = DIFFICULTIES[difficulty]
        self.base_speed = self.diff_config["speed"]
        self.current_speed = self.base_speed

        self.snake = Snake()
        self.food = None
        self.obstacle = Obstacle()

        self.score_mgr = ScoreManager()
        self.sound_mgr = SoundManager()

        self.score = 0
        self.move_timer = 0.0
        self.game_time = 0.0
        self.spawn_food()

    # ── 食物 ──────────────────────────────────────────────────

    def spawn_food(self):
        """生成食物，排除蛇身和障碍物位置"""
        self.food = Food(
            self.snake.get_body_positions(),
            self.obstacle.positions
        )

    # ── 场景生命周期 ──────────────────────────────────────────

    def enter(self):
        self.obstacle.generate(
            self.difficulty,
            self.snake.get_body_positions(),
            [self.food.position] if self.food and self.food.position else None,
        )
        self.spawn_food()
        self.sound_mgr.init()
        self.sound_mgr.load_sounds()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                elif key == pygame.K_w:
                    self.snake.change_direction((0, -1))
                elif key == pygame.K_s:
                    self.snake.change_direction((0, 1))
                elif key == pygame.K_a:
                    self.snake.change_direction((-1, 0))
                elif key == pygame.K_d:
                    self.snake.change_direction((1, 0))
                elif key in (pygame.K_SPACE, pygame.K_p):
                    from src.scenes.pause_scene import PauseScene
                    self.manager.go_to(PauseScene(self))
                elif key == pygame.K_ESCAPE:
                    self.sound_mgr.stop_music()
                    from src.scenes.menu_scene import MenuScene
                    self.manager.go_to(MenuScene())

    def update(self, dt):
        self.game_time += dt
        self.move_timer += dt

        move_interval = 1.0 / self.current_speed

        if self.move_timer >= move_interval:
            self.move_timer = 0.0
            self._game_tick()

    # ── 核心游戏逻辑 ──────────────────────────────────────────

    def _game_tick(self):
        """每一步游戏逻辑"""
        # 方向队列 → 移动
        self.snake.move()

        # 碰撞检测
        head = self.snake.get_head_pos()

        # 撞墙
        if self.snake.check_wall_collision():
            self._game_over()
            return

        # 撞自身
        if self.snake.check_self_collision():
            self._game_over()
            return

        # 撞障碍物
        if head in self.obstacle.positions:
            self._game_over()
            return

        # 吃食物
        if self.food and self.food.position and head == self.food.position:
            self.snake.grow()
            self.score += self.food.value
            self.sound_mgr.play_sound("eat")
            self.spawn_food()

            # 每 50 分加速
            if self.score % SPEED_BOOST_INTERVAL == 0:
                speed_mult = min(
                    MAX_SPEED_MULTIPLIER,
                    1.0 + (self.score // SPEED_BOOST_INTERVAL) * 0.15,
                )
                self.current_speed = int(self.base_speed * speed_mult)

    def _game_over(self):
        """游戏结束"""
        self.sound_mgr.play_sound("game_over")
        self.score_mgr.save_score(self.score, self.difficulty)
        self.sound_mgr.stop_music()

        from src.scenes.game_over_scene import GameOverScene
        self.manager.go_to(GameOverScene(self.score, self.difficulty))

    # ── 渲染 ──────────────────────────────────────────────────

    def render(self, screen):
        screen.fill(COLORS["BLACK"])

        # 绘制网格
        draw_grid(screen)

        # 渲染实体
        self.obstacle.render(screen)
        if self.food:
            self.food.render(screen, int(self.game_time * 1000))
        self.snake.render(screen)

        # HUD
        diff_label = DIFFICULTIES[self.difficulty]["label"]
        hud_text = f"分数: {self.score}  |  难度: {diff_label}  |  速度: {self.current_speed}"
        draw_text(screen, hud_text, (10, 10), COLORS["WHITE"], 20)

        # 最高分
        high = self.score_mgr.get_highest_score(self.difficulty)
        draw_text(
            screen,
            f"最高: {high}",
            (WINDOW_WIDTH - 150, 10),
            COLORS["DARK_GREEN"],
            16,
        )

        # 控制提示
        draw_text(
            screen,
            "空格暂停 | ESC退出",
            (WINDOW_WIDTH - 180, WINDOW_HEIGHT - 30),
            COLORS["DARK_GRAY"],
            14,
        )
