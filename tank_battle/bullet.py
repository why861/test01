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
