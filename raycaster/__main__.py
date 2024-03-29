import math
import time
import pygame
from os import path

WIN_W = 1280
WIN_H = 720

SCR_W = 320
SCR_H = 180

WALLSIZE = 64   # "physical" size of the wall
TILESIZE = 8   # size of a wall tile when rendering map

# you can choose here
FULLSCREEN = pygame.FULLSCREEN
FULLSCREEN = 0

UPDATE_INTERVAL = 1000 / 100 # updates per second

pygame.display.init()
window = pygame.display.set_mode((WIN_W, WIN_H), FULLSCREEN)
pygame.display.set_caption('raycaster')

screen = pygame.Surface((SCR_W, SCR_H))
tempwin = pygame.Surface((WIN_W, WIN_H))

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

RENDER_MAP = True
RENDER_TEXTURES = True
RENDER_WALLS = True
RENDER_FLOOR = True

FOV = 80.0

px = 4 * WALLSIZE
py = 1.5 * WALLSIZE

viewangle = 0
viewangle_y = 0
pxdir = 0
pydir = 0
speed = 1


level = ['####################',
         '#          o#      #',
         '#  XX XX    # #### #',
         '# X     X   # #s   #',
         '# X  X  X   # X##X #',
         '#  X   X    #      #',
         '#   X X     ##### ##',
         '#    X      X   X  #',
         '# oo          X   o#',
         '# ##################',
         '# #      o       oo#',
         '# #   f       oo  s#',
         '#        o   oooo  #',
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

def load_image(image):
    texture_path = path.join(path.dirname(path.realpath(__file__)), 'textures', image)
    return pygame.image.load(texture_path)

TEXTURES = {'#': (load_image('ironwall.png'), load_image('ironwall-dark.png')),
            'X': (load_image('wafflewall.png'), load_image('wafflewall-dark.png')),
            ' ': load_image('floor.png'),
            'plant': load_image('plant.png'),
            'sign-sbo': load_image('sign-sbo.png'),
            'fountain': (load_image('fountain1.png'),
                         load_image('fountain2.png'),
                         load_image('fountain3.png'),
                         load_image('fountain4.png'),
                         )
            }

objects = []

for y in range(LEV_H):
    for x in range(LEV_W):
        if level[y][x] == 'o':
            objects.append(('plant', x * WALLSIZE, y * WALLSIZE))
        if level[y][x] == 's':
            objects.append(('sign-sbo', x * WALLSIZE, y * WALLSIZE))
        if level[y][x] == 'f':
            objects.append(('fountain', x * WALLSIZE, y * WALLSIZE))

rays = []



def getFloorPixel(x, y):
    lx, ly = int(x / WALLSIZE), int(y / WALLSIZE)

    if ly >= LEV_H or lx >= LEV_W or ly < 0 or lx < 0:
        return (0, 0, 0)

    tile = level[ly][lx]

    if tile in TEXTURES:
        tex = TEXTURES[tile]

        if type(tex) is tuple:
            tex = tex[0]

        return tex.get_at((int(x) % WALLSIZE, int(y) % WALLSIZE))

    else:
        return (255, 0, 255)


def raycast():
    global rays
    rays = []

    # 0 -> -NEARSIZE_H
    # 160.5 -> 0
    # 320 -> +NEARSIZE_H

    NEARSIZE_H = math.tan(math.radians(FOV/2))

    for i in range(SCR_W):

        n = ((i + 0.5) / SCR_W * 2 - 1) * NEARSIZE_H
        a = math.atan(n) + math.radians(viewangle)

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


def renderMap():
    for y in range(LEV_H):
        for x in range(LEV_W):
            t = level[y][x]
            if t not in WALLCOLORS.keys():
                continue

            tilerect = (x * TILESIZE, y * TILESIZE, TILESIZE -1, TILESIZE -1)

            if t != ' ':
                pygame.draw.rect(screen, WALLCOLORS[t], tilerect, 0)

    pygame.draw.rect(screen, (255, 0, 0), (int(px / WALLSIZE * TILESIZE), int(py / WALLSIZE * TILESIZE), 2, 2))

    for angle, steps, t, bright, newx, newy in rays:
        p1 = (int(px / WALLSIZE * TILESIZE), int(py / WALLSIZE * TILESIZE))
        p2 = (int(math.cos(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[0]), int(math.sin(math.radians(angle)) * steps / WALLSIZE * TILESIZE + p1[1]))

        pygame.draw.line(screen, (0, 255, 0), p1, p2)

    for obj in objects:
            objtype, xpos, ypos = obj
            #print(objtype, xpos, ypos)
            pygame.draw.rect(screen, (255, 255, 255), (xpos // TILESIZE, ypos // TILESIZE, TILESIZE -1, TILESIZE -1))
            #print((xpos / TILESIZE, ypos / TILESIZE, TILESIZE -1, TILESIZE -1))


def renderWalls():
    strip = pygame.Surface((1, WALLSIZE), flags=pygame.SRCALPHA)

    for x in range(SCR_W):

        angle, steps, t, bright, newx, newy = rays[x]

        steps *= math.cos(math.radians(angle - viewangle))

        default_lineheight = SCR_H * 1.0
        lineheight = WALLSIZE / steps * default_lineheight

        top = (x, SCR_H / 2 - lineheight / 2)
        bottom = (x, SCR_H / 2 + lineheight / 2)

        if RENDER_TEXTURES:
            texture = TEXTURES[t][0 if bright else 1]
            strip.blit(texture, (-(int(newx % WALLSIZE)) if not bright else -(int(newy % WALLSIZE)), 0))

            scaledstrip = pygame.transform.scale(strip, (1, int(lineheight) + 1))
            screen.blit(scaledstrip, (x, int(top[1])))
        else:
            if bright:
                pygame.draw.line(screen, BRIGHTCOLORS[t], top, bottom)
            else:
                pygame.draw.line(screen, WALLCOLORS[t], top, bottom)

    objectsSorted = []

    for obj in objects:
        objtype, xpos, ypos = obj
        localX = xpos - px + 0.5 * WALLSIZE
        localY = ypos - py + 0.5 * WALLSIZE
        localAngle = math.atan2(localY, localX) - math.radians(viewangle)
        myx = math.tan(localAngle) / math.tan(math.radians(FOV / 2))
        x = (myx * 0.5 + 0.5) * SCR_W
        distance = math.sqrt(localX * localX + localY * localY) * math.cos(localAngle)

        if distance > 0.5:
            objectsSorted.append((distance, objtype, x))

    objectsSorted.sort(reverse=True)

    for distance, objtype, x in objectsSorted:
        lineheight = WALLSIZE / distance * default_lineheight
        texture = TEXTURES[objtype]

        if type(texture) is tuple:
            texture = texture[int(time.time() * 10) % len(texture)]

        fr = int(x - lineheight / 2)
        to = int(x + lineheight / 2)

        for i, xx in enumerate(range(fr, to)):
            if xx < 0 or xx >= SCR_W:
                continue

            angle, steps, t, bright, newx, newy = rays[int(xx)]
            depth = steps * math.cos(math.radians(angle - viewangle))

            if distance < depth:
                top = (xx, SCR_H / 2 - lineheight / 2)
                bottom = (xx, SCR_H / 2 + lineheight / 2)

                tex_x = int(i * (WALLSIZE / lineheight))

                strip.fill((0, 0, 0, 0))
                strip.blit(texture, (-tex_x, 0))

                scaledstrip = pygame.transform.scale(strip, (1, int(lineheight)))
                screen.blit(scaledstrip, (xx, int(top[1])))


def renderFloor():
    NEARSIZE_H = math.tan(math.radians(FOV / 2))

    r = math.radians(viewangle)
    rs = math.sin(r)
    rc = math.cos(r)

    scr_h_half = int(SCR_H / 2)
    for y in range(scr_h_half):

        ty = (y + 0.5) / scr_h_half
        d = WALLSIZE / ty
        x0 = d
        y0 = -NEARSIZE_H * d

        x1 = d
        y1 = NEARSIZE_H * d

        # floor global
        x0, y0 = rc * x0 - rs * y0, rs * x0 + rc * y0
        x1, y1 = rc * x1 - rs * y1, rs * x1 + rc * y1

        x0 += px
        y0 += py
        x1 += px
        y1 += py

        for x in range(SCR_W):
            # floor global interpolated
            rate = (x + 0.5) / SCR_W
            xi = x0 + (x1 - x0) * rate
            yi = y0 + (y1 - y0) * rate

            c = getFloorPixel(xi, yi)
            screen.set_at((x, y + scr_h_half), c)

try:
    import fastfloor
    floorRenderer = fastfloor.FloorRenderer(screen, WALLSIZE, FOV, level, TEXTURES)
    def renderFloor():
        floorRenderer.renderFloor(px, py, viewangle)
except ImportError:
    pass

def render():
    global RENDER_WALLS, RENDER_FLOOR
    screen.fill((128, 168, 192))

    if RENDER_FLOOR:
        renderFloor()
    else:
        screen.fill((64, 128, 64), rect=(0, int(SCR_H / 2), int(SCR_W), int(SCR_H / 2)))

    if RENDER_WALLS:
        renderWalls()

    if RENDER_MAP:
        renderMap()

    pygame.transform.scale(screen, (WIN_W, WIN_H), tempwin)
    window.blit(tempwin, (0, 0))
    pygame.display.flip()


def controls():
    global viewangle, pxdir, pydir, px, py, speed, RENDER_MAP, RENDER_TEXTURES, RENDER_WALLS, RENDER_FLOOR, viewangle_y

    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                if pygame.event.get_grab():
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                else:
                    return False

            if e.key == pygame.K_a:
                pxdir = -1

            if e.key == pygame.K_d:
                pxdir = 1

            if e.key == pygame.K_w:
                pydir = 1

            if e.key == pygame.K_s:
                pydir = -1

            if e.key == pygame.K_LSHIFT:
                speed = 2

            if e.key == pygame.K_F9:
                RENDER_WALLS = not RENDER_WALLS

            if e.key == pygame.K_F10:
                RENDER_FLOOR = not RENDER_FLOOR

            if e.key == pygame.K_F11:
                RENDER_TEXTURES = not RENDER_TEXTURES

            if e.key == pygame.K_F12:
                RENDER_MAP = not RENDER_MAP

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

            if e.key == pygame.K_LSHIFT:
                speed = 1

        if e.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

        if e.type == pygame.MOUSEMOTION and pygame.event.get_grab():
            mx, my = pygame.mouse.get_rel()
            viewangle += mx
            #viewangle_y += my/4

        if e.type == pygame.QUIT:
            return False

    newx = math.cos(math.radians(viewangle)) * pydir * speed - math.sin(math.radians(viewangle)) * pxdir * speed + px
    newy = math.sin(math.radians(viewangle)) * pydir * speed + math.cos(math.radians(viewangle)) * pxdir * speed + py

    if level[int(py / WALLSIZE)][int(newx / WALLSIZE)] == " ":
        px = newx
    if level[int(newy / WALLSIZE)][int(px / WALLSIZE)] == " ":
        py = newy
    return True



running = True
clock = pygame.time.Clock()
move_timer = 0
fpsTime = 0

while running:
    dt = clock.get_time()

    move_timer += dt
    while move_timer >= UPDATE_INTERVAL:
        running = controls()

        if not running:
            break

        move_timer -= UPDATE_INTERVAL

    raycast()
    render()

    fpsTime += dt
    while fpsTime >= 1000:
        pygame.display.set_caption('raycaster %i fps' % clock.get_fps())
        fpsTime = 0

    clock.tick()

pygame.quit()



