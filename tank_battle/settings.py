# 屏幕
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 580
GRID_SIZE = 60
COLS = 13
ROWS = 9
GAME_AREA_HEIGHT = GRID_SIZE * ROWS  # 540

# 颜色 (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 90, 43)
BLUE = (50, 100, 200)
GREEN = (50, 180, 50)
RED = (200, 50, 50)
YELLOW = (220, 200, 50)
ORANGE = (220, 150, 50)

# 地图元素
EMPTY = 0
BRICK = 1
STEEL = 2
WATER = 3

# 方向
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
DIRECTION_VECTORS = {
    UP: (0, -1),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    RIGHT: (1, 0),
}

# 坦克
TANK_SIZE = 50  # 像素，略小于网格以便通过
PLAYER_SPEED = 4  # 像素/帧
PLAYER_LIVES = 3
ENEMY_LIVES = 1
SHOOT_COOLDOWN = 20  # 帧

# 子弹
BULLET_SPEED = 6
BULLET_SIZE = 6

# AI 难度
DIFFICULTY = {
    "easy": {
        "enemy_count": 3,
        "enemy_speed": 2,
        "track_chance": 0.2,
        "shoot_chance": 0.01,
        "direction_change_interval": 60,
    },
    "normal": {
        "enemy_count": 5,
        "enemy_speed": 3,
        "track_chance": 0.4,
        "shoot_chance": 0.015,
        "direction_change_interval": 45,
    },
    "hard": {
        "enemy_count": 7,
        "enemy_speed": 4,
        "track_chance": 0.6,
        "shoot_chance": 0.02,
        "direction_change_interval": 30,
    },
}
