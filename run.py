import random
import time, sys
import math
from curtsies import FullscreenWindow, Input, FSArray, fsarray, fmtstr
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red
from draw import Ship, Menu, designs, Bullet
from sheet_data import Sheet
from pyfiglet import Figlet

"""Space game to kill Aliens Invasion game"""


class Background:
    """Create The stars background"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.design = [
            "".join(random.choice(" " * 20 + ".") for i in range(width))
            for _ in range(height)
        ]

        self.x = 0
        self.y = 0

    def move_background(self):
        """Move the background right to left"""
        ## remove first colum and add random colum at the end
        self.design = [row[1:] + random.choice(" " * 20 + ".") for row in self.design]


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
        self.bullets = [] # List of bullets to be updated every frame

    def update_scene(self, msg, cnt=None):
        """Update the scene"""
                    
        if msg == "<ESC>" and not self.in_menu:
            self.in_menu = True
            msg = "<UP>"

        if msg in self.keys and self.in_menu:
            self.menu_options(msg)

        elif msg in self.keys and not self.in_menu:
            if cnt % 4 == 0:
                self.move_ship(msg)
                


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

    def render(self, obj, delete=False):
        """Function that draw objects in the screen"""
        # update line per line to be faster
        if delete:
            self.grid[
                obj.y : obj.y + len(obj.design), obj.x : obj.x + len(obj.design[0])
            ] = fsarray([" " * len(obj.design[0]) for _ in range(len(obj.design))])
        else:
            self.grid[
                obj.y : obj.y + len(obj.design), obj.x : obj.x + len(obj.design[0])
            ] = fsarray(obj.design)


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
        elif msg == "<SPACE>":
            self.bullets.append(self.ship.fire())
            msg = None
            
        self.render(self.ship)


def run_game():
    MAX_FPS = 80
    cnt = 0
    time_per_frame = 1.0 / MAX_FPS
    """Main function to run the game"""
    with FullscreenWindow() as window:
        f = Figlet(font='epic')
        print(f.renderText("\tPySpace    Game"))
        input('press Enter key to start')
        print(red('\nLoading...'))
        scene = Scene(window)
        with Input() as input_generator:
            msg = None
            # Game loop
            # FPS example from curties library examples:
            # https://github.com/bpython/curtsies/blob/0a6fd78f6daa3a3cbf301376552ada6c1bd7dc83/examples/realtime.py
            while True:
                t0 = time.time()
                while True:
                    t = time.time()
                    temp_msg = input_generator.send(max(0, t - (t0 + time_per_frame)))
                    if temp_msg is not None:
                        msg = temp_msg
                    if time_per_frame < t - t0:
                        break
                    
                # Update the background
                if cnt % 8 == 0 and not scene.in_menu:
                    scene.background.move_background()
                    scene.render(scene.background)
                    cnt = 0
                
                # update scene
                scene.update_scene(msg, cnt)
                
                # stop to run forever in menu
                if scene.in_menu:
                    msg = None
                
                # update bullets
                if scene.bullets and not scene.in_menu:
                    for bullet in scene.bullets:
                        bullet.move()
                        if bullet.x < window.width:
                            scene.render(bullet)
                        else:
                            scene.bullets.remove(bullet)
                
                # update lives
                if scene.ship.lives > 0 and not scene.in_menu:
                    scene.grid[window.height - scene.ship.lives: window.height, 1 ] = fmtstr(red("♥"* scene.ship.lives) )
                
                # Render the scene
                window.render_to_terminal(scene.grid)
                cnt+=1
                # reset cnt
                if cnt > 1e6:
                    cnt = 1

if __name__ == "__main__":
    run_game()
