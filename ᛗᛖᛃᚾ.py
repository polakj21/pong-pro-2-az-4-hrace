import pygame,sys
from _ᛋᛈᚱᚨᛃᛏᛋ import *
pygame.init()

#určení proměných
pygame.display.set_caption("ᛈᛟᚾᚷ᛬ᛈᚱᛟ᛬ᚲᛉᛏᛁᚱᛉᛁ᛬ᚺᚱᚨᚨᚲᛉᛖ")
clock = pygame.time.Clock()

#vyvolání spriteů
walls = pygame.sprite.Group(wall((0,0),WIDTH,60),wall((0,HEIGHT-60),WIDTH,60))
players = pygame.sprite.Group(ver_player(95,25,80,pygame.K_w,pygame.K_s),ver_player(WIDTH-95,25,80,pygame.K_UP,pygame.K_DOWN))

#koize
def player_x_walls():
    for wall in walls:
        for player in players:
            if wall.rect.collidepoint(player.rect.midtop):
                player.rect.top = wall.rect.bottom
            elif wall.rect.collidepoint(player.rect.midbottom):
                player.rect.bottom = wall.rect.top
            
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
    
    pygame.display.update()
    clock.tick(60)
