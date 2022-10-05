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


class Room:
    wall_distance = 250


class Bullet:
    g = 200
    r = 10
    fgcolor = Color('red')
    bgcolor = Color('white')
    speedrate = 0.01
    vrate = 0.01
    angle_base_len = 150.0
    angle_range = 20.0
    angle_positive_max = 30.0

    def __init__(self, start_pos, end_pos, start_t, end_t):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        takentime = end_t - start_t
        self.discharge_t = end_t
        self.ini_pos = start_pos

        length = math.sqrt((start_x-end_x)**2+(start_y-end_y)**2)
        #print 'l', length
        if length > self.angle_base_len:
            yz_angle = self.angle_range - self.angle_positive_max
        else:
            yz_angle = self.angle_range / self.angle_base_len * length - \
              (self.angle_range - self.angle_positive_max)
        yz_angle *= math.pi / 180
        #print 'YZ:', yz_angle
        xy_angle = math.atan2(end_y - start_y, end_x - start_x)
        #print 'XY:', xy_angle, xy_angle / math.pi * 180

        if length <= 0:
            self.velocity = 0
        else:
            self.velocity = length / takentime * self.speedrate
        self.x_move = math.cos(xy_angle) * self.velocity
        self.y_move = math.sin(-1*math.pi/180) * self.velocity
        self.z = 0
        self.z_move = abs(math.cos(yz_angle) * self.velocity)
        self.sizerate = 1
        self.sizerate_change = self.velocity * self.vrate

        # calculate center position of bullet.
        self.center = start_x, start_y
        self.pos = start_x - self.r, start_y - self.r

        # create and draw surface.
        self.surface = pygame.Surface((self.r * 2, self.r * 2))
        self.surface = self.surface.convert()
        self.surface.fill(self.bgcolor)
        self.surface.set_colorkey(self.bgcolor)
        self.rect = pygame.draw.circle(self.surface, self.fgcolor, (self.r, self.r), self.r)

    def __move_x(self):
        return self.x_move

    def __move_y(self):
        return (self.g*(time.time() - self.discharge_t)**2) / 2 + self.y_move

    def __move_z(self):
        return self.z_move

    def __move_size(self):
        return self.sizerate / (1 + self.sizerate_change)

    def move(self):
        self.sizerate = self.__move_size()
        self.pos = (self.pos[0] + self.__move_x(), self.pos[1] + self.__move_y())
        self.center = (self.center[0] + self.__move_x(), self.center[1] + self.__move_y())
        self.z += self.__move_z()
        self.surface.fill(self.bgcolor)
        r = int(round(self.r * self.sizerate))
        if r < 0:
            return None
        return pygame.draw.circle(self.surface, self.fgcolor, (self.r, self.r), r)

    def get_rect(self):
        return self.surface.get_rect()


def outofrect(pos, rect):
    x, y = pos
    if rect.left > x:
        return True
    if rect.right < x:
        return True
    if rect.top > y:
        return True
    if rect.bottom < y:
        return True
    return False


def main():
    bullets = []
    screct = scr.get_rect()
    room = Room()
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                start_t = time.time()

            if event.type == MOUSEBUTTONUP:
                end_pos = pygame.mouse.get_pos()
                end_t = time.time()
                bullets.append(Bullet(start_pos, end_pos, start_t, end_t))

        scr.blit(bg, (0, 0))
        for i, bullet in enumerate(bullets):
            bullet.move()
            if outofrect(bullet.center, screct):
                del bullets[i]
                continue
            if bullet.z >= room.wall_distance:
                #print bullet.ini_pos[0] -  bullet.center[0], bullet.ini_pos[1] -  bullet.center[1]
                del bullets[i]
                continue
            #print bullet.z
            scr.blit(bullet.surface, bullet.pos)

        pygame.display.flip()


if __name__ == '__main__':
    main()
