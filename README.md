# 🐍 贪吃蛇 - Snake Game

一个用 Python + Pygame 构建的经典贪吃蛇游戏豪华版。

## ✨ 特性

- 🎮 **经典玩法** — 方向键/WASD 控制蛇移动，吃食物增长
- 🏆 **三种难度** — 简单(无障碍) / 中等(5个障碍) / 困难(10个障碍)
- 🎯 **特殊食物** — 15% 概率出现金色特殊食物，分值更高
- 🔇 **音效系统** — 吃食物音效 + 游戏结束音效 + 背景音乐
- 📈 **动态加速** — 每得50分速度提升，最高2倍速
- 🏅 **高分记录** — JSON 文件持久化保存最高分 (5个难度各10名)
- ⏸️ **暂停继续** — 空格键随时暂停
- 🧱 **障碍物系统** — 按难度级别自动生成
- 📦 **可打包分发** — PyInstaller 打包为独立可执行文件

## 🎮 操作方式

| 按键 | 功能 |
|------|------|
| ↑ ↓ ← → 或 W A S D | 控制蛇移动方向 |
| 空格键 (Space) | 暂停 / 继续 |
| P | 暂停 |
| ESC | 返回主菜单 |
| Enter / J | 确认选择 |

## 🚀 快速开始

### 运行游戏

```bash
# 安装依赖
pip install pygame

# 启动游戏
python -m src
```

### 打包为独立可执行文件

```bash
pip install pyinstaller
pyinstaller build.spec
./dist/snake_game
```

## 📁 项目结构

```
snake_game/
├── src/
│   ├── __main__.py          # 入口点
│   ├── game.py              # 游戏主类 + 场景管理器
│   ├── config.py            # 配置常量
│   ├── entities/            # 游戏实体
│   │   ├── snake.py         # 蛇 (移动/碰撞/渲染)
│   │   ├── food.py          # 食物 (生成/分值/渲染)
│   │   └── obstacle.py      # 障碍物 (生成/渲染)
│   ├── scenes/              # 游戏场景
│   │   ├── menu_scene.py    # 主菜单 + 难度选择
│   │   ├── play_scene.py    # 核心游戏逻辑
│   │   ├── pause_scene.py   # 暂停覆盖层
│   │   └── game_over_scene.py # 结束画面
│   ├── managers/            # 管理器
│   │   ├── sound_manager.py # 音效系统
│   │   ├── score_manager.py # 高分记录
│   │   └── resource_manager.py # 资源路径
│   └── utils/
│       └── helpers.py       # 工具函数
├── assets/
│   ├── fonts/               # 字体文件
│   └── sounds/              # 音效文件
├── tests/                   # 单元测试
├── build.spec               # PyInstaller 配置
└── pyproject.toml           # 项目元数据
```

## 🗺️ 游戏流程

```
主菜单 → 选择难度 → 开始游戏 → 游玩 → 暂停(可选) → 游戏结束 → 查看分数 → 重新开始
```

## 🧪 运行测试

```bash
python -m pytest tests/ -v
```

## 🛠️ 技术栈

- **Python** 3.10+
- **Pygame** 2.0+ — 游戏引擎
- **PyInstaller** — 打包分发
- **pytest** — 单元测试

## 📄 许可证

MIT License
