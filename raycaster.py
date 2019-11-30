
import pygame

WIN_W = 1280
WIN_H = 720

SCR_W = 320
SCR_H = 180

WALLSIZE = 64

pygame.display.init()
window = pygame.display.set_mode((WIN_W, WIN_H))

screen = pygame.Surface((SCR_W, SCR_H))

RENDER_RAYCASTING = True


FOV = 80

px = 4 * WALLSIZE
py = 4 * WALLSIZE

viewangle = 90


level = ['########',
         '#      #',
         '# X  X #',
         '# X  X #',
         '# X  X #',
         '# XXXX #',
         '#      #',
         '########',
         ]


def renderRaycasting():
    pass


def renderResult():
    pass


def render():
    renderResult()

    if RENDER_RAYCASTING:
        renderRaycasting()        

    pygame.transform.scale(screen, (WIN_W, WIN_H), window)
    pygame.display.flip()
    

def controls():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                
    return True


running = True

while running:
    render()
    running = controls()
    
    
pygame.quit()


