import os
from typing import Tuple, Optional
import pygame
from src.config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_COLS, GRID_ROWS,
    COLORS
)
from src.managers.resource_manager import resource_path


def grid_to_pixel(col: int, row: int) -> Tuple[int, int]:
    x = GRID_OFFSET_X + col * CELL_SIZE
    y = GRID_OFFSET_Y + row * CELL_SIZE
    return (x, y)


def draw_grid(surface: pygame.Surface):
    for col in range(GRID_COLS + 1):
        x = GRID_OFFSET_X + col * CELL_SIZE
        pygame.draw.line(surface, COLORS["GRID_LINE"],
                        (x, GRID_OFFSET_Y),
                        (x, GRID_OFFSET_Y + GRID_ROWS * CELL_SIZE))
    for row in range(GRID_ROWS + 1):
        y = GRID_OFFSET_Y + row * CELL_SIZE
        pygame.draw.line(surface, COLORS["GRID_LINE"],
                        (GRID_OFFSET_X, y),
                        (GRID_OFFSET_X + GRID_COLS * CELL_SIZE, y))


def draw_text(surface: pygame.Surface, text: str,
              pos: Tuple[int, int], color: Tuple[int, int, int] = COLORS["WHITE"],
              size: int = 24, font_name: Optional[str] = None,
              center: bool = False) -> None:
    font = _get_font(size, font_name, cjk=_has_cjk(text) and font_name is None)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    surface.blit(text_surface, text_rect)


def draw_text_centered(surface: pygame.Surface, text: str,
                       center_pos: Tuple[int, int],
                       color: Tuple[int, int, int] = COLORS["WHITE"],
                       size: int = 24, font_name: Optional[str] = None) -> None:
    draw_text(surface, text, center_pos, color, size, font_name, center=True)


_font_cache = {}
_CJK_FONT_CACHED = None  # None=unchecked, ""=not found, str=path


def _has_cjk(text: str) -> bool:
    """检测文本是否包含 CJK 中日韩字符"""
    for char in text:
        cp = ord(char)
        if (0x4E00 <= cp <= 0x9FFF or   # CJK统一表意文字
            0x3000 <= cp <= 0x303F or   # CJK符号和标点
            0xFF00 <= cp <= 0xFFEF):    # 全角字符
            return True
    return False


def _get_cjk_font_path() -> str:
    global _CJK_FONT_CACHED
    if _CJK_FONT_CACHED is None:
        p = resource_path(os.path.join("assets", "fonts", "DroidSansFallbackFull.ttf"))
        _CJK_FONT_CACHED = p if os.path.exists(p) else ""
    return _CJK_FONT_CACHED


def _get_font(size: int, font_name: Optional[str] = None, cjk: bool = False):
    key = (font_name, size, cjk)
    if key in _font_cache:
        return _font_cache[key]

    try:
        if font_name:
            font = pygame.font.Font(font_name, size)
        elif cjk:
            cjk_path = _get_cjk_font_path()
            if cjk_path:
                font = pygame.font.Font(cjk_path, size)
            else:
                font = pygame.font.Font(None, size)
        else:
            font_path = resource_path(os.path.join("assets", "fonts", "PressStart2P.ttf"))
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, size)
            else:
                font = pygame.font.Font(None, size)
    except (pygame.error, FileNotFoundError):
        font = pygame.font.Font(None, size)

    _font_cache[key] = font
    return font


def draw_rect(surface: pygame.Surface, color: Tuple[int, int, int],
              x: int, y: int, width: int, height: int,
              border_radius: int = 0, alpha: Optional[int] = None):
    if alpha is not None:
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((*color, alpha))
        surface.blit(s, (x, y))
    else:
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)
