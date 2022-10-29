import random
import time, sys
import math

from curtsies import FullscreenWindow, Input, FSArray, fsarray, fmtstr
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red
from draw import Ship, Menu, designs

"""Space game to kill Aliens Invasion (like space invaders, but left to write"""

class Background:
    """ Create The stars background"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.design = [[random.choices([" "] * 20 + ["."]) for _ in range(self.width)] for _ in range(self.height)]
        self.x = 0
        self.y = 0
        
    def move_grid(self):
        """Move the background right to left"""
        ## remove first colum and add random colum at the end
        self.design = [row[1:] + [random.choices([" "] * 20 + ["."])] for row in self.design]
            
        
class Scene:
    """Scene class to manage the game"""
    def __init__(self, window):
        self.window = window
        self.grid = FSArray(window.height, window.width)
        self.keys = [
            "<ESC>",
            "<UP>",
            "<DOWN>",
            "<LEFT>",
            "<RIGHT>",
            "<SPACE>",
            "<Ctrl-j>",
        ]
        # create initial conditions
        menu_spanw = window.width // 2, window.height // 2
        self.menu = Menu(menu_spanw)
        self.in_menu = True
        self.render(self.menu)
        self.ship = Ship(lives=3, gun=0, spawn=[10, 10], design=designs["spaceship"])
        self.background = Background(window.width, window.height)
        

    def update_scene(self, msg, cnt=None):
        """Update the scene"""
        if msg == "<ESC>" and not self.in_menu:
            self.in_menu = True
            msg = "<UP>"

        if msg in self.keys and self.in_menu:
            self.menu_options(msg)

        elif msg in self.keys and not self.in_menu:
            
            self.move_ship(msg)
        

    def set_menu(self, in_menu):
        self.in_menu = in_menu

    def menu_options(self, msg):
        """Manage the menu options"""

        # move up and down
        if msg == "<UP>" and self.menu.option > 0:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option - 1)

        elif msg == "<DOWN>" and self.menu.option <= 1:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option + 1)

        # leave the menu
        elif msg == "<ESC>" and self.menu.option < 3:
            self.menu.set_option(0)
            self.render(self.menu, True)
            self.in_menu = False  # stop to show menu

        # enter the submenus
        elif (msg == "<SPACE>" or msg == "<Ctrl-j>") and self.menu.option == 0:
            self.render(self.menu, True)
            self.in_menu = False  # need to restart the game

        elif (msg == "<SPACE>" or msg == "<Ctrl-j>") and self.menu.option == 1:
            self.render(self.menu, True)
            self.menu.set_option(11)

        elif (msg == "<SPACE>" or msg == "<Ctrl-j>") and self.menu.option == 2:
            self.render(self.menu, True)
            self.menu.set_option(12)

        # exit the submenus
        elif msg == "<ESC>" and self.menu.option > 3:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option - 10)

        # render menu if meny is active
        if self.in_menu:
            self.render(self.menu)

    # world.grid[0:4, 0:25] = fsarray(
    #                     [
    #                         world.winner_msg(tick),
    #                         "r to restart",
    #                         "q to quit",
    #                         "b to make player 2 a bot",
    #                     ]


    def render(self, obj, delete=False):
        """Function that draw objects in the screen"""
        # if delete:
        #     self.grid[obj.y: len(obj.design) + obj.y, obj.x: len(obj.design) + obj.x] = fsarray(
        #         [[" "] * len(obj.design[0]) for _ in range(len(obj.design))]
        # else:    
        #     self.grid[obj.y: len(obj.design) + obj.y, obj.x: len(obj.design) + obj.x] = fsarray(obj.design)
        
        # for i, part in enumerate(obj.design):
        #     for j, char in enumerate(part):
        #         if delete:
        #             self.grid[obj.y + i, obj.x + j] = " "
        #         else:
        #             self.grid[obj.y + i, obj.x + j] = char

    def move_ship(self, msg):
        """Move the spaceship to all directions"""
        # Need to check borders
        self.render(self.ship, True)
        if msg == "<UP>":
            self.ship.y -= 1
        elif msg == "<DOWN>":
            self.ship.y += 1
        elif msg == "<LEFT>":
            self.ship.x -= 1
        elif msg == "<RIGHT>":
            self.ship.x += 1
        self.render(self.ship)


def run_game():
    """Main function to run the game"""
    with FullscreenWindow() as window:
        cnt = 0
        # Initialize scene
        scene = Scene(window)
        
        with Input(sys.stdin) as input_generator:
            while True:
                window.render_to_terminal(scene.grid)
                for msg in input_generator:
                    if msg:
                        break
                if cnt > 100:
                    scene.background.move_grid()
                    scene.render(scene.background)
                    cnt = 0
                scene.update_scene(msg)
                time.sleep(0.01)
                cnt+=1


if __name__ == "__main__":
    # start with menu
    run_game()
