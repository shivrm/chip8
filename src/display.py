import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"

import pygame

class Display:
    def __init__(self, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0),
                 keys="X123QWEASDZC4RFV") -> None:
        
        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode((640, 320))
        
        self.set_color(fgcolor, bgcolor, clear=True)
        self.set_keys(keys)
        
        self.exit = False
        self.pressed_keys = [False] * 16

    def update(self):
        # Update display and handle events
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in self.keycodes:
                    idx = self.keycodes.index(event.key)
                    self.pressed_keys[idx] = True

            if event.type == pygame.KEYUP:
                if event.key in self.keycodes:
                    idx = self.keycodes.index(event.key)
                    self.pressed_keys[idx] = False

            if event.type == pygame.QUIT:
                self.exit = True
                pygame.quit()

    def flip(self, x, y):
        if self.exit: return
        
        # Flip a pixel on the screen.
        # Return true if the pixel was unset
        color = self.display.get_at((x * 10, y * 10))

        if color == self.FGCOLOR:
            pygame.draw.rect(self.display, self.BGCOLOR, pygame.Rect(x * 10, y * 10, 10, 10))
            return True

        else:
            pygame.draw.rect(self.display, self.FGCOLOR, pygame.Rect(x * 10, y * 10, 10, 10))
            return False

    def set_color(self, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0), clear=False):
        self.FGCOLOR = pygame.Color(*fgcolor)
        self.BGCOLOR = pygame.Color(*bgcolor)
        
        if clear: self.clear()

    def set_keys(self, keys="X123QWEASDZC4RFV"):
        self.keyboard = keys
        self.keycodes = [pygame.key.key_code(key) for key in self.keyboard]

    def clear(self):
        self.display.fill(self.BGCOLOR)

    def quit(self):
        # Close the display
        self.exit = True

        pygame.quit()
