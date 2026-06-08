import os

import pygame

from src.managers.resource_manager import resource_path


class SoundManager:
    """管理游戏音效和背景音乐"""

    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self._initialized = False
        self._enabled = True

    def init(self):
        """初始化 pygame.mixer"""
        if self._initialized:
            return
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self._initialized = True
        except pygame.error:
            self._enabled = False

    def load_sounds(self):
        """加载所有音效文件"""
        if not self._enabled:
            return
        sound_files = {
            "eat": os.path.join("assets", "sounds", "eat.wav"),
            "game_over": os.path.join("assets", "sounds", "game_over.wav"),
        }
        for name, path in sound_files.items():
            try:
                full_path = resource_path(path)
                if os.path.exists(full_path):
                    self.sounds[name] = pygame.mixer.Sound(full_path)
                else:
                    self._generate_sound(name)
            except pygame.error:
                pass

    def _generate_sound(self, name: str):
        """生成简单的程序音效作为后备"""
        import array
        import math

        sample_rate = 22050
        if name == "eat":
            duration = 0.1
            freq_start = 400
            freq_end = 800
        elif name == "game_over":
            duration = 0.5
            freq_start = 200
            freq_end = 80
        else:
            return

        n_samples = int(sample_rate * duration)
        buf = array.array('h', [0]) * n_samples
        for i in range(n_samples):
            t = i / sample_rate
            freq = freq_start + (freq_end - freq_start) * (i / n_samples)
            val = int(8000 * math.sin(2 * math.pi * freq * t) * (1 - i / n_samples))
            buf[i] = max(-32768, min(32767, val))

        sound = pygame.mixer.Sound(buffer=buf)
        self.sounds[name] = sound

    def play_sound(self, name: str):
        """播放音效"""
        if not self._enabled or name not in self.sounds:
            return
        self.sounds[name].play()

    def play_music(self, name: str = "bg_music"):
        """播放背景音乐"""
        if not self._enabled:
            return
        try:
            path = resource_path(os.path.join("assets", "sounds", f"{name}.ogg"))
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.music_playing = True
        except pygame.error:
            pass

    def stop_music(self):
        """停止背景音乐"""
        if self._enabled and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def set_volume(self, volume: float):
        """设置音量 0.0-1.0"""
        if self._enabled:
            pygame.mixer.music.set_volume(volume)
