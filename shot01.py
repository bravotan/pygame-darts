#!/usr/bin/env python

import pygame
from pygame.locals import *
import math
import time


pygame.init()
scr = pygame.display.set_mode((600, 600))
pygame.display.set_caption('shot test')
pygame.mouse.set_visible(1)

bg = pygame.Surface(scr.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))
scr.blit(bg, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()


class Bullet:
    speed = 10
    r = 10
    fgcolor = Color('red')
    bgcolor = Color('white')
    def __init__(self, ini_pos, target_pos):
        ini_x, ini_y = ini_pos
        self.pos = ini_pos
        target_x, target_y = target_pos
        rad = math.atan2(target_y - ini_y, target_x - ini_x)
        self.x_move = math.cos(rad) * self.speed
        self.y_move = math.sin(rad) * self.speed
        # calculate center position of bullet.
        self.center = ini_pos[0] - self.r, ini_pos[1] - self.r
        # create surface.
        self.surface = pygame.Surface((self.r * 2, self.r * 2))
        self.surface.convert()
        self.surface.fill(self.bgcolor)
        self.surface.set_colorkey(self.bgcolor)
        self.rect = pygame.draw.circle(self.surface, self.fgcolor, (self.r, self.r), self.r)

    def move(self):
        x, y = self.center
        self.center = (x, y - self.speed)


def main():
    bullets = []
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                sp_center = start_pos[0]-50, start_pos[1]-50
                start_t = time.time()

                bullets.append(Bullet(start_pos, (0,0)))

            if event.type == MOUSEBUTTONUP:
                end_pos = pygame.mouse.get_pos()
                end_t = time.time()

        scr.blit(bg, (0, 0))
        for i, bullet in enumerate(bullets):
            bullet.move()
            if bullet.center[1] < 0:
                del bullets[i]
                continue
            scr.blit(bullet.surface, bullet.center)

        pygame.display.flip()


if __name__ == '__main__':
    main()
