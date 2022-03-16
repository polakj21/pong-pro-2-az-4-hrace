import pygame
pygame.init()

#určení proměných
WIDTH,HEIGHT =700,700
screen = pygame.display.set_mode((WIDTH,HEIGHT))

lighter = (224,248,208)
light = (136,192,112)
dark = (52,104,86)
darker = (8,24,32)

player_speed = 8
ball_speed = 6

#nehybné zdi
class wall(pygame.sprite.Sprite):
    def __init__(self,start,width,height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.topleft = start

#míček
class ball():
    def __init__(self,center,r,direction):
        self.r = r
        self.rect_1 = pygame.Rect(center[0]-r,center[1]-r,2*r,2*r)
        self.rect_2 = pygame.Rect(center[0]-(r**2/2)**0.5,center[1]-(r**2/2)**0.5,2*((r**2/2)**0.5),2*((r**2/2)**0.5))
        self.dir = direction
        self.id = None
    def move(self):
        self.rect_1.center += self.dir*ball_speed
        self.rect_2.center += self.dir*ball_speed
    def draw(self):
        pygame.draw.circle(screen,light,self.rect_1.center,self.r)
        

#vertikální hráč
class ver_player(pygame.sprite.Sprite):
    def __init__(self,pos,width,heigth,up,down,_id):
        super().__init__()
        self.image = pygame.Surface((width,heigth))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.center = (pos,HEIGHT//2)
        self.up = up
        self.down = down
        self.id = _id
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.rect.y -= player_speed
        if keys[self.down]:
            self.rect.y += player_speed
            
#horizontáln hráč
class hor_player(pygame.sprite.Sprite):
    def __init__(self,pos,width,heigth,left,right,_id):
        super().__init__()
        self.image = pygame.Surface((width,heigth))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,pos)
        self.left = left
        self.right = right
        self.id = _id
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.rect.x -= player_speed
        if keys[self.right]:
            self.rect.x += player_speed