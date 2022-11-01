from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red, blue
from sheet_data import Sheet
import random

designs = {
    "spaceship": [yellow("▄-» "), yellow("██)»"), yellow("▀-» ")],
    "alien_0": [blue("<║E")],
    "alien_1": [
        "   █§",
        "<(█§",
        "   █§",
    ],
    "alien_2": [
        " ╔-{",
        "<╣-{",
        " ╚-{",
    ],
}


class Ship:
    def __init__(self, lives, gun, spawn, design):
        self.lives = lives
        self.gun = 1
        self.x = spawn[0]
        self.y = spawn[1]
        self.design = design
        self.bullet = None
        self.points = []

    def fire(self):
        return Bullet(self)

    def shooted(self):
        self.lives -= 1

    def move(self, max_x, max_y):
        new_x = self.x + random.choice([-3,-2,-1])
        new_y = self.y + random.choice([-2, 2])
        self.x = new_x
        self.y = new_y
            
    def all_points(self):
        for i in range(len(self.design)):
            for j in range(len(self.design[0])):
                self.points.append((self.x + j, self.y - i))
        return self.points
        
class Bullet:
    def __init__(self, object):
        self.x = object.x + len(object.design[0])
        self.y = self.get_y(object)
        self.gun = object.gun
        if object == "spaceship":
            self.dir = -1
        else:
            self.dir = 1
        self.design = self.get_desing()

    def get_desing(self):
        if self.gun == 0:
            return [red("-")]
        elif self.gun == 1:
            return [red("=")]
        elif self.gun == 2:
            return ["»"]

    def get_y(self, object):
        if len(object.design) == 3:
            return object.y + 1
        else:
            return object.y

    def move(self):
        if self.dir > 0:
            self.x += 3
        else:
            self.x -= 3

    def all_points(self):
        return (self.x, self.y)

class Menu:
    def __init__(self, spawn):
        self.x = spawn[0] - 8
        self.y = spawn[1] - 7
        self.option = 0
        sheet = Sheet()
        self.data = sheet.get_records()
        self.design = self.get_desing(self.option)

    def set_option(self, option):
        self.option = option
        self.design = self.get_desing(self.option)

    def get_desing(self, option):

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
                "║   PySpace by   ║",
                "║                ║",
                "║    Matheus     ║",
                "║   Cafalchio    ║",
                "║                ║",
                "╚════════════════╝",
            ],
            11: ["╔════════════════╗", "║    Records:    ║"]
            + list(self.format_score())
            + [
                "╚════════════════╝",
            ],
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
        for d1, d2 in data:
            if len(d1) < 7:
                d1 = d1 + " " * (7 - len(d1))
            if len(str(d2)) < 5:
                d2 = " " * (5 - len(str(d2))) + str(d2)
            yield f"║ {d1}  {d2} ║"
