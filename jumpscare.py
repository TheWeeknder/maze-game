# jumpscare.py
import pygame, random, os

class Jumpscare:
    def __init__(self, screen_size, duration_ms=2500):
        self.screen_size = screen_size
        # how long the jumpscare lasts before the "time's up" screen appears
        self.duration = duration_ms
        self.start_ms = None
        self.image = None
        self.raw_image = None
        self.sound = None
        self.font = pygame.font.SysFont("impact", 50)

        # if you add img/jumpscare.png, it will be used instead of the drawn face
        if os.path.exists('img/loser.jpg'):
            # keep the original so we can rescale it later without losing quality
            self.raw_image = pygame.image.load('img/loser.jpg')
        self.resize(screen_size)

        # if you add sounds/scream.wav (or .ogg), it plays when the jumpscare starts
        for path in ('sounds/scream.wav', 'sounds/scream.ogg'):
            if os.path.exists(path):
                try:
                    self.sound = pygame.mixer.Sound(path)
                except pygame.error:
                    # no audio device available, so just skip the sound
                    self.sound = None
                break

    # adapts the jumpscare to a new screen size
    def resize(self, screen_size):
        self.screen_size = screen_size
        # stretch the image to fill the new size
        if self.raw_image:
            self.image = pygame.transform.scale(self.raw_image, screen_size)

    # starts the jumpscare
    def trigger(self):
        self.start_ms = pygame.time.get_ticks()
        if self.sound:
            self.sound.play()

    # draws the jumpscare on top of everything else
    def draw(self, screen):
        w, h = self.screen_size
        # how long since the jumpscare started
        elapsed = pygame.time.get_ticks() - self.start_ms

        # after the jumpscare is over, show a plain "time's up" screen
        if elapsed > self.duration:
            self.draw_menu(screen)
            return

        # random shake offset so the picture jitters
        ox, oy = random.randint(0, 0), random.randint(0, 0)

        # use your own image if one was loaded
        if self.image:
            screen.fill((0, 0, 0))
            screen.blit(self.image, (ox, oy))
            return

        # otherwise draw a simple face with shapes
        # flash the background between dark red and black
        flash = (elapsed // 80) % 2 == 0
        screen.fill((120, 0, 0) if flash else (0, 0, 0))

        # two big white eyes
        pygame.draw.ellipse(screen, (255, 255, 255), (w * 0.15 + ox, h * 0.18 + oy, w * 0.28, h * 0.25))
        pygame.draw.ellipse(screen, (255, 255, 255), (w * 0.57 + ox, h * 0.18 + oy, w * 0.28, h * 0.25))
        # small red pupils
        pygame.draw.circle(screen, (255, 0, 0), (int(w * 0.29 + ox), int(h * 0.30 + oy)), int(h * 0.04))
        pygame.draw.circle(screen, (255, 0, 0), (int(w * 0.71 + ox), int(h * 0.30 + oy)), int(h * 0.04))

        # a wide jagged mouth: a zigzag along the top, then a zigzag back along the bottom
        steps = 8
        step_w = (w * 0.7) / steps
        top = [(w * 0.15 + i * step_w + ox, h * 0.58 + (h * 0.08 if i % 2 else 0) + oy)
               for i in range(steps + 1)]
        bottom = [(w * 0.85 - i * step_w + ox, h * 0.92 - (h * 0.08 if i % 2 else 0) + oy)
                  for i in range(steps + 1)]
        pygame.draw.polygon(screen, (255, 255, 255), top + bottom)

    # clears the jumpscare so it can play again after a restart
    def reset(self):
        self.start_ms = None
        # stop the scream if it is still playing
        if self.sound:
            self.sound.stop()

    # True once the jumpscare is over and the buttons are on screen
    def is_menu_showing(self):
        return self.start_ms is not None and pygame.time.get_ticks() - self.start_ms > self.duration

    # returns the two button rectangles, centered on the screen
    def get_buttons(self):
        w, h = self.screen_size
        button_w, button_h = 320, 80
        continue_rect = pygame.Rect(0, 0, button_w, button_h)
        exit_rect = pygame.Rect(0, 0, button_w, button_h)
        # stack them in the middle with a gap between
        continue_rect.center = (w // 2, h // 2 - 60)
        exit_rect.center = (w // 2, h // 2 + 60)
        return continue_rect, exit_rect

    # draws the "Continue?" and "Exit" buttons
    def draw_menu(self, screen):
        screen.fill((0, 0, 0))
        continue_rect, exit_rect = self.get_buttons()
        mouse_pos = pygame.mouse.get_pos()

        for rect, label in ((continue_rect, "Try Again?"), (exit_rect, "Exit")):
            # lighten the button when the mouse is over it
            color = (170, 0, 0) if rect.collidepoint(mouse_pos) else (110, 0, 0)
            pygame.draw.rect(screen, color, rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=12)
            text = self.font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))

    # checks which button was clicked: returns 'continue', 'exit', or None
    def handle_click(self, pos):
        # ignore clicks while the jumpscare is still playing
        if not self.is_menu_showing():
            return None
        continue_rect, exit_rect = self.get_buttons()
        if continue_rect.collidepoint(pos):
            return 'continue'
        if exit_rect.collidepoint(pos):
            return 'exit'
        return None