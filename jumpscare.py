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
        if os.path.exists('img/jumpscare.png'):
            # keep the original so we can rescale it later without losing quality
            self.raw_image = pygame.image.load('img/jumpscare.png')
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
            screen.fill((0, 0, 0))
            text = self.font.render("TIME'S UP!", True, (200, 0, 0))
            screen.blit(text, text.get_rect(center=(w // 2, h // 2)))
            return

        # random shake offset so the picture jitters
        ox, oy = random.randint(-12, 12), random.randint(-12, 12)

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