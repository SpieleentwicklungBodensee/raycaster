import math
import pygame

WIN_W = 1280
WIN_H = 720

SCR_W = 320
SCR_H = 180

WALLSIZE = 64   # "physical" size of the wall
TILESIZE = 8   # size of a wall tile when rendering map

pygame.display.init()
window = pygame.display.set_mode((WIN_W, WIN_H))

screen = pygame.Surface((SCR_W, SCR_H))

RENDER_RAYCASTING = True


FOV = 80.0

px = 4 * WALLSIZE
py = 4 * WALLSIZE

viewangle = 0
pdir = 0


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

WALLCOLORS = {'#': (40, 40, 40),
              'X': (120, 120, 120),
              }


rays = []


def raycast():
    global rays
    rays = []
    
    STEP = FOV / SCR_W    
    
    for i in range(SCR_W):
        angle = viewangle - FOV/2 + (STEP * i)
        angle %= 360

        # find box (simple version)
        
        dotx = px
        doty = py
        
        found = False
        steps = 1
        
        a = math.radians(angle)
        
        while not found:
            newx = math.cos(a) * steps + dotx
            newy = math.sin(a) * steps + doty
            steps += 1
            
            t = level[int(newy / WALLSIZE)][int(newx / WALLSIZE)]
            
            if t == '#' or t == 'X':
                found = True
                
        rays.append((angle, steps, t))
        

def renderRaycasting():
    for y in range(LEV_H):
        for x in range(LEV_W):
            t = level[y][x]
            tilerect = (x * TILESIZE, y * TILESIZE, TILESIZE -1, TILESIZE -1)
            
            if t != ' ':
                pygame.draw.rect(screen, WALLCOLORS[t], tilerect, 0)
                
    pygame.draw.rect(screen, (255, 0, 0), (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE, 2, 2))
    
    for angle, steps, t in rays:
        p1 = (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE)
        p2 = (math.cos(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[0], math.sin(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[1])
        
        pygame.draw.line(screen, (0, 255, 0), p1, p2)


def renderResult():
    for x in range(SCR_W):
        angle, steps, t = rays[x]
        
        steps *= math.cos(math.radians(angle - viewangle))
        
        default_lineheight = SCR_H * 0.75 
        lineheight = WALLSIZE / steps * default_lineheight
        
        top = (x, SCR_H / 2 - lineheight / 2)
        bottom = (x, SCR_H / 2 + lineheight / 2)
        
        pygame.draw.line(screen, WALLCOLORS[t], top, bottom)


def render():
    screen.fill((192, 192, 192))

    renderResult()

    if RENDER_RAYCASTING:
        renderRaycasting()        

    pygame.transform.scale(screen, (WIN_W, WIN_H), window)
    pygame.display.flip()
    

def controls():
    global viewangle, pdir

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False
                
            if e.key == pygame.K_LEFT:
                pdir = -1
                
            if e.key == pygame.K_RIGHT:
                pdir = 1

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                if pdir < 0:
                    pdir = 0
                
            if e.key == pygame.K_RIGHT:
                if pdir > 0:
                    pdir = 0
    
    viewangle += pdir * 1
                
    return True


running = True

while running:
    raycast()
    render()
    running = controls()
    
    
pygame.quit()


