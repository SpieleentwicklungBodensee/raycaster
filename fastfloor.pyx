import pygame
import math
cimport cython
import numpy as np
cimport numpy as np

cdef class FloorRenderer:
    cdef object screen
    cdef object level

    cdef int WALLSIZE
    cdef float NEARSIZE_H

    cdef int SCR_W
    cdef int SCR_H

    cdef int LEV_W
    cdef int LEV_H
    cdef object TEXTURES

    def __init__(self, screen, WALLSIZE, FOV, level, TEXTURES):
        self.screen = screen

        self.WALLSIZE = WALLSIZE
        self.NEARSIZE_H = math.tan(math.radians(FOV / 2))

        self.SCR_W = screen.get_width()
        self.SCR_H = screen.get_height()

        self.LEV_W = len(level[0])
        self.LEV_H = len(level)

        self.TEXTURES = np.zeros([len(TEXTURES), 64, 64], dtype=np.int32)
        mapping = []
        for name, tex in TEXTURES.items():
            if type(tex) is tuple:
                tex = tex[0]

            array = pygame.surfarray.array2d(tex.convert(screen.get_masks()))
            self.TEXTURES[len(mapping)] = array
            mapping.append(name)

        self.level = np.zeros([self.LEV_W, self.LEV_H], dtype=np.int32)
        for x in range(self.LEV_W):
            for y in range(self.LEV_H):
                try:
                    self.level[x, y] = mapping.index(level[y][x])
                except ValueError:
                    self.level[x, y] = -1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def renderFloor(self, float px, float py, float viewangle):
        cdef np.ndarray[np.int32_t, ndim=2] level
        cdef np.ndarray[np.int32_t, ndim=3] TEXTURES
        cdef np.ndarray[np.uint32_t, ndim=2] screenArray
        cdef float rs, rc
        cdef int y, scr_h_half
        cdef float ty, d, x0, y0, x1, y1, rate, xi, yi
        cdef int x, lx, ly, ix, iy, tile, c

        level = self.level
        TEXTURES = self.TEXTURES
        screenArray = pygame.surfarray.pixels2d(self.screen)

        r = math.radians(viewangle)
        rs = math.sin(r)
        rc = math.cos(r)

        scr_h_half=int(self.SCR_H/2)
        for y in range(scr_h_half):

            ty = (y + 0.5) / scr_h_half
            d = self.WALLSIZE / ty
            x0 = d
            y0 = -self.NEARSIZE_H * d

            x1 = d
            y1 = self.NEARSIZE_H * d

            # floor global
            x0,y0 = rc*x0 - rs*y0 + px, rs*x0 + rc*y0 + py
            x1,y1 = rc*x1 - rs*y1 + px, rs*x1 + rc*y1 + py

            for x in range(self.SCR_W):
                # floor global interpolated
                rate=(x + 0.5)/self.SCR_W
                xi=x0+(x1-x0)*rate
                yi=y0+(y1-y0)*rate

                lx, ly = int(xi / self.WALLSIZE), int(yi / self.WALLSIZE)

                if ly >= self.LEV_H or lx >= self.LEV_W or ly < 0 or lx < 0:
                    continue

                tile = level[lx, ly]

                if tile != -1:
                    ix, iy = int(xi), int(yi)

                    c = TEXTURES[tile, ix % self.WALLSIZE, iy % self.WALLSIZE]
                    screenArray[x, y+scr_h_half] = c

                else:
                    screenArray[x, y+scr_h_half] = 0xff00ff
