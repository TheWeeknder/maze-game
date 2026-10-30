# clock.py
import pygame, time, math

pygame.font.init()

class Clock:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.font = pygame.font.SysFont("monospace", 35)
        self.message_color = pygame.Color("yellow")

    # Start the timer
    def start_timer(self):
        self.start_time = time.time()

    # Update the timer
    def update_timer(self):
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time

    # Display the timer
    def display_timer(self):
        secs = int(self.elapsed_time % 60)
        mins = int(self.elapsed_time / 60)
        my_time = self.font.render(f"{mins:02}:{secs:02}", True, self.message_color)
        return my_time

    # Stop the timer
    def stop_timer(self):
        self.start_time = None

    # Display the time remaining, counting down from the limit
    def display_countdown(self, limit):
        # time left, never below zero
        remaining = max(0, limit - self.elapsed_time)
        # round up so it shows 30 at the start and 00 only when time is truly up
        secs = math.ceil(remaining)
        # turn red for the last 10 seconds
        color = pygame.Color("red") if secs <= 10 else self.message_color
        return self.font.render(f"{secs // 60:02}:{secs % 60:02}", True, color)