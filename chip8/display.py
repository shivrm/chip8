import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"

import pygame


class Display:
    def __init__(
        self,
        fgcolor=(255, 255, 255),
        bgcolor=(0, 0, 0),
        keys="X123QWEASDZC4RFV",
        scale=10,
    ) -> None:

        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode((64 * scale, 32 * scale))

        self.scale = scale

        # Set color and keyboard
        self.set_color(fgcolor, bgcolor, clear=True)
        self.set_keys(keys)

        self.exit = False  # Whether the display has been closed
        self.pressed_keys = [False] * 16  # Which keys have been pressed

    def update(self):
        # Update display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():

            # If any key is pressed, mark it as pressed
            if event.type == pygame.KEYDOWN:
                if event.key in self.keycodes:
                    idx = self.keycodes.index(event.key)
                    self.pressed_keys[idx] = True

            # If unpressed, make the corresponding value False
            if event.type == pygame.KEYUP:
                if event.key in self.keycodes:
                    idx = self.keycodes.index(event.key)
                    self.pressed_keys[idx] = False

            # Check if close button was pressed
            if event.type == pygame.QUIT:
                self.exit = True
                pygame.quit()

    def flip(self, x, y):
        if self.exit:
            return

        scale = self.scale

        # Flip a pixel on the screen.
        # Return true if the pixel was unset
        color = self.display.get_at((x * scale, y * scale))

        if color == self.FGCOLOR:
            pygame.draw.rect(
                self.display,
                self.BGCOLOR,
                pygame.Rect(x * scale, y * scale, scale, scale),
            )
            return True

        else:
            pygame.draw.rect(
                self.display,
                self.FGCOLOR,
                pygame.Rect(x * scale, y * scale, scale, scale),
            )
            return False

    def set_color(self, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0), clear=False):
        self.FGCOLOR = pygame.Color(*fgcolor)
        self.BGCOLOR = pygame.Color(*bgcolor)

        if clear:
            self.clear()

    def set_keys(self, keys="X123QWEASDZC4RFV"):
        self.keyboard = keys
        self.keycodes = [pygame.key.key_code(key) for key in self.keyboard]

    def clear(self):
        self.display.fill(self.BGCOLOR)

    def quit(self):
        # Close the display
        self.exit = True
        pygame.quit()
