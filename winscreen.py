# winscreen.py
import pygame, os

class WinScreen:
    def __init__(self, screen_size, delay_ms=0):
        self.screen_size = screen_size
        # how long the maze stays visible before the image appears
        self.delay = delay_ms
        self.start_ms = None
        self.font = pygame.font.SysFont("impact", 40)
        self.big_font = pygame.font.SysFont("impact", 90)
        self.raw_image = None
        self.image = None

        # your congratulations image goes in img/congrats.png
        if os.path.exists('img/you-win-better.jpg'):
            self.raw_image = pygame.image.load('img/you-win-better.jpg')
        self.resize(screen_size)

    # stretches the image to fill the screen
    def resize(self, screen_size):
        self.screen_size = screen_size
        if self.raw_image:
            self.image = pygame.transform.scale(self.raw_image, screen_size)

    # starts the win screen timer
    def trigger(self):
        self.start_ms = pygame.time.get_ticks()

    # clears the win screen so it can show again after a restart
    def reset(self):
        self.start_ms = None

    # True once the delay has passed and the image is on screen
    def is_showing(self):
        return self.start_ms is not None and pygame.time.get_ticks() - self.start_ms >= self.delay

    # returns the two button rectangles, side by side near the bottom
    def get_buttons(self):
        w, h = self.screen_size
        play_rect = pygame.Rect(0, 0, 320, 80)
        exit_rect = pygame.Rect(0, 0, 320, 80)
        play_rect.center = (w // 2 - 180, int(h * 0.50))
        exit_rect.center = (w // 2 + 180, int(h * 0.50))
        return play_rect, exit_rect

    # draws the image (or plain text if there is no image) and the buttons
    def draw(self, screen):
        w, h = self.screen_size
        if self.image:
            screen.blit(self.image, (0, 0))
        else:
            # fallback if img/congrats.png is missing
            screen.fill((0, 60, 0))
            text = self.big_font.render("CONGRATULATIONS!", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(w // 2, h // 2)))

        play_rect, exit_rect = self.get_buttons()
        mouse_pos = pygame.mouse.get_pos()
        for rect, label in ((play_rect, "Play Again"), (exit_rect, "Exit")):
            # lighten the button when the mouse is over it
            color = (0, 150, 60) if rect.collidepoint(mouse_pos) else (0, 100, 40)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=12)
            text = self.font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

    # checks which button was clicked: returns 'continue', 'exit', or None
    def handle_click(self, pos):
        # ignore clicks until the image is showing
        if not self.is_showing():
            return None
        play_rect, exit_rect = self.get_buttons()
        if play_rect.collidepoint(pos):
            return 'continue'
        if exit_rect.collidepoint(pos):
            return 'exit'
        return None