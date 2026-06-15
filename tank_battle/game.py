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
        self.font = pygame.font.Font(None, 24)
        self.running = True
        self.outcome = None

    def run(self, mode, difficulty=None):
        """运行一局游戏。mode: 'single' 或 'double'。"""
        self.mode = mode
        self.difficulty = difficulty
        self._init_game()
        self._game_loop()

    def _init_game(self):
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

        # 创建玩家
        key_p1 = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP_PLUS)
        self.player1 = PlayerTank(0, 4, settings.RIGHT, settings.GREEN,
                                  settings.PLAYER_SPEED, settings.PLAYER_LIVES, key_p1)
        self.players = [self.player1]

        if self.mode == "double":
            key_p2 = (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_f)
            self.player2 = PlayerTank(12, 4, settings.LEFT, settings.ORANGE,
                                      settings.PLAYER_SPEED, settings.PLAYER_LIVES, key_p2)
            self.players.append(self.player2)

        # 创建 AI
        if self.mode == "single":
            ai = EnemyAI(self.difficulty)
        else:
            ai = EnemyAI("normal")
        self.ai = ai

        # 创建敌人
        enemy_colors = [settings.RED, (180, 60, 60), (220, 80, 80),
                        (255, 100, 100), (160, 40, 40), (200, 70, 70), (140, 30, 30)]
        self.enemies = []
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
            self.clock.tick(60)
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

        # 移除死亡单位
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

        # 地图
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

        # 坦克
        for tank in self.all_tanks:
            tank.draw(self.screen)

        # 子弹
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # 信息栏
        info_y = settings.GAME_AREA_HEIGHT
        lives_text = self.font.render(
            f"P1 Lives: {self.player1.hp if self.player1.alive else 0}",
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
        """显示胜利/失败信息，等待按键返回。"""
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(settings.BLACK)
        self.screen.blit(overlay, (0, 0))

        if self.outcome == "win":
            text = "Victory! Press any key to return"
            color = settings.GREEN
        else:
            text = "Defeat! Press any key to return"
            color = settings.RED

        result_font = pygame.font.Font(None, 48)
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
