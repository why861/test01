# 坦克大战 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 Python + Pygame 构建坦克大战游戏，支持单人/双人模式，随机地图生成。

**Architecture:** 7 个模块分层构建。settings 提供全局常量，map/tank/bullet/ai 为游戏实体层，game 为主循环控制器，main 为菜单入口。数据自底向上：settings → map/entities → game → main。

**Tech Stack:** Python 3, Pygame

**画面布局:** 屏幕 780×580，上 540px 为 13×9 网格游戏区（每格 60px），下 40px 为信息栏。坦克、子弹在网格内以像素精度移动。

---

### Task 1: settings.py — 全局常量配置

**Files:**
- Create: `tank_battle/settings.py`

- [ ] **Step 1: 创建 settings.py**

```python
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
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/settings.py`
Expected: 无输出（编译成功）

- [ ] **Step 3: 提交**

```bash
git add tank_battle/settings.py
git commit -m "feat: add settings module with game constants"
```

---

### Task 2: map.py — 随机地图生成

**Files:**
- Create: `tank_battle/map.py`

- [ ] **Step 1: 创建 map.py**

```python
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
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/map.py`
Expected: 无输出

- [ ] **Step 3: 提交**

```bash
git add tank_battle/map.py
git commit -m "feat: add random map generation module"
```

---

### Task 3: bullet.py — 子弹类

**Files:**
- Create: `tank_battle/bullet.py`

- [ ] **Step 1: 创建 bullet.py**

```python
import pygame
from . import settings
from .map import is_destroyable, bullet_can_pass, destroy_tile


class Bullet:
    def __init__(self, x, y, direction, owner_type):
        """owner_type: 'player' 或 'enemy'"""
        self.x = float(x)
        self.y = float(y)
        self.direction = direction
        self.owner_type = owner_type
        self.speed = settings.BULLET_SPEED
        self.alive = True
        self.rect = pygame.Rect(x, y, settings.BULLET_SIZE, settings.BULLET_SIZE)

    def update(self, grid, tanks):
        """移动子弹并检测碰撞。返回碰撞信息或 None。"""
        if not self.alive:
            return None

        dx, dy = settings.DIRECTION_VECTORS[self.direction]
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 边界检测
        if (self.x < 0 or self.x > settings.SCREEN_WIDTH - settings.BULLET_SIZE or
                self.y < 0 or self.y > settings.GAME_AREA_HEIGHT - settings.BULLET_SIZE):
            self.alive = False
            return None

        # 网格碰撞检测
        col = int(self.x + settings.BULLET_SIZE // 2) // settings.GRID_SIZE
        row = int(self.y + settings.BULLET_SIZE // 2) // settings.GRID_SIZE

        if is_destroyable(grid, col, row):
            destroy_tile(grid, col, row)
            self.alive = False
            return None
        elif not bullet_can_pass(grid, col, row):
            self.alive = False
            return None

        # 坦克碰撞检测
        for tank in tanks:
            if not tank.alive:
                continue
            tank_type = 'player' if tank.is_player else 'enemy'
            if tank_type == self.owner_type:
                continue
            if self.rect.colliderect(tank.rect):
                self.alive = False
                tank.take_damage()
                return tank

        return None

    def draw(self, screen):
        """绘制子弹为小黄色方块。"""
        if self.alive:
            pygame.draw.rect(screen, settings.YELLOW, self.rect)
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/bullet.py`
Expected: 无输出

- [ ] **Step 3: 提交**

```bash
git add tank_battle/bullet.py
git commit -m "feat: add bullet class with collision detection"
```

---

### Task 4: tank.py — 坦克基类与玩家类

**Files:**
- Create: `tank_battle/tank.py`

- [ ] **Step 1: 创建 tank.py**

```python
import math
import pygame
from . import settings
from .map import is_passable
from .bullet import Bullet


class Tank:
    """坦克基类。位置以像素坐标存储。"""
    def __init__(self, col, row, direction, color, speed, hp, is_player):
        self.col = col
        self.row = row
        self.x = float(col * settings.GRID_SIZE + (settings.GRID_SIZE - settings.TANK_SIZE) // 2)
        self.y = float(row * settings.GRID_SIZE + (settings.GRID_SIZE - settings.TANK_SIZE) // 2)
        self.direction = direction
        self.color = color
        self.speed = speed
        self.hp = hp
        self.alive = True
        self.is_player = is_player
        self.shoot_cooldown = 0
        self.rect = pygame.Rect(int(self.x), int(self.y), settings.TANK_SIZE, settings.TANK_SIZE)

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def shoot(self):
        """开火，返回新子弹或 None（冷却中）。"""
        if self.shoot_cooldown > 0:
            return None
        self.shoot_cooldown = settings.SHOOT_COOLDOWN
        bx, by = self._bullet_spawn_pos()
        return Bullet(bx, by, self.direction, 'player' if self.is_player else 'enemy')

    def _bullet_spawn_pos(self):
        """子弹从炮管口发射。"""
        half_tank = settings.TANK_SIZE // 2
        half_bullet = settings.BULLET_SIZE // 2
        cx, cy = self.x + half_tank - half_bullet, self.y + half_tank - half_bullet
        offset = settings.TANK_SIZE // 2 + 1
        if self.direction == settings.UP:
            return cx, self.y - half_bullet - 2
        elif self.direction == settings.DOWN:
            return cx, self.y + settings.TANK_SIZE - half_bullet + 2
        elif self.direction == settings.LEFT:
            return self.x - half_bullet - 2, cy
        elif self.direction == settings.RIGHT:
            return self.x + settings.TANK_SIZE - half_bullet + 2, cy
        return cx, cy

    def can_move_forward(self, grid, tanks):
        """检查向前移动是否会碰撞。"""
        dx, dy = settings.DIRECTION_VECTORS[self.direction]
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        return self._can_place_at(new_x, new_y, grid, tanks)

    def _can_place_at(self, x, y, grid, tanks):
        """检查坦克在指定位置是否合法。"""
        margin = 2
        test_rect = pygame.Rect(int(x) + margin, int(y) + margin,
                                settings.TANK_SIZE - margin * 2, settings.TANK_SIZE - margin * 2)

        # 边界
        if (x < 0 or x > settings.SCREEN_WIDTH - settings.TANK_SIZE or
                y < 0 or y > settings.GAME_AREA_HEIGHT - settings.TANK_SIZE):
            return False

        # 角落对应的网格格
        corners = [
            (int(x) // settings.GRID_SIZE, int(y) // settings.GRID_SIZE),
            (int(x + settings.TANK_SIZE - 1) // settings.GRID_SIZE, int(y) // settings.GRID_SIZE),
            (int(x) // settings.GRID_SIZE, int(y + settings.TANK_SIZE - 1) // settings.GRID_SIZE),
            (int(x + settings.TANK_SIZE - 1) // settings.GRID_SIZE, int(y + settings.TANK_SIZE - 1) // settings.GRID_SIZE),
        ]
        for col, row in corners:
            if not is_passable(grid, col, row):
                return False

        # 其他坦克碰撞
        for other in tanks:
            if other is self or not other.alive:
                continue
            if test_rect.colliderect(other.rect):
                return False

        return True

    def move_forward(self, grid, tanks):
        """尝试向前移动，成功返回 True。"""
        dx, dy = settings.DIRECTION_VECTORS[self.direction]
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if self._can_place_at(new_x, new_y, grid, tanks):
            self.x = new_x
            self.y = new_y
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            return True
        return False

    def update(self):
        """每帧冷却减少。"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        """用几何图形绘制坦克。"""
        if not self.alive:
            return
        cx, cy = self.x + settings.TANK_SIZE // 2, self.y + settings.TANK_SIZE // 2
        half = settings.TANK_SIZE // 2

        # 车身
        body_rect = pygame.Rect(int(self.x + 4), int(self.y + 4),
                                settings.TANK_SIZE - 8, settings.TANK_SIZE - 8)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.rect(screen, settings.BLACK, body_rect, 2)

        # 炮管
        barrel_len = settings.TANK_SIZE // 2 + 6
        barrel_width = 8
        end_x, end_y = cx, cy
        if self.direction == settings.UP:
            start_x, start_y = cx - barrel_width // 2, cy
            end_x, end_y = cx - barrel_width // 2, cy - barrel_len
        elif self.direction == settings.DOWN:
            start_x, start_y = cx - barrel_width // 2, cy
            end_x, end_y = cx - barrel_width // 2, cy + barrel_len
        elif self.direction == settings.LEFT:
            start_x, start_y = cx, cy - barrel_width // 2
            end_x, end_y = cx - barrel_len, cy - barrel_width // 2
        elif self.direction == settings.RIGHT:
            start_x, start_y = cx, cy - barrel_width // 2
            end_x, end_y = cx + barrel_len, cy - barrel_width // 2

        pygame.draw.line(screen, self.color, (cx, cy), (end_x, end_y), barrel_width)


class PlayerTank(Tank):
    """玩家坦克，由键盘控制。"""
    def __init__(self, col, row, direction, color, speed, hp, key_config):
        super().__init__(col, row, direction, color, speed, hp, is_player=True)
        self.key_up, self.key_down, self.key_left, self.key_right, self.key_shoot = key_config

    def handle_input(self, keys, grid, tanks):
        """处理键盘输入。"""
        if not self.alive:
            return None

        # 方向切换
        if keys[self.key_up]:
            self.direction = settings.UP
        elif keys[self.key_down]:
            self.direction = settings.DOWN
        elif keys[self.key_left]:
            self.direction = settings.LEFT
        elif keys[self.key_right]:
            self.direction = settings.RIGHT

        moved = self.move_forward(grid, tanks)
        bullet = None
        if keys[self.key_shoot]:
            bullet = self.shoot()
        return bullet
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/tank.py`
Expected: 无输出

- [ ] **Step 3: 提交**

```bash
git add tank_battle/tank.py
git commit -m "feat: add tank base class and player tank with keyboard control"
```

---

### Task 5: ai.py — 敌人 AI 模块

**Files:**
- Create: `tank_battle/ai.py`

- [ ] **Step 1: 创建 ai.py**

```python
import random
from . import settings


class EnemyAI:
    """敌人 AI 控制器。为每个敌人实例保持独立状态。"""
    def __init__(self, difficulty):
        config = settings.DIFFICULTY[difficulty]
        self.speed = config["enemy_speed"]
        self.track_chance = config["track_chance"]
        self.shoot_chance = config["shoot_chance"]
        self.direction_change_interval = config["direction_change_interval"]
        self.frame_counter = 0

    def decide_direction(self, enemy, player_tanks):
        """决策移动方向。概率追踪玩家，否则随机转向。"""
        self.frame_counter += 1

        # 追踪逻辑
        if player_tanks and random.random() < self.track_chance:
            target = random.choice(player_tanks)
            if target.alive:
                dx = target.x - enemy.x
                dy = target.y - enemy.y
                if abs(dx) > abs(dy):
                    return settings.RIGHT if dx > 0 else settings.LEFT
                else:
                    return settings.DOWN if dy > 0 else settings.UP

        # 随机转向
        if self.frame_counter >= self.direction_change_interval:
            self.frame_counter = 0
            enemy.direction = random.choice([settings.UP, settings.DOWN, settings.LEFT, settings.RIGHT])

        return enemy.direction

    def decide_shoot(self, enemy):
        """决策是否开火。"""
        if random.random() < self.shoot_chance:
            return enemy.shoot()
        return None
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/ai.py`
Expected: 无输出

- [ ] **Step 3: 提交**

```bash
git add tank_battle/ai.py
git commit -m "feat: add enemy AI with difficulty-based behavior"
```

---

### Task 6: game.py — 游戏主控制器

**Files:**
- Create: `tank_battle/game.py`

- [ ] **Step 1: 创建 game.py**

```python
import random
import pygame
from . import settings
from .map import generate_map
from .tank import PlayerTank, Tank
from .ai import EnemyAI


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("simhei", 20)
        self.running = True
        self.outcome = None  # 'win' or 'lose'

    def run(self, mode, difficulty=None):
        """运行一局游戏。mode: 'single' 或 'double'，难度仅 single 模式有效。"""
        self.mode = mode
        self.difficulty = difficulty
        self._init_game()
        self._game_loop()

    def _init_game(self):
        # 生成玩家出生点
        player_spawns = [(0, 4)]
        if self.mode == "double":
            player_spawns.append((12, 4))

        enemy_count = 3
        enemy_speed = 2
        if self.mode == "single" and self.difficulty:
            config = settings.DIFFICULTY[self.difficulty]
            enemy_count = config["enemy_count"]
            enemy_speed = config["enemy_speed"]

        self.grid = generate_map(player_spawns)

        # 创建玩家坦克
        key_p1 = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP_PLUS)
        self.player1 = PlayerTank(0, 4, settings.RIGHT, settings.GREEN,
                                  settings.PLAYER_SPEED, settings.PLAYER_LIVES, key_p1)
        self.players = [self.player1]

        if self.mode == "double":
            key_p2 = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_f)
            self.player2 = PlayerTank(12, 4, settings.LEFT, settings.ORANGE,
                                      settings.PLAYER_SPEED, settings.PLAYER_LIVES, key_p2)
            self.players.append(self.player2)

        # 创建敌人
        if self.mode == "single":
            ai = EnemyAI(self.difficulty)
        else:
            ai = EnemyAI("normal")

        self.ai = ai
        enemy_colors = [settings.RED, (180, 60, 60), (220, 80, 80),
                        (255, 100, 100), (160, 40, 40), (200, 70, 70), (140, 30, 30)]

        self.enemies = []
        # 在右侧区域随机生成敌人出生点
        for i in range(enemy_count):
            col = random.randint(8, 12)
            row = random.randint(0, settings.ROWS - 1)
            while self.grid[row][col] != settings.EMPTY:
                col = random.randint(8, 12)
                row = random.randint(0, settings.ROWS - 1)
            enemy = Tank(col, row, settings.DOWN, enemy_colors[i % len(enemy_colors)],
                         enemy_speed, settings.ENEMY_LIVES, is_player=False)
            self.enemies.append(enemy)

        self.all_tanks = self.players + self.enemies
        self.bullets = []
        self.running = True
        self.outcome = None

    def _game_loop(self):
        while self.running:
            dt = self.clock.tick(60)  # 60 FPS
            self._handle_events()
            self._update()
            self._draw()
        return self.outcome

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.outcome = "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.outcome = "quit"

    def _update(self):
        keys = pygame.key.get_pressed()

        # 玩家输入
        for player in self.players:
            player.update()
            bullet = player.handle_input(keys, self.grid, self.all_tanks)
            if bullet:
                self.bullets.append(bullet)

        # 敌人 AI
        alive_players = [p for p in self.players if p.alive]
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            enemy.update()
            self.ai.decide_direction(enemy, alive_players)
            enemy.move_forward(self.grid, self.all_tanks)
            bullet = self.ai.decide_shoot(enemy)
            if bullet:
                self.bullets.append(bullet)

        # 更新子弹
        for bullet in self.bullets:
            bullet.update(self.grid, self.all_tanks)
        self.bullets = [b for b in self.bullets if b.alive]

        # 移除死亡坦克
        self.all_tanks = [t for t in self.all_tanks if t.alive]
        self.enemies = [e for e in self.enemies if e.alive]
        self.players = [p for p in self.players if p.alive]

        # 判定胜负
        if not any(p.alive for p in self.players):
            self.running = False
            self.outcome = "lose"
        elif not self.enemies:
            self.running = False
            self.outcome = "win"

    def _draw(self):
        self.screen.fill(settings.BLACK)

        # 绘制地图
        for row in range(settings.ROWS):
            for col in range(settings.COLS):
                tile = self.grid[row][col]
                x, y = col * settings.GRID_SIZE, row * settings.GRID_SIZE
                if tile == settings.BRICK:
                    pygame.draw.rect(self.screen, settings.BROWN,
                                     (x, y, settings.GRID_SIZE, settings.GRID_SIZE))
                    pygame.draw.rect(self.screen, settings.BLACK,
                                     (x, y, settings.GRID_SIZE, settings.GRID_SIZE), 1)
                elif tile == settings.STEEL:
                    pygame.draw.rect(self.screen, settings.DARK_GRAY,
                                     (x, y, settings.GRID_SIZE, settings.GRID_SIZE))
                elif tile == settings.WATER:
                    pygame.draw.rect(self.screen, settings.BLUE,
                                     (x, y, settings.GRID_SIZE, settings.GRID_SIZE))

        # 绘制坦克
        for tank in self.all_tanks:
            tank.draw(self.screen)

        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # 信息栏（底部 40px）
        info_y = settings.GAME_AREA_HEIGHT
        lives_text = self.font.render(
            f"P1 Lives: {self.player1.hp if hasattr(self, 'player1') and self.player1.alive else 0}",
            True, settings.WHITE)
        self.screen.blit(lives_text, (10, info_y + 10))

        enemies_text = self.font.render(
            f"Enemies: {len(self.enemies)}", True, settings.WHITE)
        self.screen.blit(enemies_text, (200, info_y + 10))

        if self.mode == "double" and hasattr(self, 'player2'):
            p2_text = self.font.render(
                f"P2 Lives: {self.player2.hp if self.player2.alive else 0}",
                True, settings.WHITE)
            self.screen.blit(p2_text, (350, info_y + 10))

        pygame.display.flip()

    def show_result(self):
        """在屏幕上显示胜利/失败信息，等待按键返回。"""
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(settings.BLACK)
        self.screen.blit(overlay, (0, 0))

        if self.outcome == "win":
            text = "胜利！按任意键返回主菜单"
            color = settings.GREEN
        else:
            text = "失败！按任意键返回主菜单"
            color = settings.RED

        result_font = pygame.font.SysFont("simhei", 36)
        text_surface = result_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                   settings.SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type in (pygame.KEYDOWN, pygame.QUIT):
                    waiting = False
```

- [ ] **Step 2: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/game.py`
Expected: 无输出

- [ ] **Step 3: 提交**

```bash
git add tank_battle/game.py
git commit -m "feat: add main game controller with game loop"
```

---

### Task 7: main.py — 入口与主菜单 & __init__.py

**Files:**
- Create: `tank_battle/main.py`
- Create: `tank_battle/__init__.py`

- [ ] **Step 1: 创建 __init__.py**

```python
# tank_battle package
```

- [ ] **Step 2: 创建 main.py**

```python
import sys
import pygame
from . import settings
from .game import Game


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("simhei", 40)
        self.menu_font = pygame.font.SysFont("simhei", 28)

    def show(self):
        """显示主菜单，返回 (mode, difficulty) 或 ('quit', None)。"""
        clock = pygame.time.Clock()
        selected = 0
        options = ["单人模式", "双人模式", "退出"]

        while True:
            self.screen.fill(settings.BLACK)

            # 标题
            title = self.title_font.render("坦克大战", True, settings.GREEN)
            title_rect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)

            # 菜单选项
            for i, opt in enumerate(options):
                color = settings.YELLOW if i == selected else settings.WHITE
                text = self.menu_font.render(opt, True, color)
                text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, 220 + i * 60))
                self.screen.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ("quit", None)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            diff = self._select_difficulty()
                            if diff:
                                return ("single", diff)
                        elif selected == 1:
                            return ("double", None)
                        elif selected == 2:
                            return ("quit", None)

            clock.tick(30)

    def _select_difficulty(self):
        """难度选择子菜单。"""
        clock = pygame.time.Clock()
        selected = 0
        options = ["简单", "普通", "困难", "返回"]

        while True:
            self.screen.fill(settings.BLACK)

            title = self.menu_font.render("选择难度", True, settings.GREEN)
            title_rect = title.get_rect(center=(settings.SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)

            for i, opt in enumerate(options):
                color = settings.YELLOW if i == selected else settings.WHITE
                text = self.menu_font.render(opt, True, color)
                text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, 220 + i * 60))
                self.screen.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected == 0:
                            return "easy"
                        elif selected == 1:
                            return "normal"
                        elif selected == 2:
                            return "hard"
                        elif selected == 3:
                            return None
                    elif event.key == pygame.K_ESCAPE:
                        return None

            clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("坦克大战")

    menu = Menu(screen)

    while True:
        mode, difficulty = menu.show()
        if mode == "quit":
            break

        game = Game(screen)
        game.run(mode, difficulty)

        if game.outcome == "quit":
            break

        game.show_result()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 验证文件无语法错误**

Run: `python -m py_compile tank_battle/main.py && python -m py_compile tank_battle/__init__.py`
Expected: 无输出

- [ ] **Step 4: 测试游戏能否启动**

Run: `cd tank_battle && python -m tank_battle.main`
Expected: Pygame 窗口打开，显示主菜单

- [ ] **Step 5: 提交**

```bash
git add tank_battle/main.py tank_battle/__init__.py
git commit -m "feat: add main menu and game entry point"
```

---

### Task 8: 整合测试与修复

**Files:**
- Modify: `tank_battle/game.py`
- Modify: `tank_battle/__init__.py`

*此阶段在实际运行时根据遇到的问题进行调整。*

- [ ] **Step 1: 安装 pygame 依赖**

Run: `pip install pygame`
Expected: 安装成功

- [ ] **Step 2: 运行完整游戏测试**

Run: `python -m tank_battle.main`
Expected: 主菜单可操作，单人和双人模式可正常进入和退出

- [ ] **Step 3: 修复问题并提交**

提交修复后的最终版本。
