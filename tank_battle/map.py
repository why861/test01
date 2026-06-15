import random
from . import settings


def generate_map(player_spawns):
    """生成随机地图。player_spawns 为 [(col, row), ...] 列表。
       返回 2D list: grid[row][col]。
    """
    grid = [[settings.EMPTY for _ in range(settings.COLS)] for _ in range(settings.ROWS)]

    # 统计总格数，目标 60% 空地
    total = settings.COLS * settings.ROWS
    target_empty = int(total * 0.6)

    # 放置水域 (约10%的格子)
    water_count = int(total * 0.1)
    _place_random(grid, settings.WATER, water_count, player_spawns)

    # 放置铁墙 (约10%的格子)
    steel_count = int(total * 0.1)
    _place_random(grid, settings.STEEL, steel_count, player_spawns)

    # 放满剩余非保护区域为砖墙 (可达20%左右)
    for row in range(settings.ROWS):
        for col in range(settings.COLS):
            if grid[row][col] == settings.EMPTY and (col, row) not in player_spawns:
                if random.random() < 0.4:
                    grid[row][col] = settings.BRICK

    return grid


def _place_random(grid, tile_type, count, protected):
    """在非保护区域随机放置 count 个 tile_type 格子。"""
    placed = 0
    attempts = 0
    while placed < count and attempts < 1000:
        attempts += 1
        col = random.randint(0, settings.COLS - 1)
        row = random.randint(0, settings.ROWS - 1)
        if grid[row][col] == settings.EMPTY and (col, row) not in protected:
            grid[row][col] = tile_type
            placed += 1


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
