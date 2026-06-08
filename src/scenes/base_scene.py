from abc import ABC, abstractmethod
from typing import List, Optional, Any
import pygame


class Scene(ABC):
    """场景抽象基类"""

    def __init__(self):
        self.manager: Optional[Any] = None  # 由 SceneManager 设置

    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """处理事件"""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """更新逻辑（dt 是帧时间，单位秒）"""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """渲染到屏幕"""
        pass

    def enter(self) -> None:
        """进入场景时的钩子"""
        pass

    def exit(self) -> None:
        """离开场景时的钩子"""
        pass
