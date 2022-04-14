import pygame
pygame.init()

#určení proměných
WIDTH,HEIGHT,HEIGHT_2,HEIGHT_3 = 700,700,449,590
screen = pygame.display.set_mode((WIDTH,HEIGHT_2))
CENTER = (WIDTH//2,HEIGHT//2)

lighter = (224,248,208)
light = (136,192,112)
dark = (52,104,86)
darker = (8,24,32)

player_speed = 8
ball_speed = 6

tg60 = 1.73
tg_60 = -1.73
tg30 = 0.57
tg_30 = -0.57

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
class right_triangel_wall():
    def __init__(self,topleft,width,heigth):
        topleft = pygame.math.Vector2(topleft)
        v = pygame.math.Vector2(-1,0).rotate(60)
        self.v1 = pygame.math.Vector2(-1,0).rotate(150)
        self.a = topleft
        self.b = width*self.v1+topleft
        self.c = self.b - heigth*v
        self.d = self.a - heigth*v
        
        self.q01 = -tg60 * topleft.x + topleft.y
        self.q02 = -tg60 * self.b.x + self.b.y
        self.q11 = -tg_30 * self.b.x + self.b.y
        self.q12 = -tg_30 * self.d.x + self.d.y
    def collide(self,test_point):
        x0 = -(-test_point[1]+self.q02)//tg60
        x1 = -(-test_point[1]+self.q01)//tg60
        y0 = tg_30*test_point[0] + self.q11
        y1 = tg_30*test_point[0] + self.q12
        #print(x0,x1,"--",test_point[0],"\n",y0,y1,"--",test_point[1])
        
        #pygame.draw.polygon(screen,"blue",((x0,test_point[1]),(x1,test_point[1]),(test_point[0],y0),(test_point[0],y1)),width=3)
        
        if x0 >= test_point[0] >= x1 and y0 >= test_point[1] >= y1:
            return True,x0,x1,y0,y1
        else:
            return False,None,None,None,None
    def draw(self):
        pygame.draw.polygon(screen,light,(self.a,self.b,self.c,self.d))

class left_triangel_wall():
    def __init__(self,topright,width,heigth):
        topright = pygame.math.Vector2(topright)
        v = pygame.math.Vector2(-1,0).rotate(120)
        self.v1 = pygame.math.Vector2(-1,0).rotate(30)
        self.a = topright
        self.b = topright+width*self.v1
        self.c = self.b - heigth*v
        self.d = self.a - heigth*v
        
        self.q01 = -tg_60 * topright.x + topright.y
        self.q02 = -tg_60 * self.b.x + self.b.y
        self.q11 = -tg30 * self.b.x + self.b.y
        self.q12 = -tg30 * self.d.x + self.d.y
    def collide(self,test_point):
        x0 = -(-test_point[1]+self.q02)//tg_60
        x1 = -(-test_point[1]+self.q01)//tg_60
        y0 = tg30*test_point[0] + self.q11
        y1 = tg30*test_point[0] + self.q12
        #print(-x0,-x1,"--",test_point[0],"\n",y0,y1,"--",test_point[1])
        
        #pygame.draw.polygon(screen,"red",((x0,test_point[1]),(x1,test_point[1]),(test_point[0],y0),(test_point[0],y1)),width=3)
        
        if x0 <= test_point[0] <= x1 and y0 >= test_point[1] >= y1:
            return True,x0,x1,y0,y1
        else:
            return False,None,None,None,None
    def draw(self):
        pygame.draw.polygon(screen,light,(self.a,self.b,self.c,self.d))

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

class right_triangel_branka():
    def __init__(self):
        pass
    def draw(self):
        pass
    def restart(self):
        pass

#míček
class ball():
    def __init__(self,center,r,direction):
        self.r = r
        self.rect_1 = pygame.Rect(center[0]-r,center[1]-r,2*r,2*r)
        self.rect_2 = pygame.Rect(center[0]-(r**2/2)**0.5,center[1]-(r**2/2)**0.5,2*((r**2/2)**0.5),2*((r**2/2)**0.5))
        self.dir = direction
        self.id = 2
        
        self.rv0 = pygame.math.Vector2(-1,0).rotate(60)
        self.rv1 = self.rv0.rotate(90)
        self.rv2 = self.rv0.rotate(45)
        self.rv3 = self.rv1.rotate(45)
        
        self.ra = self.rect_1.center + self.rv0*self.r
        self.rb = self.rect_1.center + self.rv1*self.r
        self.rc = self.rect_1.center - self.rv0*self.r
        self.rd = self.rect_1.center - self.rv1*self.r
        
        self.re = self.rect_1.center + self.rv2*self.r
        self.rf = self.rect_1.center + self.rv3*self.r
        self.rg = self.rect_1.center - self.rv2*self.r
        self.rh = self.rect_1.center - self.rv3*self.r
        
        self.lv0 = pygame.math.Vector2(-1,0).rotate(120)
        self.lv1 = self.lv0.rotate(90)
        self.lv2 = self.lv0.rotate(45)
        self.lv3 = self.lv1.rotate(45)
        
        self.la = self.rect_1.center + self.lv0*self.r
        self.lb = self.rect_1.center + self.lv1*self.r
        self.lc = self.rect_1.center - self.lv0*self.r
        self.ld = self.rect_1.center - self.lv1*self.r
        
        self.le = self.rect_1.center + self.lv2*self.r
        self.lf = self.rect_1.center + self.lv3*self.r
        self.lg = self.rect_1.center - self.lv2*self.r
        self.lh = self.rect_1.center - self.lv3*self.r
        
    def move(self):
        self.rect_1.center += self.dir*ball_speed
        self.rect_2.center += self.dir*ball_speed
        
        self.ra = self.rect_1.center + self.rv0*self.r
        self.rb = self.rect_1.center + self.rv1*self.r
        self.rc = self.rect_1.center - self.rv0*self.r
        self.rd = self.rect_1.center - self.rv1*self.r
        
        self.re = self.rect_1.center + self.rv2*self.r
        self.rf = self.rect_1.center + self.rv3*self.r
        self.rg = self.rect_1.center - self.rv2*self.r
        self.rh = self.rect_1.center - self.rv3*self.r
        
        self.la = self.rect_1.center + self.lv0*self.r
        self.lb = self.rect_1.center + self.lv1*self.r
        self.lc = self.rect_1.center - self.lv0*self.r
        self.ld = self.rect_1.center - self.lv1*self.r
        
        self.le = self.rect_1.center + self.lv2*self.r
        self.lf = self.rect_1.center + self.lv3*self.r
        self.lg = self.rect_1.center - self.lv2*self.r
        self.lh = self.rect_1.center - self.lv3*self.r
        
    def draw(self):
        pygame.draw.circle(screen,light,self.rect_1.center,self.r)
        #pygame.draw.polygon(screen,"cyan",(self.ra,self.rb,self.rc,self.rd),width = 2)
        #pygame.draw.polygon(screen,"red",(self.re,self.rf,self.rg,self.rh),width = 2)
        #pygame.draw.polygon(screen,"white",(self.la,self.lb,self.lc,self.ld),width = 2)
        #pygame.draw.polygon(screen,"silver",(self.le,self.lf,self.lg,self.lh),width = 2)
        
        #pygame.draw.circle(screen,"red",self.ld,2)

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
class right_triangel_player():
    def __init__(self,center,up,down,_id):
        self.id = _id
        self.down = down
        self.up = up
        self.v = pygame.math.Vector2(-1,0).rotate(60)
        self.center = self.v*246.5+center
        self.restarting = self.center
        
        self.do_up = True
        self.do_down = True
        
        self.v1 = pygame.math.Vector2(-1,0).rotate(150)
        self.q01 = -tg60 * (self.v1*12.5 + self.v*50+self.center).x + (self.v1*12.5 + self.v*50+self.center).y
        self.q02 = -tg60 * (self.v1*(-12.5) + self.v*50+self.center).x + (self.v1*(-12.5) + self.v*50+self.center).y
        self.q11 = -tg_30 * (self.v1*12.5 + self.v*50+self.center).x + (self.v1*12.5 + self.v*50+self.center).y
        self.q12 = -tg_30 * (self.v1*12.5 + self.v*(-50)+self.center).x + (self.v1*12.5 + self.v*(-50)+self.center).y
    def collide(self,test_point):
        x0 = -(-test_point[1]+self.q02)//tg60
        x1 = -(-test_point[1]+self.q01)//tg60
        y0 = tg_30*test_point[0] + self.q11
        y1 = tg_30*test_point[0] + self.q12
        #print(x0,x1,"--",test_point[0],"\n",y0,y1,"--",test_point[1])
        
        #pygame.draw.polygon(screen,"green",((x0,test_point[1]),(x1,test_point[1]),(test_point[0],y0),(test_point[0],y1)),width=3)
        #pygame.draw.circle(screen,"red",(test_point[0],y0),2)
        if x0 <= test_point[0] <= x1 and y0 <= test_point[1] <= y1:
            return True,x0,x1,y0,y1
        else:
            return False,None,None,None,None
    def draw(self):
        center = self.center
        v = self.v
        v1 = self.v1
        top = v*50+center
        bottom = v*(-50)+center
        
        a = v1*12.5 + top
        b = v1*(-12.5) + top
        c = v1*(-12.5) + bottom
        d = v1*12.5 + bottom
        self.q11 = -tg_30 * a.x + a.y
        self.q12 = -tg_30 * d.x + d.y
        
        pygame.draw.polygon(screen,light,(a,b,c,d))
    def update(self):
        keys = pygame.key.get_pressed()
        if self.do_up:
            if keys[self.up]:
                self.center += self.v*player_speed
        if self.do_down:
            if keys[self.down]:
                self.center -= self.v*player_speed
    def restart(self):
        self.center = self.restarting
    
#pravá část trojuhelníku
class left_triangel_player():
    def __init__(self,center,up,down,_id):
        self.id = _id
        self.down = down
        self.up = up
        self.v = pygame.math.Vector2(-1,0).rotate(120)
        #print(self.v)
        self.center = self.v*246.5+center
        self.restarting = self.center
        
        self.do_up = True
        self.do_down = True
        
        self.v1 = pygame.math.Vector2(-1,0).rotate(30)
        self.q01 = -tg_60 * (self.v1*12.5 + self.v*50+self.center).x + (self.v1*12.5 + self.v*50+self.center).y
        self.q02 = -tg_60 * (self.v1*(-12.5) + self.v*50+self.center).x + (self.v1*(-12.5) + self.v*50+self.center).y
        self.q11 = -tg30 * (self.v1*12.5 + self.v*50+self.center).x + (self.v1*12.5 + self.v*50+self.center).y
        self.q12 = -tg30 * (self.v1*12.5 + self.v*(-50)+self.center).x + (self.v1*12.5 + self.v*(-50)+self.center).y
    def collide(self,test_point):
        x0 = -(-test_point[1]+self.q02)//tg_60
        x1 = -(-test_point[1]+self.q01)//tg_60
        y0 = tg30*test_point[0] + self.q11
        y1 = tg30*test_point[0] + self.q12
        #print(x0,x1,"--",test_point[0],"\n",y0,y1,"--",test_point[1])
        
        #pygame.draw.polygon(screen,"yellow",((x0,test_point[1]),(x1,test_point[1]),(test_point[0],y0),(test_point[0],y1)),width=3)
        
        if x1 <= test_point[0] <= x0 and y0 <= test_point[1] <= y1:
            return True,x0,x1,y0,y1
        else:
            return False,None,None,None,None
    def draw(self):
        center = self.center
        v = self.v
        v1 = self.v1
        top = v*50+center
        bottom = v*(-50)+center
        
        a = v1*12.5 + top
        b = v1*(-12.5) + top
        c = v1*(-12.5) + bottom
        d = v1*12.5 + bottom
        
        pygame.draw.polygon(screen,light,(a,b,c,d))
        self.q11 = -tg30 * a.x + a.y
        self.q12 = -tg30 * d.x + d.y
    def update(self):
        keys = pygame.key.get_pressed()
        if self.do_up:
            if keys[self.up]:
                self.center += self.v*player_speed
        if self.do_down:
            if keys[self.down]:
                self.center -= self.v*player_speed
    def restart(self):
        self.center = self.restarting   