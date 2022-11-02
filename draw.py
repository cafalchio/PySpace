""" Draw.py - Contains the Draw, Menu, Ship and Bullet classes. """
import random
from curtsies.fmtfuncs import red, green, yellow, cyan, magenta
from sheet_data import Sheet


designs = {
    "spaceship": [cyan("▄-  "), cyan("██)»"), cyan("▀-  ")],
    "alien_0": [yellow("<○█")],
    "alien_1": [magenta("   █§"), magenta(" <(█§"), magenta("   █§")],
    "alien_2": [red(" ╔-{"), red("<╣-{"), red(" ╚-{")],
}


class Ship:
    """A spaceship that can be drawn on the screen."""

    # pylint: disable=too-many-instance-attributes
    # 8 is reasonable in this case. I could use a dict but I prefer this way
    def __init__(self, lives, gun, spawn, design):
        self.lives = lives
        self.gun = gun
        self.row = spawn[0]
        self.col = spawn[1]
        self.design = design
        self.bullet = None
        self.points = []
        self.difficulty = 0

    def fire(self):
        """ Fire a bullet """
        return Bullet(self)

    def shooted(self):
        """ Remove a life from the ship """
        self.lives -= 1

    def inc_dificulty(self):
        """ Increase the difficulty """
        self.difficulty += 1

    def move(self, target=None):
        """Move enemy ship"""
        new_y = None
        y_diff = target[1] - self.col
        # scape from the bullet
        if y_diff > 0:  # keep bellow the bullet
            new_y = random.choice([0, -1])
        elif y_diff < 0:  # keep above the bullet
            new_y = random.choice([0, 1])
        else:
            new_y = random.choice([-1, 1])

        if self.gun == 0:

            self.row -= random.choice([0, 1, 2, 2, 3, 3, 4, 4]) + self.difficulty
            self.col += new_y

        elif self.gun == 1:
            self.row -= random.choice([0, 0, 1, 1, 2, 2, 3, 3]) + self.difficulty
            self.col += new_y

        elif self.gun == 2:
            self.row -= random.choice([0, 0, 0, 1, 1, 2, 2, 3, 3]) + self.difficulty
            self.col += new_y

    def all_points(self):
        """ Return all the points of the ship """
        for i in range(len(self.design)):
            for j in range(len(self.design[0])):
                self.points.append((self.row + j, self.col + i))
        return self.points

    def check_borders(self, window):
        """ Check if the ship is out of the screen """
        if self.col < 0 or self.row > window.height or self.col > window.width:
            return True
        return False


class Bullet:
    """A bullet that can be drawn on the screen."""

    def __init__(self, obj):
        self.row = obj.row + len(obj.design[0])
        self.col = self.get_y(obj)
        self.gun = obj.gun
        if obj == "spaceship":
            self.dir = -1
        else:
            self.dir = 1
        self.design = self.get_desing()

    def get_desing(self):
        """ Return the design of the bullet """
        style = ""
        if self.gun == 0:
            style = ["-"]
        elif self.gun == 1:
            style = [red("=")]
        elif self.gun == 2:
            style = [yellow("»")]
        return style

    def get_y(self, obj):
        """ Return the y position of the bullet """
        if len(obj.design) == 3:
            return obj.col + 1
        return obj.col

    def move(self):
        """ Move the bullet """
        if self.dir > 0:
            self.row += 4
        else:
            self.row -= 4

    def all_points(self):
        """ Return all the points of the bullet """
        return (self.row, self.col)


class Menu:
    """ Create the design of the menu """

    def __init__(self, spawn):
        self.row = spawn[0] - 8
        self.col = spawn[1] - 7
        self.option = 0
        sheet = Sheet()
        self.data = sheet.get_records()
        self.design = self.get_desing(self.option)

    def set_option(self, option):
        """ Set the option of the menu """
        self.option = option
        self.design = self.get_desing(self.option)

    def get_desing(self, option):
        """ Return the design of the menu """
        art_menu_box = {
            0: [
                "╔════════════════╗",
                "║                ║",
                "║   " + green("»") + " START! " + green("«") + "   ║",
                "║                ║",
                "║    RECORDS!    ║",
                "║                ║",
                "║     ABOUT!     ║",
                "║                ║",
                "╚════════════════╝",
            ],
            1: [
                "╔════════════════╗",
                "║                ║",
                "║     START!     ║",
                "║                ║",
                "║  " + green("»") + " RECORDS! " + green("«") + "  ║",
                "║                ║",
                "║     ABOUT!     ║",
                "║                ║",
                "╚════════════════╝",
            ],
            2: [
                "╔════════════════╗",
                "║                ║",
                "║     START!     ║",
                "║                ║",
                "║    RECORDS!    ║",
                "║                ║",
                "║   " + green("»") + " ABOUT! " + green("«") + "   ║",
                "║                ║",
                "╚════════════════╝",
            ],
            12: [
                "╔════════════════╗",
                "║     About:     ║",
                "║                ║",
                "║   PySpace 1.0  ║",
                "║                ║",
                "║   by Matheus   ║",
                "║   Cafalchio    ║",
                "║                ║",
                "╚════════════════╝",
            ],
            11: ["╔════════════════╗", "║    Records:    ║"]
            + list(self.format_score())
            + ["╚════════════════╝"],
        }
        return art_menu_box[option]

    def format_score(self):
        """Format and sort the score to be displayed in the menu"""
        # change the score to integers and sort it
        data = []
        for i in self.data:
            data.append([i[0], int(i[1])])

        data = sorted(data, key=lambda x: x[1], reverse=True)
        if len(data) > 7:
            data = data[:7]
        if len(data) < 7:
            for i in range(7 - len(data)):
                data.append(["-------", "00"])
        for name, score in data:
            if len(name) < 7:
                name = name + " " * (7 - len(name))
            if len(str(score)) < 5:
                score = " " * (5 - len(str(score))) + str(score)
            yield f"║ {name}  {score} ║"
