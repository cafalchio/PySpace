import random
import time, sys
import math

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red
from draw import Ship, Menu,  designs

"""Space game to kill Aliens Invasion (like space invaders, but left to write"""

class Scene:
    def __init__(self, window):
        self.window = window
        self.grid = FSArray(window.height, window.width)
        self.keys = [
            "<ESC>", "<UP>", "<DOWN>", "<LEFT>", 
            "<RIGHT>", "<SPACE>", "<ENTER>"
        ]
        # create initial conditions
        menu_spanw = window.width//2, window.height//2
        self.menu = Menu(menu_spanw)
        self.in_menu = True
        self.render(self.menu)
        self.ship = Ship(lives=3, gun=0, spawn=[10,10], design = designs["spaceship"])
    
    def start_game(self):
        print("Game started")
        self.render(self.ship)
    
    def update_scene(self, msg):
        if msg in self.keys and self.in_menu:
            self.menu_options(msg)
            
        elif msg in self.keys and not self.in_menus:
            self.move_ship(msg)
        
            
    def set_menu(self, in_menu):
        self.in_menu = in_menu
    
    def menu_options(self, msg):
        # print("UPDATE SCENE MENU")
        options = {
            0: "start_game",
            1: "records",
            2: "about"
        }
        if msg == "<UP>" and self.menu.option  > 0:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option - 1)
            
        elif msg == "<DOWN>" and self.menu.option  < 3:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option + 1)
            
        elif msg == "<ESC>":
            self.render(self.menu, True)
            self.set_menu(False) # stop to show menu
        # render menu (update grid)
        self.render(self.menu)

    def render(self, obj, delete = False):
        """Function that draw objects in the screen"""
        for i, part in enumerate(obj.design):
            for j, char in enumerate(part):
                if delete:
                    self.grid[obj.y + i, obj.x + j ]  = " "
                else:
                    self.grid[obj.y + i, obj.x + j ]  = char   

    def move_ship(self, msg):
        """Move the spaceship to all directions"""
        # Need to check borders
        self.render(ship, True)
        if msg == "<UP>":
            self.ship.y -= 1
        elif msg == "<DOWN>":
            self.ship.y += 1
        elif msg == "<LEFT>":
            self.ship.x -=1
        elif msg == "<RIGHT>":
            self.ship.x +=1
        render(self.ship)        
          

def run_game():
    with FullscreenWindow() as window:
        # Initialize scene
        scene = Scene(window)
        with Input(sys.stdin) as input_generator:
            while True:
                window.render_to_terminal(scene.grid)
                for msg in input_generator:
                    if msg:
                        break
                scene.update_scene(msg)
                # window.render_to_terminal(scene.grid)
                # control time
                time.sleep(.01)     

                
if __name__ == '__main__':
    # start with menu
    run_game()