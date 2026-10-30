# player.py
import pygame

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    # get current cell position of the player
    def get_current_cell(self, x, y, grid_cells):
        for cell in grid_cells:
            if cell.x == x and cell.y == y:
                return cell

    # stops player to pass through walls
    def check_move(self, tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile
        if self.left_pressed:
            if current_cell.walls['left']:
                if self.x <= current_cell_abs_x + thickness:
                    self.left_pressed = False
        if self.right_pressed:
            if current_cell.walls['right']:
                if self.x >= current_cell_abs_x + tile - (self.player_size + thickness):
                    self.right_pressed = False
        if self.up_pressed:
            if current_cell.walls['top']:
                if self.y <= current_cell_abs_y + thickness:
                    self.up_pressed = False
        if self.down_pressed:
            if current_cell.walls['bottom']:
                if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                    self.down_pressed = False


    # drawing player to the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  

        

    # updates player position while moving
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)

    # sets the movement flags based on where the mouse is
    def follow_mouse(self, mouse_pos):
        # start each frame with no movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # find the center of the player square
        center_x = self.x + self.player_size / 2
        center_y = self.y + self.player_size / 2

        # how far the mouse is from the player on each axis
        dx = mouse_pos[0] - center_x
        dy = mouse_pos[1] - center_y

        # only move if the mouse is farther away than one step (self.speed)
        # this "dead zone" stops the player from jittering back and forth
        if dx < -self.speed:
            self.left_pressed = True
        elif dx > self.speed:
            self.right_pressed = True

        if dy < -self.speed:
            self.up_pressed = True
        elif dy > self.speed:
            self.down_pressed = True