import pygame
pygame.init()

#určení proměných
WIDTH,HEIGHT = 1000,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

lighter = (224,248,208)
light = (136,192,112)
dark = (52,104,86)
darker = (8,24,32)

player_speed = 5

#nehybné zdi
class wall(pygame.sprite.Sprite):
    def __init__(self,start,width,height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.topleft = start

#vertikální hráč
class ver_player(pygame.sprite.Sprite):
    def __init__(self,pos,width,heigth,up,down):
        super().__init__()
        self.image = pygame.Surface((width,heigth))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.center = (pos,HEIGHT//2)
        self.up = up
        self.down = down
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.rect.y -= player_speed
        if keys[self.down]:
            self.rect.y += player_speed
#horizontáln hráč
class hor_player(pygame.sprite.Sprite):
    def __init__(self,pos,width,heigth,left,right):
        super().__init__()
        self.image = pygame.Surface((width,heigth))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,pos)
        self.left = left
        self.right = right
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.rect.x -= player_speed
        if keys[self.right]:
            self.rect.x += player_speed
            