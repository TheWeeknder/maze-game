# main.py
import pygame, sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock

from jumpscare import Jumpscare

pygame.init()
pygame.font.init()

class Main():
    def __init__(self, window, game_size):
        # the real display (your whole monitor)
        self.window = window
        # the maze is drawn on this smaller surface, then scaled up onto the window
        self.screen = pygame.Surface(game_size)
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.failed = False
        # seconds the player has to finish the maze
        self.time_limit = 60
        self.FPS = pygame.time.Clock()

    # works out how much to scale the game so it fits the monitor
    def get_scale_and_offset(self):
        win_w, win_h = self.window.get_size()
        game_w, game_h = self.screen.get_size()
        # scale as much as possible without stretching the picture
        scale = min(win_w / game_w, win_h / game_h)
        new_size = (int(game_w * scale), int(game_h * scale))
        # offset centers the game, leaving black bars on the sides if needed
        offset = ((win_w - new_size[0]) // 2, (win_h - new_size[1]) // 2)
        return scale, offset, new_size

    # converts the mouse position on the monitor into game coordinates
    def get_game_mouse(self):
        scale, offset, _ = self.get_scale_and_offset()
        mx, my = pygame.mouse.get_pos()
        return ((mx - offset[0]) / scale, (my - offset[1]) / scale)

    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Your Mouse', True, self.message_color)
        instructions3 = self.font.render('to Move', True, self.message_color)
        self.screen.blit(instructions1,(655,300))
        self.screen.blit(instructions2,(610,331))
        self.screen.blit(instructions3,(630,362))

    # draws all configs; maze, player, instructions, and time
    def _draw(self, maze, tile, player, game, clock, jumpscare):
        # draw maze
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        # add a goal point to reach
        game.add_goal_point(self.screen)
        # draw every player movement
        player.draw(self.screen)
        player.update()
        # instructions, clock, winning message
        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(),(610,120))
        elif self.failed:
            # freeze the timer once time has run out
            clock.stop_timer()
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (625,200))

        # draw the jumpscare on top of everything
        if self.failed:
            # the jumpscare draws straight onto the full monitor
            jumpscare.draw(self.window)
        else:
            # scale the game up and center it on the monitor
            scale, offset, new_size = self.get_scale_and_offset()
            self.window.fill((0, 0, 0))
            scaled = pygame.transform.smoothscale(self.screen, new_size)
            self.window.blit(scaled, offset)
        pygame.display.flip()

    # main game loop
    def main(self, frame_size, tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile // 3, tile // 3)
        clock = Clock()

        jumpscare = Jumpscare(self.window.get_size())

        maze.generate_maze()
        clock.start_timer()
        while self.running:
            self.screen.fill("gray")
            self.screen.fill( pygame.Color("darkslategray"), (603, 0, 752, 752))
            for event in pygame.event.get():
                # F11 switches between fullscreen and windowed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                # Esc closes the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # # if keys were pressed still
            # if event.type == pygame.KEYDOWN:
            #     if not self.game_over:
            #         if event.key == pygame.K_LEFT:
            #             player.left_pressed = True
            #         if event.key == pygame.K_RIGHT:
            #             player.right_pressed = True
            #         if event.key == pygame.K_UP:
            #             player.up_pressed = True
            #         if event.key == pygame.K_DOWN:
            #             player.down_pressed = True
            #         player.check_move(tile, maze.grid_cells, maze.thickness)
            # # if pressed key released
            # if event.type == pygame.KEYUP:
            #     if not self.game_over:
            #         if event.key == pygame.K_LEFT:
            #             player.left_pressed = False
            #         if event.key == pygame.K_RIGHT:
            #             player.right_pressed = False
            #         if event.key == pygame.K_UP:
            #             player.up_pressed = False
            #         if event.key == pygame.K_DOWN:
            #             player.down_pressed = False
            #         player.check_move(tile, maze.grid_cells, maze.thickness)
            # move the player toward the mouse every frame

            # only let the player move while the game is still going
            if not self.game_over and not self.failed:
                # set the movement flags from the mouse position
                player.follow_mouse(self.get_game_mouse())

            # check if the player has reached the gate
            if not self.failed and game.is_game_over(player):
                self.game_over = True
                player.left_pressed = False
                player.right_pressed = False
                player.up_pressed = False
                player.down_pressed = False

            # if the player touches a wall, send them back to the start
            if not self.game_over and not self.failed and player.touching_wall(tile, maze.grid_cells, maze.thickness):
                player.reset_position()

            # if time runs out before the player wins, trigger the jumpscare
            if not self.game_over and not self.failed and clock.elapsed_time >= self.time_limit:
                self.failed = True
                # stop the player from moving
                player.left_pressed = False
                player.right_pressed = False
                player.up_pressed = False
                player.down_pressed = False
                # start the jumpscare
                jumpscare.trigger()

            self._draw(maze, tile, player, game, clock, jumpscare)
            self.FPS.tick(60)
# main.py

if __name__ == "__main__":
    window_size = (602, 602)
    # the maze area plus the sidebar on the right
    game_size = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    # (0, 0) means "use my monitor's resolution"
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Maze")

    game = Main(window, game_size)
    game.main(window_size, tile_size)