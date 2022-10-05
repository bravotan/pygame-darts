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


class Board(pygame.sprite.Sprite):

    image_fn = 'dartsboard.png'
    points = 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.image_fn).convert_alpha()
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

    def getpoint(self, pos):
        angle_p = 2 * math.pi / 20
        x, y = pos
        x_distance = self.center_x - x
        y_distance = self.center_y - y
        angle = math.atan2(y_distance, x_distance)
        distance = math.sqrt(x_distance**2 + y_distance**2)
        # OutBoard
        if distance > 170:
            return 0
        # Inner BULL
        if distance < 12.7 / 2:
            return 50
        # Outer BULL
        if distance < 31.8 / 2:
            return 25
        stdpoint = self.points[int(angle / angle_p + 10.5)]
        # Triple ring
        if 99 <= distance <= 107:
            return stdpoint * 3
        # Double ring
        if 162 <= distance <= 170:
            return stdpoint * 2
        return stdpoint


def main():
    screct = scr.get_rect()

    board = Board((90, 90))
    allsprites = pygame.sprite.RenderPlain(board)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                print(board.getpoint(pygame.mouse.get_pos()))

        scr.blit(bg, (0, 0))
        allsprites.draw(scr)
        pygame.display.flip()


if __name__ == '__main__':
    main()
