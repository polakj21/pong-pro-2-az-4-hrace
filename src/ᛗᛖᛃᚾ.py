import pygame,sys
from _ᛋᛈᚱᚨᛃᛏᛋ import *
pygame.init()

#určení proměných
pygame.display.set_caption("ᛈᛟᚾᚷ᛬ᛈᚱᛟ᛬ᚲᛉᛏᛁᚱᛉᛁ᛬ᚺᚱᚨᚨᚲᛉᛖ")
clock = pygame.time.Clock()
player_distance = 70

#vyvolání spriteů
walls = pygame.sprite.Group(wall((0,0),83,83),wall((0,HEIGHT-82),83,83),wall((WIDTH-82,0),83,83),wall((WIDTH-82,HEIGHT-82),83,83))

players = pygame.sprite.Group(ver_player(player_distance,25,80,pygame.K_w,pygame.K_s),ver_player(WIDTH-player_distance,25,80,pygame.K_UP,pygame.K_DOWN),
                              hor_player(player_distance,80,25,pygame.K_KP4,pygame.K_KP6),hor_player(HEIGHT-player_distance,80,25,pygame.K_g,pygame.K_j))

ball = ball((500,400),20,"dir")

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
    
    #update
    players.update()
    player_x_walls()
    
    #vykreslení
    screen.fill(darker)
    walls.draw(screen)
    players.draw(screen)
    ball.draw()
    
    pygame.display.update()
    clock.tick(60)
