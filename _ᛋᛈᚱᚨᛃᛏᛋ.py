import pygame
pygame.init()

#určení proměných
width,height = 1000,600
screen = pygame.display.set_mode((width,height))

lighter = (224,248,208)
light = (136,192,112)
dark = (52,104,86)
darker = (8,24,32)

#nehybné zdi
class wall(pygame.sprite.Sprite):
    def __init__(self,start,width,height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(dark)
        self.rect = self.image.get_rect()
        self.rect.topleft = start