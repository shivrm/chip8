import pygame

# Define constants
BGCOLOR = pygame.Color(0, 0, 0)
FGCOLOR = pygame.Color(255, 255, 255)


keyboard = "1234QWERASDFZXCV"
keycodes = [pygame.key.key_code(key) for key in keyboard]


class Display:
    def __init__(self) -> None:
        # Initialize display
        pygame.init()
        self.display = pygame.display.set_mode((640, 320))

        self.exit = False
        self.pressed_keys = [False] * 16

    def update(self):
        # Update display then handle events
        pygame.display.flip()

        for event in pygame.event.get():

            # Update list of pressed keys
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
        if self.exit:
            return

        # Flip a pixel on the screen.
        # Return true if the pixel was unset
        color = self.display.get_at((x * 10, y * 10))

        if color == FGCOLOR:
            pygame.draw.rect(self.display, BGCOLOR, pygame.Rect(x * 10, y * 10, 10, 10))
            return True

        else:
            pygame.draw.rect(self.display, BGCOLOR, pygame.Rect(x * 10, y * 10, 10, 10))
            return False

    def set_color(self, fg_color, bg_color):
        global FGCOLOR, BGCOLOR
        
        FGCOLOR = pygame.Color(*fg_color)
        BGCOLOR = pygame.color(*bg_color)

    def set_keyboard(self, keys):
        global keyboard, keycodes
        
        if len(keys) != 16:
            raise ValueError("keys must be a sequence of 16 characters")
        
        keyboard = keys
        keycodes = [pygame.key.key_code(key) for key in keyboard]

    def clear(self):
        self.display.fill(BGCOLOR)

    def quit(self):
        # Close the display
        self.exit = True
        pygame.quit()
