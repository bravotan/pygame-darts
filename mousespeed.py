#!/usr/bin/env python

import pygame
from pygame.locals import *
import math
import time

pygame.init()
scr = pygame.display.set_mode((600, 600))
pygame.display.set_caption('mousespeed test')
pygame.mouse.set_visible(1)

bg = pygame.Surface(scr.get_size())
bg = bg.convert()
bg.fill((255, 255, 255))
scr.blit(bg, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

def initial_velocity(start_pos, end_pos, start_t, end_t):
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    takentime = end_t - start_t
    if takentime <= 0:
        return 0
    return math.sqrt((start_x-end_x)**2+(start_y-end_y)**2) / takentime

class VZone:
    st_width = 100, 60, 30 #straight zone width
    
    def __init__(self, pos):
        self.pos = (pos[0] - self.st_width[0]/2, 0)
    def draw(self, surface, height):
        color = 60, 0, 0
        pygame.draw.rect(surface, color, ((0, 0), (self.st_width[0], height)))
        color = 128, 0, 0
        pygame.draw.rect(surface, color, (((self.st_width[0] - self.st_width[1])/2, 0), (self.st_width[1], height)))
        color = 255, 0, 0
        pygame.draw.rect(surface, color, (((self.st_width[0] - self.st_width[2])/2, 0), (self.st_width[2], height)))

class Dart:
    def through:
        

def main():
    
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                start_t = time.time()
                vz = VZone(start_pos)
                vz.draw(bg, scr.get_height())
                scr.blit(bg, vz.pos)
            if event.type == MOUSEBUTTONUP:
                end_pos = pygame.mouse.get_pos()
                end_t = time.time()
                print initial_velocity(start_pos, end_pos, start_t, end_t)
                bg.fill((255, 255, 255))
                scr.blit(bg, (0, 0))
            
        pygame.display.flip()

if __name__ == '__main__':
    main()
