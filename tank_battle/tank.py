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

        # 车身
        body_rect = pygame.Rect(int(self.x + 4), int(self.y + 4),
                                settings.TANK_SIZE - 8, settings.TANK_SIZE - 8)
        pygame.draw.rect(screen, self.color, body_rect)
        pygame.draw.rect(screen, settings.BLACK, body_rect, 2)

        # 炮管
        barrel_len = settings.TANK_SIZE // 2 + 6
        barrel_width = 8
        if self.direction == settings.UP:
            end_x, end_y = cx, cy - barrel_len
        elif self.direction == settings.DOWN:
            end_x, end_y = cx, cy + barrel_len
        elif self.direction == settings.LEFT:
            end_x, end_y = cx - barrel_len, cy
        elif self.direction == settings.RIGHT:
            end_x, end_y = cx + barrel_len, cy
        else:
            end_x, end_y = cx, cy

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

        self.move_forward(grid, tanks)
        bullet = None
        if keys[self.key_shoot]:
            bullet = self.shoot()
        return bullet
