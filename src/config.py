# 窗口和网格
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_COLS = 20
GRID_ROWS = 20
CELL_SIZE = 30
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_COLS * CELL_SIZE) // 2  # 100
GRID_OFFSET_Y = (WINDOW_HEIGHT - GRID_ROWS * CELL_SIZE) // 2  # 0

# 颜色 (R, G, B)
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "GREEN": (0, 200, 0),
    "DARK_GREEN": (0, 150, 0),
    "RED": (200, 0, 0),
    "DARK_RED": (150, 0, 0),
    "GRAY": (100, 100, 100),
    "DARK_GRAY": (50, 50, 50),
    "YELLOW": (255, 255, 0),
    "BLUE": (0, 100, 200),
    "SNAKE_HEAD": (0, 230, 0),
    "SNAKE_BODY": (0, 180, 0),
    "FOOD_COLOR": (255, 50, 50),
    "FOOD_GLOW": (255, 100, 100),
    "OBSTACLE": (80, 80, 80),
    "GRID_LINE": (30, 30, 30),
    "OVERLAY": (0, 0, 0, 128),
}

# 方向
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

# 难度参数: {名称: (速度FPS, 障碍物数量, 显示名)}
DIFFICULTIES = {
    "easy": {"speed": 8, "obstacles": 0, "label": "简单"},
    "medium": {"speed": 12, "obstacles": 5, "label": "中等"},
    "hard": {"speed": 18, "obstacles": 10, "label": "困难"},
}

# FPS
FPS = 60

# 分数
SCORE_PER_FOOD = 10
SPECIAL_FOOD_SCORE = 50
SPECIAL_FOOD_CHANCE = 0.15  # 15% chance
SPEED_BOOST_INTERVAL = 50   # 每50分加速
MAX_SPEED_MULTIPLIER = 2.0  # 最大2倍速

# 文件路径
HIGH_SCORE_FILE = "~/.snake_highscores.json"

# 窗口标题
GAME_TITLE = "🐍 贪吃蛇 - Snake"

# 初始蛇
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_X = GRID_COLS // 2
INITIAL_SNAKE_Y = GRID_ROWS // 2
INITIAL_DIRECTION = (1, 0)  # 向右
