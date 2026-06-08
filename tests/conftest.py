import os
import sys

# 确保 src 可导入
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

# 设置 dummy video driver 避免 pygame 显示问题
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# 初始化 pygame 的 font 模块（某些测试可能间接依赖）
import pygame
pygame.display.init()
pygame.font.init()
