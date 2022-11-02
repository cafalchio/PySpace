"""run.py is the main file to run the game"""
import random
import time
import dataclasses
from curtsies import FullscreenWindow, Input, FSArray, fsarray, fmtstr
from curtsies.fmtfuncs import red
from pyfiglet import Figlet
from draw import Ship, Menu, designs
from sheet_data import Sheet


@dataclasses.dataclass
class Background:
    """Create The stars background"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.design = [
            "".join(random.choice(" " * 20 + ".") for i in range(width))
            for _ in range(height)
        ]
        self.row = 0
        self.col = 0

    def move_background(self):
        """Move the background right to left"""
        ## remove first colum and add random colum at the end
        self.design = [row[1:] + random.choice(" " * 20 + ".") for row in self.design]


class Scene:
    """Scene class to manage the game"""

    # pylint: disable=too-many-instance-attributes
    # Disabled because it is the main class that controls the game
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
        """ Create enemies in the screen"""
        type_ship = random.choice([0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3,3,3,3, 5, 5, 5, 5])
        self.enemies.append(
            Ship(
                lives=type_ship + 1,
                gun=type_ship,
                spawn=[
                    self.window.width - 15,
                    random.randint(10, self.window.height - 10),
                ],
                design=designs["alien_" + str(type_ship)],
            )
        )

    def make_enemies(self, cnt, in_menu):
        """Create enemies"""
        if cnt % 80 == 0 and not in_menu:
            if len(self.enemies) < 5 and cnt % 200 == 0:
                self.enemies.append(self.create_enemies())
            self.enemies.append(self.create_enemies())
        # for enemy in self.enemies:
        #     if enemy:
        #         self.render(enemy)

    def remove_enemy(self, enemy):
        """Remove enemy from the list"""
        self.enemies.remove(enemy)

    def update_ship(self, msg, cnt=None):
        """Update the scene"""
        if msg == "<ESC>" and not self.in_menu:
            self.in_menu = True
            msg = "<UP>"
        if msg in self.keys and self.in_menu:
            self.menu_options(msg)
        elif msg in self.keys and not self.in_menu:
            if cnt % 3 == 0:
                self.move_ship(msg)
        if msg is None:
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
        elif (msg in ["<SPACE>", "<Ctrl-j>"]) and self.menu.option == 0:
            self.render(self.menu, True)
            self.in_menu = False  # need to restart the game

        elif (msg in ["<SPACE>", "<Ctrl-j>"]) and self.menu.option == 1:
            self.render(self.menu, True)
            self.menu.set_option(11)

        elif (msg in ["<SPACE>", "<Ctrl-j>"]) and self.menu.option == 2:
            self.render(self.menu, True)
            self.menu.set_option(12)

        # exit the submenus
        elif msg == "<ESC>" and self.menu.option > 3:
            self.render(self.menu, True)
            self.menu.set_option(self.menu.option - 10)

        # render menu if menu is active
        if self.in_menu:
            self.render(self.menu)

    def render(self, obj, delete=False):
        """Function that draw objects in the screen"""
        # update line per line to be faster
        if delete:
            self.grid[
                obj.col : obj.col + len(obj.design),
                obj.row : obj.row + len(obj.design[0]),
            ] = fsarray([" " * len(obj.design[0]) for _ in range(len(obj.design))])
        else:
            try:
                self.grid[
                    obj.col : obj.col + len(obj.design),
                    obj.row : obj.row + len(obj.design[0]),
                ] = fsarray(obj.design)

            except ValueError:
                # sometimes, parts of the ship are out of the screen
                # In these cases the ship is not drawn
                pass

    def move_ship(self, msg):
        """Move the spaceship to all directions"""
        # Need to check borders
        self.render(self.ship, True)
        if msg == "<UP>" and self.ship.col > 1:
            self.ship.col -= 1
        elif msg == "<DOWN>" and self.ship.col < self.window.height - 5:
            self.ship.col += 1
        elif msg == "<LEFT>" and self.ship.row > 5:
            self.ship.row -= 1
        elif msg == "<RIGHT>" and self.ship.row < self.window.width - 10:
            self.ship.row += 1
        elif msg == "<SPACE>":
            self.bullets.append(self.ship.fire())
            msg = None
        self.render(self.ship)

    def end_game(self):
        """ End the game"""
        fig = Figlet(font="big")
        print(fig.renderText("\nGAME  OVER"))
        print(f"Your score is: {self.score}")
        time.sleep(1)
        if self.score > sorted(self.data)[0]:
            print("Congratulations! You are in the top 7\n")
            name = input(fmtstr("Name for Scoreboard: "))
            if len(name) > 7:
                name = name[:7]
            self.sheet.update_records([name, self.score])
            print("\n\nYour score has been added to the leaderboard!\n\n")
            time.sleep(1)
        input("\nPress Run Program to play again\n")

    def update_background(self, cnt, in_menu):
        """Update the background"""
        if cnt % 12 == 0 and not in_menu:
            self.background.move_background()
            self.render(self.background)

    def update_bullets(self, in_menu):
        """Update the bullets"""
        # update bullets
        if self.bullets and not in_menu:
            for bullet in self.bullets:
                bullet.move()
                if bullet.row < self.window.width:
                    self.render(bullet)
                else:
                    self.bullets.remove(bullet)

    def update_enemies(self, cnt, in_menu):
        """Update the enemies"""
        if self.enemies and not in_menu:
            for enemy in self.enemies:
                # remove the ones that passed the screen
                if not enemy:
                    continue

                # Increase randomnes of the enemies
                if self.score % 100 == 0 and self.score != 0:
                    enemy.inc_dificulty()

                if enemy.row < 2:
                    self.score -= enemy.lives
                    self.remove_enemy(enemy)
                    continue
                # remove dead enemies
                if enemy.lives <= 0:
                    self.score += 1 + enemy.gun
                    self.remove_enemy(enemy)
                    continue

                if cnt % 10 == 0:
                    enemy.move(self.window)

                for bullet in self.bullets:
                    if bullet.all_points() in enemy.all_points():
                        self.render(bullet, True)
                        self.bullets.remove(bullet)
                        enemy.shooted()

                # fast way to detect collision
                if set(enemy.all_points()).intersection(set(self.ship.all_points())):
                    self.ship.shooted()
                    self.remove_enemy(enemy)
                self.render(enemy)
                    

def intro():
    """ Intro of the game"""
    fig = Figlet(font="big")
    print(fig.renderText("   PySpace    Game"))
    print("\tProtect the Earth from the aliens!")
    print("\tUse the arrow keys to move, space to shoot and esc for menu\n")
    input("press Enter to start")
    print(red("\nLoading..."))


def run_game():
    """Main function to run the game"""
    cnt = 0
    fps = 45
    with FullscreenWindow() as window:
        intro()
        scene = Scene(window)
        with Input() as input_generator:
            msg = None
            # Game loop
            # FPS example from curties library examples:
            # https://github.com/bpython/curtsies/blob/0a6fd78f6daa3a3cbf301376552ada6c1bd7dc83/examples/realtime.py
            while True:
                time_per_frame = 1.0 / fps
                time_0 = time.time()
                while True:
                    t_now = time.time()
                    temp_msg = input_generator.send(
                        max(0, t_now - (time_0 + time_per_frame))
                    )
                    if temp_msg is not None and temp_msg in scene.keys:
                        msg = temp_msg
                    if time_per_frame < t_now - time_0:
                        break

                # Update the background
                scene.update_background(cnt, scene.in_menu)

                # Create the aliens
                scene.make_enemies(cnt, scene.in_menu)

                # update scene
                scene.update_ship(msg, cnt)
                scene.render(scene.ship)
                # stop to run forever in menu
                if scene.in_menu:
                    msg = None
                    cnt = 0

                # stop menu to run forever
                elif not scene.in_menu and msg == "<ESC>":
                    msg = None
                    cnt = 0

                # update bullets
                scene.update_bullets(scene.in_menu)
                # update enemies
                scene.update_enemies(cnt, scene.in_menu)
              
                # negative score looses lives
                if scene.score < 0:
                    scene.ship.lives -= 1
                    scene.score = 0

                # update score and lives
                scene.grid[0, 1 : 1 + len(f"Score: {scene.score}")] = [
                    f"Score: {scene.score}"
                ]
                scene.grid[1, 1 : 1 + scene.ship.lives * 2] = [
                    fmtstr(red("♥ " * scene.ship.lives))
                ]

                # rencer the entire grid
                window.render_to_terminal(scene.grid)

                # check if game is over
                if scene.ship.lives == 0:
                    break

                # add or reset cnt
                cnt += 1
                if cnt > 1e5:
                    cnt = 1
    # end game
    scene.end_game()


if __name__ == "__main__":
    run_game()
