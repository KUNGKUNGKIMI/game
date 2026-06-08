import json
import os
from typing import Dict, List

from src.config import HIGH_SCORE_FILE


class ScoreManager:
    """管理最高分记录，单例模式"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.scores: Dict[str, List[int]] = {"easy": [], "medium": [], "hard": []}
        self.load_high_scores()

    def _get_file_path(self) -> str:
        return os.path.expanduser(HIGH_SCORE_FILE)

    def load_high_scores(self):
        """从 JSON 文件加载分数"""
        path = self._get_file_path()
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    self.scores = data
        except (json.JSONDecodeError, IOError):
            self.scores = {"easy": [], "medium": [], "hard": []}

    def save_score(self, score: int, difficulty: str):
        """保存分数"""
        if difficulty not in self.scores:
            self.scores[difficulty] = []
        self.scores[difficulty].append(score)
        self.scores[difficulty].sort(reverse=True)
        self.scores[difficulty] = self.scores[difficulty][:10]
        self._write_file()

    def _write_file(self):
        path = self._get_file_path()
        try:
            with open(path, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except IOError:
            pass

    def get_top_scores(self, difficulty: str, limit: int = 5) -> List[int]:
        """获取指定难度的前 N 名分数"""
        scores = self.scores.get(difficulty, [])
        return scores[:limit]

    def get_highest_score(self, difficulty: str) -> int:
        """获取指定难度的最高分"""
        scores = self.scores.get(difficulty, [])
        return scores[0] if scores else 0

    def is_new_high_score(self, score: int, difficulty: str) -> bool:
        """判断是否为新最高分"""
        return score > self.get_highest_score(difficulty)

    def reset(self):
        """重置所有分数（测试用）"""
        self.scores = {"easy": [], "medium": [], "hard": []}
