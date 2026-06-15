import random
from . import settings


class EnemyAI:
    """敌人 AI 控制器。"""
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

        if player_tanks and random.random() < self.track_chance:
            target = random.choice(player_tanks)
            if target.alive:
                dx = target.x - enemy.x
                dy = target.y - enemy.y
                if abs(dx) > abs(dy):
                    return settings.RIGHT if dx > 0 else settings.LEFT
                else:
                    return settings.DOWN if dy > 0 else settings.UP

        if self.frame_counter >= self.direction_change_interval:
            self.frame_counter = 0
            enemy.direction = random.choice([settings.UP, settings.DOWN, settings.LEFT, settings.RIGHT])

        return enemy.direction

    def decide_shoot(self, enemy):
        """决策是否开火。"""
        if random.random() < self.shoot_chance:
            return enemy.shoot()
        return None
