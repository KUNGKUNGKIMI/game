"""贪吃蛇游戏入口点 — 支持 python -m src 启动"""
from src.game import Game


def main():
    game = Game()
    game.setup()
    game.run()


if __name__ == "__main__":
    main()
