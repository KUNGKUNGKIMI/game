import os
from typing import Tuple, Optional
import pygame
from src.config import (
    CELL_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_COLS, GRID_ROWS,
    COLORS
)
from src.managers.resource_manager import resource_path


_FALLBACK_FONTS_LOADED = False
_FALLBACK_FONT_PATH = ""


def _init_fallback_fonts():
    global _FALLBACK_FONTS_LOADED, _FALLBACK_FONT_PATH
    if _FALLBACK_FONTS_LOADED:
        return
    cjk_path = resource_path(os.path.join("assets", "fonts", "DroidSansFallbackFull.ttf"))
    if os.path.exists(cjk_path):
        _FALLBACK_FONT_PATH = cjk_path
    _FALLBACK_FONTS_LOADED = True


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
    font = _get_font(size, font_name)
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


def _get_font(size: int, font_name: Optional[str] = None):
    key = (font_name, size)
    if key in _font_cache:
        return _font_cache[key]

    _init_fallback_fonts()
    font = None

    try:
        if font_name:
            font = pygame.font.Font(font_name, size)
        else:
            pp_path = resource_path(os.path.join("assets", "fonts", "PressStart2P.ttf"))
            if os.path.exists(pp_path):
                font = pygame.font.Font(pp_path, size)
            else:
                font = pygame.font.Font(None, size)
    except (pygame.error, FileNotFoundError):
        font = None

    # 回退链：PressStart2P失败 → DroidSansFallback
    if font is None and _FALLBACK_FONT_PATH:
        try:
            font = pygame.font.Font(_FALLBACK_FONT_PATH, size)
        except (pygame.error, FileNotFoundError):
            font = None

    # 终极回退：系统默认字体
    if font is None:
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
