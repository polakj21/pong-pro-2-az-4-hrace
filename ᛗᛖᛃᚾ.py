import pygame,sys
from _ᛋᛈᚱᚨᛃᛏᛋ import *
pygame.init()

#určení proměných
pygame.display.set_caption("ᛈᛟᚾᚷ᛬ᛈᚱᛟ᛬ᚲᛉᛏᛁᚱᛉᛁ᛬ᚺᚱᚨᚨᚲᛉᛖ")
clock = pygame.time.Clock()

#vyvolání zdí
walls = pygame.sprite.Group(wall((0,0),width,80),wall((0,height-80),width,80))

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
    
    
    
    #vykreslení
    screen.fill(darker)
    walls.draw(screen)
    
    pygame.display.update()
    clock.tick(60)
