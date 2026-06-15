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
        options = ["Single Player", "Two Players", "Quit"]

        while True:
            self.screen.fill(settings.BLACK)

            title = self.title_font.render("Tank Battle", True, settings.GREEN)
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
        options = ["Easy", "Normal", "Hard", "Back"]

        while True:
            self.screen.fill(settings.BLACK)

            title = self.menu_font.render("Select Difficulty", True, settings.GREEN)
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
    pygame.display.set_caption("Tank Battle")

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
