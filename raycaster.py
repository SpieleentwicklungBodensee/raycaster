import math
import pygame

WIN_W = 1920
WIN_H = 1080

SCR_W = 320
SCR_H = 180

WALLSIZE = 64   # "physical" size of the wall
TILESIZE = 8   # size of a wall tile when rendering map

pygame.display.init()
window = pygame.display.set_mode((WIN_W, WIN_H), pygame.FULLSCREEN)

screen = pygame.Surface((SCR_W, SCR_H))

SHOW_MAP = True


FOV = 80.0

px = 4 * WALLSIZE
py = 1.5 * WALLSIZE

viewangle = 0
pxdir = 0
pydir = 0


level = ['####################',
         '#           #      #',
         '#  XX XX    # #### #',
         '# X     X   # #    #',
         '# X  X  X   # X##X #',
         '#  X   X    #      #',
         '#   X X     ##### ##',
         '#    X      X   X  #',
         '#             X    #',
         '####################',
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

        dx, dy = math.cos(a), math.sin(a)
        bx, by = int(px / WALLSIZE), int(py / WALLSIZE)
        if dx >= 0:
            bx += 1
        if dy >= 0:
            by += 1
        dbx = -1 if dx < 0 else 1
        dby = -1 if dy < 0 else 1

        if bx * WALLSIZE == px:
            bx += dbx
        if by * WALLSIZE == py:
            by += dby

        l = 0.0
        while True:
            lx = (bx * WALLSIZE - px) / dx
            ly = (by * WALLSIZE - py) / dy

            if lx < ly:
                l = lx
                nx = bx if dx >= 0 else bx - 1
                ny = int((py + dy * l) / WALLSIZE)
                bx += dbx
            else:
                l = ly
                nx = int((px + dx * l) / WALLSIZE)
                ny = by if dy >= 0 else by - 1
                by += dby

            t = level[ny][nx]
            if t == '#' or t == 'X':
                break

        newx = px + dx * l
        newy = py + dy * l
        
        if abs((newx % WALLSIZE) - 32) > abs((newy % WALLSIZE) - 32):
            bright = True

        rays.append((math.degrees(a), max(l, 0.5), t, bright, newx, newy))
        

def renderRaycasting():
    for y in range(LEV_H):
        for x in range(LEV_W):
            t = level[y][x]
            tilerect = (x * TILESIZE, y * TILESIZE, TILESIZE -1, TILESIZE -1)
            
            if t != ' ':
                pygame.draw.rect(screen, WALLCOLORS[t], tilerect, 0)
                
    pygame.draw.rect(screen, (255, 0, 0), (int(px / WALLSIZE * TILESIZE), int(py / WALLSIZE * TILESIZE), 2, 2))
    
    for angle, steps, t, bright, newx, newy in rays:
        p1 = (int(px / WALLSIZE * TILESIZE), int(py / WALLSIZE * TILESIZE))
        p2 = (int(math.cos(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[0]), int(math.sin(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[1]))
        
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
        strip.blit(texture, (-(int(newx % WALLSIZE)) if not bright else -(int(newy % WALLSIZE)), 0))
        
        texo = (-(newx % WALLSIZE) if not bright else -(newy % WALLSIZE))
        
        #strip = pygame.Surface((20,20))
        scaledstrip = pygame.transform.scale(strip, (1, int(lineheight)))
        screen.blit(scaledstrip, (x, int(top[1])))
        #pygame.transform.scale(strip, (x, top[1], 1, bottom[1] - top[1]), screen)
        
        #pygame.draw.line(screen, (255,0,0), (x, 0),(x, int(abs(texo))))
        
        #if bright:
        #    pygame.draw.line(screen, BRIGHTCOLORS[t], top, bottom)
        #else:
        #    pygame.draw.line(screen, WALLCOLORS[t], top, bottom)            


def render():
    screen.fill((128, 168, 192))
    screen.fill((64, 128, 64), rect=(0, int(SCR_H / 2), int(SCR_W), int(SCR_H / 2)))
    
    renderResult()

    if SHOW_MAP:
        renderRaycasting()        

    pygame.transform.scale(screen, (WIN_W, WIN_H), window)
    pygame.display.flip()
    

def controls():
    global viewangle, pxdir, pydir, px, py, SHOW_MAP

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
                
            if e.key == pygame.K_F12:
                SHOW_MAP = not SHOW_MAP

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
    

    if level[int(py/WALLSIZE)][int(newx/WALLSIZE)] == " ":
        px = newx
    if level[int(newy/WALLSIZE)][int(px/WALLSIZE)] == " ":
        py = newy
                
    return True


running = True

while running:
    raycast()
    render()
    running = controls()
    
    
pygame.quit()


