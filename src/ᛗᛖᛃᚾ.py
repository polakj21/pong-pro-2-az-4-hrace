import pygame,sys
from _ᛋᛈᚱᚨᛃᛏᛋ import *
pygame.init()

#určení proměných
pygame.display.set_caption("ᛈᛟᚾᚷ᛬ᛈᚱᛟ᛬ᚲᛉᛏᛁᚱᛉᛁ᛬ᚺᚱᚨᚨᚲᛉᛖ")
clock = pygame.time.Clock()
player_distance = 70
ende = True
new_dir = None
countdown_time = 180

ball_timeout = 0
timeout = 9
change_vector = pygame.math.Vector2(0.15,-0.15)

sets = [[ver_player(player_distance,25,100,pygame.K_w,pygame.K_s,0),branka((20,83),20,HEIGHT-(82*2),0),wall((0,83),83,HEIGHT-(82*2)),True],
        [hor_player(player_distance,100,25,pygame.K_KP4,pygame.K_KP6,1),branka((83,20),WIDTH-(82*2),20,1),wall((83,0),WIDTH-(82*2),83),True],
        [ver_player(WIDTH-player_distance,25,100,pygame.K_UP,pygame.K_DOWN,2),branka((WIDTH-40,83),20,HEIGHT-(82*2),2),wall((WIDTH-82,83),83,HEIGHT-(82*2)),True],
        [hor_player(HEIGHT-player_distance,100,25,pygame.K_g,pygame.K_j,3),branka((83,HEIGHT-40),WIDTH-(82*2),20,3),wall((83,HEIGHT-82),WIDTH-(82*2),83),True]]

#vyvolání spriteů
walls = pygame.sprite.Group(wall((0,0),83,83),wall((0,HEIGHT-82),83,83),wall((WIDTH-82,0),83,83),wall((WIDTH-82,HEIGHT-82),83,83))
players = pygame.sprite.Group()
branky = pygame.sprite.Group()

def vyvolání():
    global walls,players,branky
    walls = pygame.sprite.Group(wall((0,0),83,83),wall((0,HEIGHT-82),83,83),wall((WIDTH-82,0),83,83),wall((WIDTH-82,HEIGHT-82),83,83))
    players = pygame.sprite.Group()
    branky = pygame.sprite.Group()
    for option in sets:
        if option[3]:
            players.add(option[0])
            branky.add(option[1])
        else:
            walls.add(option[2])

ball_dir = pygame.math.Vector2(1,0)
ball = ball((CENTER),20,ball_dir.normalize())
vyvolání()

#koize
def player_x_walls():
    for wall in walls:
        for player in players:
            if wall.rect.collidepoint(player.rect.midtop):
                player.rect.top = wall.rect.bottom
            elif wall.rect.collidepoint(player.rect.midbottom):
                player.rect.bottom = wall.rect.top
                
            if wall.rect.collidepoint(player.rect.midleft):
                player.rect.left = wall.rect.right
            elif wall.rect.collidepoint(player.rect.midright):
                player.rect.right = wall.rect.left
                
def ball_x_walls():
    global ball_timeout
    for wall in walls:
        if wall.rect.collidepoint(ball.rect_1.midtop) or wall.rect.collidepoint(ball.rect_1.midbottom):
            ball.dir.y = -ball.dir.y
            ball_timeout = timeout
        elif wall.rect.collidepoint(ball.rect_1.midright) or wall.rect.collidepoint(ball.rect_1.midleft):
            ball.dir.x = -ball.dir.x
            ball_timeout = timeout
        
        elif wall.rect.collidepoint(ball.rect_2.topleft) or wall.rect.collidepoint(ball.rect_2.topright) or wall.rect.collidepoint(ball.rect_2.bottomleft) or wall.rect.collidepoint(ball.rect_2.bottomright):
            ball.dir = -ball.dir

            ball_timeout = timeout
def ball_x_player():
    global ball_timeout
    for player in players:
        if player.rect.collidepoint(ball.rect_1.midtop) or player.rect.collidepoint(ball.rect_1.midbottom):
            ball.dir.y = -ball.dir.y
            ball_timeout = timeout
            ball.id = player.id
            if player.rect.collidepoint(ball.rect_1.midbottom):
                ball.rect_1.bottom = player.rect.top
            else:
                ball.rect_1.top = player.rect.bottom
            ball.rect_2.center = ball.rect_1.center
            
            #odchilka
            if player.rect.center[0] > ball.rect_1.center[0]:
                if player.rect.center[0] - ball.rect_1.center[0] > 10:
                    ball.dir -= change_vector
                if player.rect.center[0] - ball.rect_1.center[0] > 20:
                    ball.dir -= change_vector
                if player.rect.center[0] - ball.rect_1.center[0] > 30:
                    ball.dir -= change_vector
            else:
                if ball.rect_1.center[0] - player.rect.center[0] > 10:
                    ball.dir += change_vector
                if ball.rect_1.center[0] - player.rect.center[0] > 20:
                    ball.dir += change_vector
                if ball.rect_1.center[0] - player.rect.center[0] > 30:
                    ball.dir += change_vector
            ball.dir.normalize_ip()
            
        elif player.rect.collidepoint(ball.rect_1.midright) or player.rect.collidepoint(ball.rect_1.midleft):
            ball.dir.x = -ball.dir.x
            ball_timeout = timeout
            ball.id = player.id
            if player.rect.collidepoint(ball.rect_1.midleft):
                ball.rect_1.left = player.rect.right
            else:
                ball.rect_1.right = player.rect.left
            ball.rect_2.center = ball.rect_1.center
            
            #odchilka
            if player.rect.center[1] > ball.rect_1.center[1]:
                if player.rect.center[1] - ball.rect_1.center[1] > 10:
                    ball.dir += change_vector
                if player.rect.center[1] - ball.rect_1.center[1] > 20:
                    ball.dir += change_vector
                if player.rect.center[1] - ball.rect_1.center[1] > 30:
                    ball.dir += change_vector
            else:
                if ball.rect_1.center[1] - player.rect.center[1] > 10:
                    ball.dir -= change_vector
                if ball.rect_1.center[1] - player.rect.center[1] > 20:
                    ball.dir -= change_vector
                if ball.rect_1.center[0] - player.rect.center[1] > 30:
                    ball.dir -= change_vector
            ball.dir.normalize_ip()
        
        elif player.rect.collidepoint(ball.rect_2.topleft) or player.rect.collidepoint(ball.rect_2.topright) or player.rect.collidepoint(ball.rect_2.bottomleft) or player.rect.collidepoint(ball.rect_2.bottomright):
            ball.dir = -ball.dir
            ball_timeout = timeout
            ball.id = player.id

def ball_x_branky():
    global sets,ende,new_dir
    for branka in branky:
        if branka.rect.colliderect(ball.rect_2):
            if branka.id == 0:
                new_dir = pygame.math.Vector2(-1,0)
            elif branka.id == 1:
                new_dir = pygame.math.Vector2(0,-1)
            elif branka.id == 2:
                new_dir = pygame.math.Vector2(1,0)
            else:
                new_dir = pygame.math.Vector2(0,1)
            
            for player in players:
                player.restart()
                
            ende = True
            ball.rect_1.center = CENTER
            ball.rect_2.center = CENTER
            branka.color_change(ball.id)
            branka.lives -= 1
            
            if branka.lives == 0:
                sets[branka.id][3] = False
                vyvolání()
                if ball.id == 0 and sets[0][3]:
                    new_dir = pygame.math.Vector2(-1,0)
                elif ball.id == 1 and sets[1][3]:
                    new_dir = pygame.math.Vector2(0,-1)
                elif ball.id == 2 and sets[2][3]:
                    new_dir = pygame.math.Vector2(1,0)
                else:
                    new_dir = pygame.math.Vector2(0,1)
                
            ball.dir = new_dir
                

#odpočet na začátku hry
def countdown(time):
    if time == 180:
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        ball.draw()
        screen.blit(number_3,number_rect)
    if time == 120:
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        ball.draw()
        screen.blit(number_2,number_rect)
    if time == 60:
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        ball.draw()
        screen.blit(number_1,number_rect)
    if time == 0:
        return False,180
    else:
        return True,time-1

#main loop
while True:
    #vypnutí
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
        
    if not ende:
        #update
        players.update()
        player_x_walls()
        if ball_timeout <= 0:
            ball_x_walls()
            ball_x_player()
        ball.move()
        ball_x_branky()
        ball_timeout -=1
        
        #vykreslení
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        ball.draw()
    else:
        ende,countdown_time = countdown(countdown_time)
    
    pygame.display.update()
    clock.tick(60)
