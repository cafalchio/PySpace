from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red
from sheet_data import Sheet

designs = {
    "spaceship": [yellow("▄-» "), yellow("██)»"), yellow("▀-» ")],
    "aliens_0": ["<║E", "<║E"],
    "aliens_1": [
        "   █§",
        "<(█§",
        "   █§",
    ],
    "aliens_2": [
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

    def fire(self):
        return Bullet(self)

    def set_lives(self, n):
        self.lives = self.lives + n


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
            self.x += 1
        else:
            self.x -= 1


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
        """Format the score to be displayed in the menu"""
        data = sorted(self.data, key=lambda x: x[1])
        if len(data) > 7:
            data = data[:7]
        if len(data) < 7:
            for i in range(7 - len(data)):
                data.append(["-------", "00"])
        for d1, d2 in data:
            if len(d1) < 7:
                d1 = d1 + " " * (7 - len(d1))
            if len(d2) < 5:
                d2 = " " * (5 - len(d2)) + d2
            yield f"║ {d1}  {d2} ║"
