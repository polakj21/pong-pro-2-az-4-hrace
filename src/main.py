import pygame,sys
from sprites import *
pygame.init()

#určení proměných
pygame.display.set_caption("ᛈᛟᚾᚷ᛬ᛈᚱᛟ᛬ᚲᛉᛏᛁᚱᛉᛁ᛬ᚺᚱᚨᚨᚲᛉᛖ")
clock = pygame.time.Clock()
player_distance = 70
state = "menu"
new_dir = None
countdown_time = 180

ball_timeout = 0
timeout = 6
change_vector = pygame.math.Vector2(0.15,-0.15)

sets_4 = [[ver_player(player_distance,25,100,pygame.K_w,pygame.K_s,0),branka((20,83),20,HEIGHT-(82*2),0),wall((0,83),83,HEIGHT-(82*2)),True],
        [hor_player(player_distance,100,25,pygame.K_KP4,pygame.K_KP6,1),branka((83,20),WIDTH-(82*2),20,1),wall((83,0),WIDTH-(82*2),83),True],
        [ver_player(WIDTH-player_distance,25,100,pygame.K_UP,pygame.K_DOWN,2),branka((WIDTH-40,83),20,HEIGHT-(82*2),2),wall((WIDTH-82,83),83,HEIGHT-(82*2)),True],
        [hor_player(HEIGHT-player_distance,100,25,pygame.K_g,pygame.K_j,3),branka((83,HEIGHT-40),WIDTH-(82*2),20,3),wall((83,HEIGHT-82),WIDTH-(82*2),83),True]]

sets_3 = [[hor_player(HEIGHT_3-player_distance,100,25,pygame.K_LEFT,pygame.K_RIGHT,1),branka((83,HEIGHT_3-40),WIDTH-(82*2),20,1),wall((83,HEIGHT_3-82),WIDTH-(82*2),83),True],
          [right_triangel_player(pygame.math.Vector2(WIDTH-68,HEIGHT_3-82),pygame.K_KP8,pygame.K_KP2,2),right_triangel_branka(),right_triangel_wall(pygame.math.Vector2(80,60),82,60),True],
          [left_triangel_player(pygame.math.Vector2(68,HEIGHT_3-82),pygame.K_w,pygame.K_s,0),right_triangel_branka(),right_triangel_wall(pygame.math.Vector2(80,60),82,60),True]]

#vyvolání spriteů
walls = pygame.sprite.Group()
players = pygame.sprite.Group()
branky = pygame.sprite.Group()

players_s,walls_s,branky_s = [],[],[]

def vyvolání_4():
    global walls,players,branky
    walls = pygame.sprite.Group(wall((0,0),83,83),wall((0,HEIGHT-82),83,83),wall((WIDTH-82,0),83,83),wall((WIDTH-82,HEIGHT-82),83,83))
    players = pygame.sprite.Group()
    branky = pygame.sprite.Group()
    for option in sets_4:
        if option[3]:
            players.add(option[0])
            branky.add(option[1])
        else:
            walls.add(option[2])
            
def vyvolání_3():
    global walls,players,branky,players_s,walls_s
    walls = pygame.sprite.Group(wall((WIDTH-82,HEIGHT_3-82),83,83),wall((0,HEIGHT_3-82),83,83),wall((WIDTH//2-21,42),41,40))
    players = pygame.sprite.Group()
    branky = pygame.sprite.Group()
    players_s = []
    walls_s = [right_triangel_wall((WIDTH-82,HEIGHT_3-82),100,50),left_triangel_wall((82,HEIGHT_3-82),100,50),
               right_triangel_wall((WIDTH//2+20,81),200,-100),left_triangel_wall((WIDTH//2-20,81),200,-100)]
    branky_s = []
    for option_ind,option in enumerate(sets_3):
        if option_ind == 0:
            if option[3]:
                players.add(option[0])
                branky.add(option[1])
            else:
                walls.add(option[2])
        else:
            if option[3]:
                players_s.append(option[0])
                branky_s.append(option[1])
            else:
                walls_s.append(option[2])

ball_dir = pygame.math.Vector2(1,0)
ball = ball((CENTER),20,ball_dir.normalize())

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
            if wall.rect.collidepoint(ball.rect_1.midtop):
                ball.rect_1.top = wall.rect.bottom
                ball.rect_2.center = ball.rect_1.center
            else:
                ball.rect_1.bottom = wall.rect.top
                ball.rect_2.center = ball.rect_1.center
        elif wall.rect.collidepoint(ball.rect_1.midright) or wall.rect.collidepoint(ball.rect_1.midleft):
            ball.dir.x = -ball.dir.x
            ball_timeout = timeout
            if wall.rect.collidepoint(ball.rect_1.midright):
                ball.rect_1.right = wall.rect.left
                ball.rect_2.center = ball.rect_1.center
            else:
                ball.rect_1.left = wall.rect.right
                ball.rect_2.center = ball.rect_1.center
        
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

def ball_x_player_s():
    for player in players_s:
        if player.collide(ball.rect_1.midleft)[0] or player.collide(ball.rect_1.midright)[0]:
            ball.dir.x = -ball.dir.x
            ball_timeout = timeout
            ball.id = player.id
            if player.collide(ball.rect_1.midleft)[0]:
                ball.rect_1.left = int(player.collide(ball.rect_1.midleft)[2])
            else:
                ball.rect_1.right = int(player.collide(ball.rect_1.midright)[1])
            ball.rect_2.center = ball.rect_1.center
                
        elif player.collide(ball.rect_1.midtop)[0] or player.collide(ball.rect_1.midbottom)[0]:
            ball.dir.y = -ball.dir.y
            ball_timeout = timeout
            ball.id = player.id
            if player.collide(ball.rect_1.midtop)[0]:
                ball.rect_1.top = int(player.collide(ball.rect_1.midtop)[4])
            else:
                ball.rect_1.bottom = int(player.collide(ball.rect_1.midbottom)[3])
            ball.rect_2.center = ball.rect_1.center
            
        elif player.collide(ball.rect_2.topleft)[0] or player.collide(ball.rect_2.topright)[0] or player.collide(ball.rect_2.bottomleft)[0] or player.collide(ball.rect_2.bottomright)[0]:
            ball.dir = -ball.dir
            ball_timeout = timeout
            ball.id = player.id
        
def ball_x_walls_s():
    for wall in walls_s:
        if wall.collide(ball.rect_1.midleft)[0] or wall.collide(ball.rect_1.midright)[0]:
            ball.dir.x = -ball.dir.x
            ball_timeout = timeout
            if wall.collide(ball.rect_1.midleft)[0]:
                ball.rect_1.left = int(wall.collide(ball.rect_1.midleft)[2])
            else:
                ball.rect_1.right = int(wall.collide(ball.rect_1.midright)[1])
            ball.rect_2.center = ball.rect_1.center
                
        elif wall.collide(ball.rect_1.midtop)[0] or wall.collide(ball.rect_1.midbottom)[0]:
            ball.dir.y = -ball.dir.y
            ball_timeout = timeout
            if wall.collide(ball.rect_1.midtop)[0]:
                ball.rect_1.top = int(wall.collide(ball.rect_1.midtop)[4])
            else:
                ball.rect_1.bottom = int(wall.collide(ball.rect_1.midbottom)[3])
            ball.rect_2.center = ball.rect_1.center
            
        elif wall.collide(ball.rect_2.topleft)[0] or wall.collide(ball.rect_2.topright)[0] or wall.collide(ball.rect_2.bottomleft)[0] or wall.collide(ball.rect_2.bottomright)[0]:
            ball.dir = -ball.dir
            ball_timeout = timeout

def ball_x_branky():
    global sets_4,state,new_dir
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
                
            state = "countdown_4"
            ball.rect_1.center = CENTER
            ball.rect_2.center = CENTER
            branka.color_change(ball.id)
            branka.lives -= 1
            
            if branka.lives == 0:
                sets_4[branka.id][3] = False
                vyvolání_4()
                if ball.id == 0 and sets_4[0][3]:
                    new_dir = pygame.math.Vector2(-1,0)
                elif ball.id == 1 and sets_4[1][3]:
                    new_dir = pygame.math.Vector2(0,-1)
                elif ball.id == 2 and sets_4[2][3]:
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
        for player in players_s:
            player.draw()
        for wall in walls_s:
            wall.draw()
        ball.draw()
        screen.blit(number_3,number_rect)
    if time == 120:
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        for player in players_s:
            player.draw()
        for wall in walls_s:
            wall.draw()
        ball.draw()
        screen.blit(number_2,number_rect)
    if time == 60:
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        for player in players_s:
            player.draw()
        for wall in walls_s:
            wall.draw()
        ball.draw()
        screen.blit(number_1,number_rect)
    if time == 0:
        return 180
    else:
        return time-1

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
    
    #menu
    if state == "menu":
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        screen.fill(dark)
        if four_players_0_rect.collidepoint(mouse_pos):
            screen.blit(four_players_1,four_players_1_rect)
            if mouse_pressed[0]:
                for part in sets_4:
                    part[0].restart()
                    part[1].restart()
                    part[3] = True
                state = "countdown_4"
                vyvolání_4()
                screen = pygame.display.set_mode((WIDTH,HEIGHT))
                ball.dir = pygame.math.Vector2(1,0)
                ball.rect_1.center = ball.rect_2.center = CENTER
        else:
            screen.blit(four_players_0,four_players_0_rect)
        if three_players_0_rect.collidepoint(mouse_pos):
            screen.blit(three_players_1,three_players_1_rect)
            if mouse_pressed[0]:
                for part in sets_3:
                    part[0].restart()
                    part[1].restart()
                    part[3] = True
                state = "countdown_3"
                vyvolání_3()
                screen = pygame.display.set_mode((WIDTH,HEIGHT_3))
                ball.dir = pygame.math.Vector2(0,1)
                ball.rect_1.center = ball.rect_2.center = CENTER
        else:
            screen.blit(three_players_0,three_players_0_rect)
        screen.blit(menu_title,menu_title_rect)
    
    #hra pro čtyři hráče
    elif state == "game_4":
        #update
        players.update()
        player_x_walls()
        if ball_timeout <= 0:
            ball_x_walls()
            ball_x_player()
        ball.move()
        ball_x_branky()
        ball_timeout -=1
        if len(players) == 1:
            state = "win_4"
        
        #vykreslení
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        ball.draw()
            
    #hra pro tři hráče
    elif state == "game_3":
        #update
        players.update()
        for player in players_s:
            player.update()
        player_x_walls()
        if ball_timeout <= 0:
            ball_x_walls()
            ball_x_player()
            ball_x_player_s()
            ball_x_walls_s()
        ball.move()
        ball_x_branky()
        ball_timeout -=1
        
        #vykreslení
        screen.fill(darker)
        branky.draw(screen)
        walls.draw(screen)
        players.draw(screen)
        for player in players_s:
            player.draw()
        for wall in walls_s:
            wall.draw()
        
        ball.draw()
            
    #mezera mezi koli
    elif state == "countdown_4":
        countdown_time = countdown(countdown_time)
        if countdown_time == 180:
            state = "game_4"
    
    elif state == "countdown_3":
        countdown_time = countdown(countdown_time)
        if countdown_time == 180:
            state = "game_3"
        
    #vítězná obrazovka
    elif state == "win_4":
        screen = pygame.display.set_mode((WIDTH,HEIGHT_2))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        for player in players:
            win_text = chiller.render("Player "+str(player.id+1)+" has won!",False,light)
        win_rect = win_text.get_rect()
        win_rect.center = (WIDTH//2,HEIGHT_2//4)
        
        screen.fill(dark)
        screen.blit(win_text,win_rect)
        if restart_0_rect.collidepoint(mouse_pos):
            screen.blit(restart_1,restart_1_rect)
            if mouse_pressed[0]:
                for part in sets_4:
                    part[0].restart()
                    part[1].restart()
                    part[3] = True
                state = "countdown_4"
                screen = pygame.display.set_mode((WIDTH,HEIGHT))
                ball.dir = pygame.math.Vector2(1,0)
                ball.rect_1.center = ball.rect_2.center = CENTER
                
        else:
            screen.blit(restart_0,restart_0_rect)
        if menu_0_rect.collidepoint(mouse_pos):
            screen.blit(menu_1,menu_1_rect)
            if mouse_pressed[0]:
                state = "menu"
        else:
            screen.blit(menu_0,menu_0_rect)
        
    pygame.display.update()
    clock.tick(60)