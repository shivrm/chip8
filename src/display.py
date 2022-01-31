import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"

import pygame

# Define constants

keyboard = "1234QWERASDFZXCV"
keycodes = [pygame.key.key_code(key) for key in keyboard]


class Display:
    def __init__(self, fgcolor=(255, 255, 255), bgcolor=(0, 0, 0)) -> None:
        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode((640, 320))
        
        self.set_color(fgcolor, bgcolor, clear=True)
        
        self.exit = False
        self.pressed_keys = [False] * 16

    def update(self):
        # Update display and handle events
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in keycodes:
                    idx = keycodes.index(event.key)
                    self.pressed_keys[idx] = True

            if event.type == pygame.KEYUP:
                if event.key in keycodes:
                    idx = keycodes.index(event.key)
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


    def clear(self):
        self.display.fill(self.BGCOLOR)

    def quit(self):
        # Close the display
        self.exit = True

        pygame.quit()
