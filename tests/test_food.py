from src.entities.food import Food
from src.entities.obstacle import Obstacle
from src.config import GRID_COLS, GRID_ROWS


def test_food_in_grid():
    snake_positions = [(5, 5), (4, 5), (3, 5)]
    food = Food(snake_positions)
    assert food.position is not None
    col, row = food.position
    assert 0 <= col < GRID_COLS
    assert 0 <= row < GRID_ROWS


def test_food_avoids_snake():
    snake_positions = [(5, 5), (4, 5), (3, 5)]
    for _ in range(50):
        food = Food(snake_positions)
        assert food.position not in snake_positions


def test_obstacle_generation():
    obstacle = Obstacle()
    snake_positions = [(10, 10), (9, 10), (8, 10)]
    obstacle.generate("medium", snake_positions)
    assert len(obstacle.positions) == 5
    for pos in obstacle.positions:
        assert pos not in snake_positions
        col, row = pos
        assert 0 <= col < GRID_COLS
        assert 0 <= row < GRID_ROWS


def test_obstacle_easy_none():
    obstacle = Obstacle()
    obstacle.generate("easy", [(10, 10)])
    assert len(obstacle.positions) == 0


def test_food_value_default():
    snake_positions = [(5, 5), (4, 5), (3, 5)]
    food = Food(snake_positions)
    assert food.value in (10, 50)
    assert isinstance(food.is_special, bool)
