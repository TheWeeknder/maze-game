# game.py
import pygame

pygame.font.init()

class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.SysFont("impact", 35)
        self.message_color = pygame.Color("darkorange")
        self.goal_cell = goal_cell
        self.tile = tile

    # add goal point for player to reach
    def add_goal_point(self, screen):
        # adding gate for the goal point
        img_path = 'img/gate.png'
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (self.tile, self.tile))
        screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    # winning message
    def message(self):
        msg = self.font.render('You Win!!', True, self.message_color)
        return msg

    # checks if the player has reached the goal point
    def is_game_over(self, player):
        # build a rectangle that covers the whole goal cell
        goal_rect = pygame.Rect(
            self.goal_cell.x * self.tile,   # left edge of the goal cell
            self.goal_cell.y * self.tile,   # top edge of the goal cell
            self.tile,                      # width of the cell
            self.tile                       # height of the cell
        )
        # the player wins once the center of their square is inside that cell
        return goal_rect.collidepoint(player.rect.center)