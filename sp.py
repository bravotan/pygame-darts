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


class Obj(pygame.sprite.Sprite):

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        FONTNAME = 'GDhighwayJapan-026b1.otf'
        self.font = pygame.font.Font(FONTNAME, 48)
        self.blackX = self.font.render('X', True, (0,0,0))
        self.redX = self.font.render('X', True, (255,0,0))
        self.image = self.blackX
        self.rect = self.image.get_rect()
        self.height, self.width = self.image.get_size()
        self.center_x = self.width / 2.0
        self.center_y = self.height / 2.0
        self.move(pos)

    def move(self, pos):
        x, y = pos
        self.center_x = self.width / 2.0 + x
        self.center_y = self.height / 2.0 + y
        self.rect = self.rect.move(pos)

    def update(self):
        if self.rect.colliderect(pygame.mouse.get_pos(), (0, 0)):
            self.image = self.redX
        else:
            self.image = self.blackX


def main():
    screct = scr.get_rect()

    board = Obj((90, 200))
    allsprites = pygame.sprite.RenderPlain(board)
    while True:
        clock.tick(30)
        event = pygame.event.wait()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return

        scr.blit(bg, (0, 0))
        allsprites.update()
        allsprites.draw(scr)
        pygame.display.flip()


if __name__ == '__main__':
    main()
