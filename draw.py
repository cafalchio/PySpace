designs = {
    "spaceship": ["▄»", "██)»", "▀»"],
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
