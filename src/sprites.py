import pygame
pygame.init()

#určení proměných
WIDTH,HEIGHT,HEIGHT_2 = 700,700,449
screen = pygame.display.set_mode((WIDTH,HEIGHT_2))
CENTER = (WIDTH//2,HEIGHT//2)

lighter = (224,248,208)
light = (136,192,112)
dark = (52,104,86)
darker = (8,24,32)

player_speed = 8
ball_speed = 6

#texty
chiller = pygame.font.SysFont("Chiller",45)

number_3 = chiller.render("3",False,dark)
number_2 = chiller.render("2",False,dark)
number_1 = chiller.render("1",False,dark)
number_rect = number_3.get_rect()
number_rect.center = CENTER

restart_0 = chiller.render("RESTART",False,light)
restart_1 = chiller.render("¤RESTART¤",False,lighter)
restart_0_rect = restart_0.get_rect()
restart_0_rect.center = (WIDTH//2,2*HEIGHT_2//4)
restart_1_rect = restart_1.get_rect()
restart_1_rect.center = (WIDTH//2-3,2*HEIGHT_2//4)

menu_0 = chiller.render("MENU",False,light)
menu_1 = chiller.render("¤MENU¤",False,lighter)
menu_0_rect = menu_0.get_rect()
menu_0_rect.center = (WIDTH//2,3*HEIGHT_2//4)
menu_1_rect = menu_1.get_rect()
menu_1_rect.center = (WIDTH//2,3*HEIGHT_2//4)

menu_title = chiller.render("CHOOSE YOUR GAMEMODE",False,light)
menu_title_rect = menu_title.get_rect()
menu_title_rect.center = (WIDTH//2,HEIGHT_2//5)

four_players_0 = chiller.render("four players",False,light)
four_players_1 = chiller.render("¤four players¤",False,lighter)
four_players_0_rect = four_players_0.get_rect()
four_players_1_rect = four_players_1.get_rect()
four_players_0_rect.center = (WIDTH//2,2.5*HEIGHT_2//4)
four_players_1_rect.center = (WIDTH//2+1,2.5*HEIGHT_2//4)

three_players_0 = chiller.render("three players",False,light)
three_players_1 = chiller.render("¤three players¤",False,lighter)
three_players_0_rect = three_players_0.get_rect()
three_players_1_rect = three_players_1.get_rect()
three_players_0_rect.center = (WIDTH//2,2*HEIGHT_2//4)
three_players_1_rect.center = (WIDTH//2+1,2*HEIGHT_2//4)


#horizontální zdi
class wall(pygame.sprite.Sprite):
    def __init__(self,start,width,height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill(light)
        self.rect = self.image.get_rect()
        self.rect.topleft = start
        
#šikmé zdi
class wierd_wall():
    def __init__(topleft,topright,bottomright,bottomleft):
        self.A,self.B,self.C,self.D = topleft,topright,bottomright,bottomleft
        self.color = light
    def draw():
        pygame.draw.polygon(screen,self.color,(self.A,self.B,self.C,self.D))

#"branky"
class branka(pygame.sprite.Sprite):
    def __init__(self,pos,width,heigth,_id):
        super().__init__()
        self.color = [255,255,255]
        self.image = pygame.Surface((width,heigth))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.id = _id
    def color_change(self,_id):
        if _id != self.id:
            if _id > self.id: _id -= 1
            self.color[_id] -= 51
        else:
            for color in self.color:
                color -= 51
        self.image.fill(self.color)
    def restart(self):
        self.color = [255,255,255]
        self.image.fill(self.color)
        self.lives = 5
        #self.lives = 1

#míček
class ball():
    def __init__(self,center,r,direction):
        self.r = r
        self.rect_1 = pygame.Rect(center[0]-r,center[1]-r,2*r,2*r)
        self.rect_2 = pygame.Rect(center[0]-(r**2/2)**0.5,center[1]-(r**2/2)**0.5,2*((r**2/2)**0.5),2*((r**2/2)**0.5))
        self.dir = direction
        self.id = 2
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
        self.pos = pos
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.rect.y -= player_speed
        if keys[self.down]:
            self.rect.y += player_speed
    def restart(self):
        self.rect.center = (self.pos,HEIGHT//2)
            
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
        self.pos = pos
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.left]:
            self.rect.x -= player_speed
        if keys[self.right]:
            self.rect.x += player_speed
    def restart(self):
        self.rect.center = (WIDTH//2,self.pos)
        
#levá část trojuhelníku
class left_triangel_player():
    def __init__(topleft,topright,bottomright,bottomleft,up,down,_id):
        self.A,self.B,self.C,self.D = topleft,topright,bottomright,bottomleft
        self.color = light
        self.id = _id
        self.up = up
        self.down = down
    def draw():
        pygame.draw.polygon(screen,self.color,(self.A,self.B,self.C,self.D))
        