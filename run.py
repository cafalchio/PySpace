import random
import time, sys
import math
from curtsies import FullscreenWindow, Input, FSArray, fsarray, fmtstr
from curtsies.fmtfuncs import red
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
        self.ship = Ship(lives=3, gun=2, spawn=[10, 10], design=designs["spaceship"])
        self.enemies = []

        self.background = Background(window.width, window.height)
        self.bullets = []  # List of bullets to be updated every frame
        self.score = 0
        self.sheet = Sheet()
        self.data = self.sheet.get_scores()

    def create_enemies(self):
        tipo = random.choice([0, 0, 0, 1, 1, 1, 1, 1,  2, 2, 2, 2])
        self.enemies.append(
            Ship(
                lives=tipo + 3,
                gun=tipo,
                spawn=[
                    self.window.width - 15,
                    random.randint(10, self.window.height - 10),
                ],
                design=designs["alien_" + str(tipo)],
            )
        )

    def remove_enemy(self, enemy):
        """Remove enemy from the list"""
        self.enemies.remove(enemy)

    def update_scene(self, msg, cnt=None):
        """Update the scene"""

        if msg == "<ESC>" and not self.in_menu:
            self.in_menu = True
            msg = "<UP>"

        if msg in self.keys and self.in_menu:
            self.menu_options(msg)

        elif msg in self.keys and not self.in_menu:
            if cnt % 3 == 0:
                self.move_ship(msg)
        if msg == None:
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
            self.in_menu = False  # stop to show menu
            self.render(self.menu, True)

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
            try:
                self.grid[
                    obj.y : obj.y + len(obj.design), obj.x : obj.x + len(obj.design[0])
                ] = fsarray(obj.design)
            except Exception as e:
                if e == ValueError:
                    # sometimes, parts of the ship are out of the screen
                    # In these cases the ship is not drawn
                    pass

    def move_ship(self, msg):
        """Move the spaceship to all directions"""
        # Need to check borders
        self.render(self.ship, True)
        if msg == "<UP>" and self.ship.y > 1:
            self.ship.y -= 1
        elif msg == "<DOWN>" and self.ship.y < self.window.height - 5:
            self.ship.y += 1
        elif msg == "<LEFT>" and self.ship.x > 5:
            self.ship.x -= 1
        elif msg == "<RIGHT>" and self.ship.x < self.window.width - 10:
            self.ship.x += 1
        elif msg == "<SPACE>":
            self.bullets.append(self.ship.fire())
            msg = None
        self.render(self.ship)

    def end_game(self):
        f = Figlet(font="epic")
        print(f.renderText("\nGAME  OVER"))
        print(f"Your score is: {self.score}")

        time.sleep(2)
        if self.score > sorted(self.data)[0]:
            print("Congratulations! You are in the top 7\n")
            name = input(fmtstr("Name for Scoreboard: "))
            if len(name) > 7:
                name = name[:7]
            self.sheet.update_records([name, self.score])
            print("\n\nYour score has been added to the leaderboard!\n\n")
            time.sleep(2)

        input("\nPress Run Program to play again\n")
        return None

    def update_background(self):
        self.background.move_background()
        self.render(self.background)


def intro():
    f = Figlet(font="epic")
    print(f.renderText("         PySpace    Game"))
    input("press Enter to start")
    print(red("\nLoading..."))


def run_game():
    MAX_FPS = 50
    cnt = 0
    time_per_frame = 1.0 / MAX_FPS
    """Main function to run the game"""
    with FullscreenWindow() as window:
        intro()
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
                    if temp_msg is not None and temp_msg in scene.keys:
                        msg = temp_msg

                    if time_per_frame < t - t0:
                        break

                # Update the background
                if cnt % 12 == 0 and not scene.in_menu:
                    scene.update_background()

                # Create enemies
                if cnt % 100 == 0 and not scene.in_menu:
                    if len(scene.enemies) < 7 and cnt % 500 == 0:
                        scene.enemies.append(scene.create_enemies())
                    scene.create_enemies()
                for enemy in scene.enemies:
                    # if enemy:
                    scene.render(enemy)

                # update scene
                scene.update_scene(msg, cnt)

                # stop to run forever in menu
                if scene.in_menu:
                    msg = None
                    cnt = 0

                # stop menu to run forever
                elif not scene.in_menu and msg == "<ESC>":
                    msg = None
                    cnt = 0

                # update bullets
                if scene.bullets and not scene.in_menu:
                    for bullet in scene.bullets:
                        bullet.move()
                        if bullet.x < window.width:
                            scene.render(bullet)
                        else:
                            scene.bullets.remove(bullet)

                # update enemies
                if scene.enemies and not scene.in_menu:
                    for enemy in scene.enemies:
                        # remove the ones that passed the screen
                        if not enemy:
                            continue
                        if enemy.x < 2:
                            scene.score -= enemy.lives
                            scene.remove_enemy(enemy)
                            continue
                        # remove dead enemies
                        if enemy.lives <= 0:
                            scene.score += 1 + enemy.gun
                            scene.render(enemy, True)
                            scene.remove_enemy(enemy)
                            continue

                        # move the enemies
                        if enemy.y < 10:
                            enemy.y += 3
                        elif enemy.y > window.height - 10:
                            enemy.y -= 3
                        elif enemy.x > window.width - 10:
                            enemy.x -= 3
                        else:
                            if cnt % 10 == 0:
                                scene.render(enemy, True)
                                enemy.move(window.width, window.height, target = (scene.ship.x, scene.ship.y))

                        for bullet in scene.bullets:
                            if bullet.all_points() in enemy.all_points():
                                scene.render(bullet, True)
                                scene.bullets.remove(bullet)
                                enemy.shooted()

                        # fast way to detect collision
                        if set(enemy.all_points()).intersection(
                            set(scene.ship.all_points())
                        ):
                            scene.ship.shooted()
                            scene.render(enemy, True)
                            scene.remove_enemy(enemy)

                # negative score looses lives
                if scene.score < 0:
                    scene.ship.lives -= 1
                    scene.score = 0

                # update lives
                if scene.ship.lives > 0 and not scene.in_menu:
                    scene.grid[
                        window.height - scene.ship.lives : window.height, 1
                    ] = fmtstr(red("♥" * scene.ship.lives))

                # update score botton left
                print("\tScore: ", scene.score)

                # Render the scene
                window.render_to_terminal(scene.grid)
                cnt += 1
                if scene.ship.lives == 0:
                    break

                # reset cnt
                if cnt > 1e5:
                    cnt = 1

    scene.end_game()
    return None


if __name__ == "__main__":
    run_game()
