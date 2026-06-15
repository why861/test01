import random
from . import settings


def generate_map(player_spawns):
    """生成随机地图。player_spawns 为 [(col, row), ...] 列表。
       返回 2D list: grid[row][col]。
    """
    _validate_spawns(player_spawns)
    protected = set(player_spawns)

    grid = [[settings.EMPTY for _ in range(settings.COLS)] for _ in range(settings.ROWS)]

    total = settings.COLS * settings.ROWS
    target_empty = int(total * 0.6)

    water_count = int(total * 0.1)
    _place_random(grid, settings.WATER, water_count, protected)

    steel_count = int(total * 0.1)
    _place_random(grid, settings.STEEL, steel_count, protected)

    current_empty = sum(1 for row in grid for cell in row if cell == settings.EMPTY)
    brick_count = current_empty - target_empty
    _place_random(grid, settings.BRICK, max(0, brick_count), protected)

    return grid


def _validate_spawns(spawns):
    for col, row in spawns:
        if not (0 <= col < settings.COLS and 0 <= row < settings.ROWS):
            raise ValueError(f"player spawn ({col},{row}) out of bounds")


def _place_random(grid, tile_type, count, protected):
    """在非保护区域随机放置 count 个 tile_type 格子。
       返回实际放置数量。"""
    placed = 0
    attempts = 0
    max_attempts = max(count * 20, 500)
    while placed < count and attempts < max_attempts:
        attempts += 1
        col = random.randint(0, settings.COLS - 1)
        row = random.randint(0, settings.ROWS - 1)
        if grid[row][col] == settings.EMPTY and (col, row) not in protected:
            grid[row][col] = tile_type
            placed += 1
    return placed


def is_passable(grid, col, row):
    """坦克能否通过该格子。"""
    if not (0 <= col < settings.COLS and 0 <= row < settings.ROWS):
        return False
    return grid[row][col] in (settings.EMPTY,)


def is_destroyable(grid, col, row):
    """该格子是否可被子弹摧毁。"""
    if not (0 <= col < settings.COLS and 0 <= row < settings.ROWS):
        return False
    return grid[row][col] == settings.BRICK


def bullet_can_pass(grid, col, row):
    """子弹能否通过该格子（水可以通过，铁墙/砖墙不能）。"""
    if not (0 <= col < settings.COLS and 0 <= row < settings.ROWS):
        return False
    return grid[row][col] in (settings.EMPTY, settings.WATER)


def destroy_tile(grid, col, row):
    """摧毁指定格子的砖墙。"""
    if is_destroyable(grid, col, row):
        grid[row][col] = settings.EMPTY
