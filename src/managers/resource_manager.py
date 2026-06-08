import os
import sys


def resource_path(relative_path: str) -> str:
    """获取资源的绝对路径，兼容 PyInstaller 打包后"""
    try:
        # PyInstaller 打包后使用 _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发模式，使用项目根目录
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
