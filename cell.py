# cell.py
import pygame
from random import choice

class Cell:
    def __init__(self, x, y, thickness):
        self.x, self.y = x, y
        self.thickness = thickness
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

# When an instance of the Cell class is created, the __init__() method is called. This special method serves as a constructor and takes three parameters: x, y, and thickness. These parameters define the position and thickness of the wall per cell within the maze. Within the constructor, the walls attribute is initialized as a dictionary with keys representing the directions (top, right, bottom, and left) and values set to True. This indicates that all walls surrounding the cell are initially present. The visited attribute is set to False, allowing us to keep track of whether the cell has been visited during maze generation or traversal.