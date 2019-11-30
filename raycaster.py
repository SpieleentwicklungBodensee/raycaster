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
pxdir = 0
pydir = 0


level = ['################',
         '#       #      #',
         '#  X X  # #### #',
         '# X X X # #    #',
         '# X   X # #### #',
         '#  X X  #      #',
         '#   X   #### ###',
         '#              #',
         '################',
        ]
         
LEV_W = len(level[0])
LEV_H = len(level)

WALLCOLORS = {'#': (64, 64, 64),
              'X': (96, 64, 32),
              }
              
BRIGHTCOLORS = {'#': (80, 80, 80),
                'X': (112, 80, 48),
                }
                
TEXTURES = {'#': (pygame.image.load('textures/ironwall.png'), pygame.image.load('textures/ironwall-dark.png')),
            'X': (pygame.image.load('textures/wafflewall.png'), pygame.image.load('textures/wafflewall-dark.png')),
            }

rays = []


def raycast():
    global rays
    rays = []
    
    STEP = FOV / SCR_W    
    
    # 0 -> -NEARSIZE_H
    # 160.5 -> 0
    # 320 -> +NEARSIZE_H

    NEARSIZE_H = math.tan(math.radians(FOV/2))
    
    for i in range(SCR_W):
        
        n = ((i + 0.5) / SCR_W * 2 -1) * NEARSIZE_H
        a = math.atan(n) + math.radians(viewangle)

        # find box (simple version)
        
        found = False
        bright = False
        steps = 1
        
        while not found:
            newx = math.cos(a) * steps + px
            newy = math.sin(a) * steps + py
            steps += 1
            
            t = level[int(newy / WALLSIZE)][int(newx / WALLSIZE)]
            
            if t == '#' or t == 'X':
                found = True
                
                if abs((newx % WALLSIZE) - 32) > abs((newy % WALLSIZE) - 32):
                    bright = True
                
        rays.append((math.degrees(a), steps, t, bright, newx, newy))
        

def renderRaycasting():
    for y in range(LEV_H):
        for x in range(LEV_W):
            t = level[y][x]
            tilerect = (x * TILESIZE, y * TILESIZE, TILESIZE -1, TILESIZE -1)
            
            if t != ' ':
                pygame.draw.rect(screen, WALLCOLORS[t], tilerect, 0)
                
    pygame.draw.rect(screen, (255, 0, 0), (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE, 2, 2))
    
    for angle, steps, t, bright, newx, newy in rays:
        p1 = (px / WALLSIZE * TILESIZE, py / WALLSIZE * TILESIZE)
        p2 = (math.cos(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[0], math.sin(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[1])
        
        pygame.draw.line(screen, (0, 255, 0), p1, p2)


def renderResult():
    strip = pygame.Surface((1, WALLSIZE))
    
    for x in range(SCR_W):
        
        angle, steps, t, bright, newx, newy = rays[x]
        
        steps *= math.cos(math.radians(angle - viewangle))
        
        default_lineheight = SCR_H * 0.75 
        lineheight = WALLSIZE / steps * default_lineheight
        
        top = (x, SCR_H / 2 - lineheight / 2)
        bottom = (x, SCR_H / 2 + lineheight / 2)
        
        texture = TEXTURES[t][0 if bright else 1]
        strip.blit(texture, (-(newx % WALLSIZE) if not bright else -(newy % WALLSIZE), 0))
        
        texo = (-(newx % WALLSIZE) if not bright else -(newy % WALLSIZE))
        
        #strip = pygame.Surface((20,20))
        scaledstrip = pygame.transform.scale(strip, (1, int(lineheight)))
        screen.blit(scaledstrip, (x, top[1]))
        #pygame.transform.scale(strip, (x, top[1], 1, bottom[1] - top[1]), screen)
        
        #pygame.draw.line(screen, (255,0,0), (x, 0),(x, int(abs(texo))))
        
        #if bright:
        #    pygame.draw.line(screen, BRIGHTCOLORS[t], top, bottom)
        #else:
        #    pygame.draw.line(screen, WALLCOLORS[t], top, bottom)            


def render():
    screen.fill((128, 168, 192))
    screen.fill((64, 128, 64), rect=(0, SCR_H / 2, SCR_W, SCR_H / 2))
    
    renderResult()

    if RENDER_RAYCASTING:
        renderRaycasting()        

    pygame.transform.scale(screen, (WIN_W, WIN_H), window)
    pygame.display.flip()
    

def controls():
    global viewangle, pxdir, pydir, px, py

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return False
                
            if e.key == pygame.K_a:
                pxdir = -1
                
            if e.key == pygame.K_d:
                pxdir = 1
                
            if e.key == pygame.K_w:
                pydir = 1
                
            if e.key == pygame.K_s:
                pydir = -1

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                if pxdir < 0:
                    pxdir = 0
                
            if e.key == pygame.K_d:
                if pxdir > 0:
                    pxdir = 0
                    
            if e.key == pygame.K_w:
                if pydir > 0:
                    pydir = 0
                
            if e.key == pygame.K_s:
                if pydir < 0:
                    pydir = 0
    
        if e.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_rel()
            
            viewangle += mx
    
    newx = math.cos(math.radians(viewangle)) * pydir - math.sin(math.radians(viewangle)) * pxdir + px
    newy = math.sin(math.radians(viewangle)) * pydir + math.cos(math.radians(viewangle)) * pxdir + py
    
    px = newx
    py = newy
                
    return True


running = True

while running:
    raycast()
    render()
    running = controls()
    
    
pygame.quit()


