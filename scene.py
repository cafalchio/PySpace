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
            "<ENTER>",
        ]
        # create initial conditions
        menu_spanw = window.width // 2, window.height // 2
        self.menu = Menu(menu_spanw)
        self.in_menu = True
        self.render(self.menu)
        self.ship = Ship(lives=3, gun=0, spawn=[10, 10], design=designs["spaceship"])

    def start_game(self):
        """Start the game"""
        print("Game started")
        self.render(self.ship)

    def update_scene(self, msg):
        """Update the scene"""

        if msg == "<ESC>" and not self.in_menu:
            self.in_menu = True
            msg = "<UP>"

        if msg in self.keys and self.in_menu:
            self.menu_options(msg)

        elif msg in self.keys and not self.in_menu:
            self.move_ship(msg)

    def set_menu(self, in_menu):
        self.in_menu = in_menu

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
        elif msg == "<SPACE>" and self.menu.option == 0:
            self.render(self.menu, True)
            self.in_menu = False  # need to restart the game

        elif msg == "<SPACE>" and self.menu.option == 1:
            self.render(self.menu, True)
            self.menu.set_option(11)

        elif msg == "<SPACE>" and self.menu.option == 2:
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
        for i, part in enumerate(obj.design):
            for j, char in enumerate(part):
                if delete:
                    self.grid[obj.y + i, obj.x + j] = " "
                else:
                    self.grid[obj.y + i, obj.x + j] = char

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
        self.render(self.ship)
