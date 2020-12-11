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

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        pygame.display.flip()

if __name__ == '__main__':
    main()
