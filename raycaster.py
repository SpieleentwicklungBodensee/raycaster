import math
import pygame

WIN_W = 1280
WIN_H = 720

SCR_W = 320
SCR_H = 180

WALLSIZE = 64   # "physical" size of the wall
TILESIZE = 16   # size of a wall tile when rendering map

pygame.display.init()
window = pygame.display.set_mode((WIN_W, WIN_H))

screen = pygame.Surface((SCR_W, SCR_H))

RENDER_RAYCASTING = True


FOV = 80.0

px = 4 * WALLSIZE
py = 4 * WALLSIZE

viewangle = 0


level = ['########',
         '#      #',
         '# X  X #',
         '# X  X #',
         '# X  X #',
         '# XXXX #',
         '#      #',
         '########',
         ]
         
LEV_W = len(level[0])
LEV_H = len(level)


rays = []


def raycast():
    global rays
    STEP = FOV / SCR_W    
    
    for i in range(SCR_W):
        angle = viewangle - FOV/2 + (STEP * i)
        angle %= 360
        rays.append(angle)
        print(angle)
    print('---')


def renderRaycasting():
    for y in range(LEV_H):
        for x in range(LEV_W):
            t = level[y][x]
            tilerect = (x * TILESIZE, y * TILESIZE, TILESIZE -1, TILESIZE -1)
            
            if t == '#':
                pygame.draw.rect(screen, (0, 0, 0), tilerect, 0)
            elif t == 'X':
                pygame.draw.rect(screen, (80, 80, 80), tilerect, 0)
                
    pygame.draw.rect(screen, (255, 0, 0), (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE, 2, 2))
    
    for angle in rays:
        p1 = (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE)
        p2 = (math.cos(math.radians(angle)) * WALLSIZE + p1[0], math.sin(math.radians(angle)) * WALLSIZE + p1[1])
        
        pygame.draw.line(screen, (0, 255, 0), p1, p2)


def renderResult():
    pass


def render():
    screen.fill((192, 192, 192))

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
    raycast()
    render()
    running = controls()
    
    
pygame.quit()


