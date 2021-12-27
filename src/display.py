import pygame

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

pygame.init()
DISPLAY = pygame.display.set_mode((640, 320))

def update():
    pygame.display.update()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()

def set(x, y):
    pygame.draw.rect(DISPLAY, WHITE, pygame.Rect(x * 10, y * 10, 10, 10))
    pygame.display.update()
    
def unset(x, y):
    pygame.draw.rect(DISPLAY, BLACK, pygame.Rect(x * 10, y * 10, 10, 10))
    pygame.display.update()

def quit():
    pygame.quit()
    