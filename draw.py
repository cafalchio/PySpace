""" Draw.py - Contains the Draw, Menu, Ship and Bullet classes. """
import random
from curtsies.fmtfuncs import red, green, yellow, cyan, magenta
from sheet_data import Sheet


designs = {
    "spaceship": [cyan("▄-  "), cyan("██)»"), cyan("▀-  ")],
    "alien_0": [yellow("<○{")],
    "alien_1": [magenta("   █§"), magenta(" <(█§"), magenta("   █§")],
    "alien_2": [red(" ╔-{"), red("<╣-{"), red(" ╚-{")],
    "alien_3": [green("  /-"), green("<<{ "), green("  \\-")],
    "alien_4": [yellow("  ┼ "), yellow("<E┤┼"), yellow("  ┼ ")],
}


class Ship:
    """A spaceship that can be drawn on the screen."""

    def __init__(self, lives, gun, spawn, design):
        self.lives = lives
        self.gun = gun
        self.x_y = [spawn[0], spawn[1]]
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

    def move(self, window):
        """Move enemy ship"""
        speed = random.choice([4, 3, 2, 2, 1, 1, 1])
        up_down = random.choice([1, 0, 0, 0, -1])
        # limit the speed
        self.x_y[0] -= min(3, speed + self.difficulty)
        self.x_y[1] -= up_down
        if self.x_y[0] + up_down <= 10:
            self.x_y[0] += up_down + 1
        elif self.x_y[0] + up_down >= window[0] - 10:
            self.x_y[0] += up_down - 1

    def all_points(self):
        """ Return all the points of the ship """
        for i in range(len(self.design)):
            for j in range(len(self.design[0])):
                self.points.append((self.x_y[0] + j, self.x_y[1] + i))
        return self.points


class Bullet:
    """A bullet that can be drawn on the screen."""

    def __init__(self, obj):
        self.x_y = [obj.x_y[0] + len(obj.design[0]), self.get_y(obj)]
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
            return obj.x_y[1] + 1
        return obj.x_y[1]

    def move(self):
        """ Move the bullet """
        if self.dir > 0:
            self.x_y[0] += 4
        else:
            self.x_y[0] -= 4

    def all_points(self):
        """ Return all the points of the bullet """
        return (self.x_y[0], self.x_y[1])


class Menu:
    """ Create the design of the menu """

    def __init__(self, spawn):
        self.x_y = [spawn[0] - 8, spawn[1] - 7]
        self.option = 0
        sheet = Sheet()
        self.data = sheet.data
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
            11: ["╔════════════════╗", "║     Top 10!    ║"]
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
        if len(data) > 10:
            data = data[:10]
        if len(data) < 10:
            for i in range(10 - len(data)):
                data.append(["---------", "0000"])
        for name, score in data:
            if len(name) < 9:
                name = name + " " * (9 - len(name))
            if len(str(score)) < 5:
                score = " " * (5 - len(str(score))) + str(score)
            yield f"║ {name}{score} ║"
