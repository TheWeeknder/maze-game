# player.py
import pygame

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

        # remember where the player started so we can send them back here
        self.start_x = int(x)
        self.start_y = int(y)

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

    # builds a rectangle for every wall that still exists in a cell
    def get_wall_rects(self, cell, tile, thickness):
        rects = []
        # top-left corner of the cell in pixels
        x, y = cell.x * tile, cell.y * tile
        # walls are drawn centered on the cell edge, so go half the thickness each way
        half = thickness // 2
        if cell.walls['top']:
            rects.append(pygame.Rect(x - half, y - half, tile + thickness, thickness))
        if cell.walls['bottom']:
            rects.append(pygame.Rect(x - half, y + tile - half, tile + thickness, thickness))
        if cell.walls['left']:
            rects.append(pygame.Rect(x - half, y - half, thickness, tile + thickness))
        if cell.walls['right']:
            rects.append(pygame.Rect(x + tile - half, y - half, thickness, tile + thickness))
        return rects

    # returns True if the player's square overlaps any wall
    def touching_wall(self, tile, grid_cells, thickness):
        # which cell is the center of the player in?
        player_cell_x = self.rect.centerx // tile
        player_cell_y = self.rect.centery // tile
        for cell in grid_cells:
            # only check the player's cell and the cells right next to it
            if abs(cell.x - player_cell_x) <= 1 and abs(cell.y - player_cell_y) <= 1:
                for wall in self.get_wall_rects(cell, tile, thickness):
                    # does the player's square overlap this wall?
                    if self.rect.colliderect(wall):
                        return True
        return False

    # puts the player back at the starting position
    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        # stop any movement that was in progress
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False