from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red

designs = {
    "spaceship": ["▄-» ", "██)»", "▀-» "],
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
        self.gun = 0
        self.x = spawn[0]
        self.y = spawn[1]
        self.design = design
        self.bullet = None        

    def fire(self):
        return Bullet(self)

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
            return [on_red("-")]
        elif self.gun == 1:
            return ["="]
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
        self.design = self.get_desing(self.option)

    def set_option(self, option):
        self.option = option
        self.design = self.get_desing(self.option)

    def get_desing(self, option):

        art_menu_box = {
            0: [
                "╔════════════════╗",
                "║                ║",
                "║   » START! «   ║",
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
                "║  » RECORDS! «  ║",
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
                "║   » ABOUT! «   ║",
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
            11: [
                "╔════════════════╗",
                "║    Records:    ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "║ ________  000  ║",
                "╚════════════════╝",
            ],
        }
        return art_menu_box[option]
