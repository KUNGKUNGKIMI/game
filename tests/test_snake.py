from src.entities.snake import Snake
from src.config import (
    INITIAL_SNAKE_LENGTH, INITIAL_SNAKE_X, INITIAL_SNAKE_Y,
    INITIAL_DIRECTION, GRID_COLS, GRID_ROWS, DIRECTIONS
)


def test_initial_position():
    snake = Snake()
    assert len(snake.body) == INITIAL_SNAKE_LENGTH
    # 蛇头在 (INITIAL_SNAKE_X - (INITIAL_SNAKE_LENGTH-1), INITIAL_SNAKE_Y)
    # 因为 body 从右向左构建 (appendleft)
    expected_head_x = INITIAL_SNAKE_X - (INITIAL_SNAKE_LENGTH - 1)
    assert snake.get_head_pos() == (expected_head_x, INITIAL_SNAKE_Y)
    assert snake.direction == INITIAL_DIRECTION


def test_move_right():
    snake = Snake()
    head_before = snake.get_head_pos()
    snake.move()
    expected_head = (head_before[0] + 1, head_before[1])
    assert snake.get_head_pos() == expected_head
    assert len(snake.body) == INITIAL_SNAKE_LENGTH  # 长度不变


def test_move_up():
    snake = Snake()
    head_before = snake.get_head_pos()
    snake.change_direction(DIRECTIONS["UP"])
    snake.move()
    expected_head = (head_before[0], head_before[1] - 1)
    assert snake.get_head_pos() == expected_head


def test_cannot_reverse():
    snake = Snake()
    # 当前方向向右，尝试向左（反向）
    snake.change_direction(DIRECTIONS["LEFT"])
    assert len(snake.direction_queue) == 0  # 反向被拒绝


def test_wall_collision():
    snake = Snake()
    # 将蛇移到右边界并继续向右
    while snake.get_head_pos()[0] < GRID_COLS - 1:
        snake.move()
    snake.move()  # 再走一步撞墙
    assert snake.check_wall_collision() is True


def test_self_collision():
    snake = Snake()
    # 构造自撞：让蛇变长后绕圈
    for _ in range(3):
        snake.grow()
        snake.move()
    # 此时蛇较长，向下绕回
    snake.change_direction(DIRECTIONS["DOWN"])
    snake.move()
    snake.change_direction(DIRECTIONS["LEFT"])
    snake.move()
    snake.change_direction(DIRECTIONS["UP"])
    snake.move()
    assert snake.check_self_collision() is True


def test_grow():
    snake = Snake()
    length_before = len(snake.body)
    snake.grow()
    snake.move()
    assert len(snake.body) == length_before + 1


def test_direction_queue():
    snake = Snake()
    # 快速按多个方向（右->上->左）
    snake.change_direction(DIRECTIONS["UP"])
    snake.change_direction(DIRECTIONS["LEFT"])
    assert len(snake.direction_queue) == 2

    # 执行移动，应该先向上
    snake.move()
    assert snake.direction == DIRECTIONS["UP"]

    # 再执行移动，应该再向左
    snake.move()
    assert snake.direction == DIRECTIONS["LEFT"]


def test_direction_queue_max_length():
    snake = Snake()
    snake.change_direction(DIRECTIONS["UP"])
    snake.change_direction(DIRECTIONS["UP"])  # 重复方向，应被忽略
    snake.change_direction(DIRECTIONS["LEFT"])
    snake.change_direction(DIRECTIONS["DOWN"])
    # 队列最大长度3，所以只有 UP, LEFT, DOWN
    assert len(snake.direction_queue) == 3


def test_get_body_positions():
    snake = Snake()
    positions = snake.get_body_positions()
    assert len(positions) == INITIAL_SNAKE_LENGTH
    assert positions[0] == snake.get_head_pos()
