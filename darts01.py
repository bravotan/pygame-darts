#!/usr/bin/env python

import pygame
from pygame import color
from pygame.locals import *
import math
import time
import os

pygame.init()
scr = pygame.display.set_mode((640, 480))
pygame.display.set_caption('shot test')
pygame.mouse.set_visible(1)

bg = pygame.image.load('background.jpg').convert()
scr.blit(bg, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

OB = 0
SINGLE = 1
DOUBLE = 2
TRIPLE = 3
BULL = 4
DBULL = 5


class Room:
    wall_distance = 237


class Bullet:
    g = 10
    r = 10
    fgcolor = color.Color('purple')
    bgcolor = color.Color('white')
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
        if length > self.angle_base_len:
            yz_angle = self.angle_range - self.angle_positive_max
        else:
            yz_angle = self.angle_range / self.angle_base_len * length - \
              (self.angle_range - self.angle_positive_max)
        yz_angle *= math.pi / 180
        xy_angle = math.atan2(end_y - start_y, end_x - start_x)

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
        self.surface = pygame.Surface((self.r * 2, self.r * 2)).convert()
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


class BoardShadow(pygame.sprite.Sprite):
    image_fn = './dartsboard-shadow.png'
    def __init__(self, pos=(0, 0)):
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


class Board(pygame.sprite.Sprite):
    image_fn = 'dartsboard.png'
    inbull = 12.7/4.0
    outbull = 31.8/4.0
    triple_inside = 99/2.0
    triple_outside = 107/2.0
    double_inside = 162/2.0
    double_outside = 170/2.0
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
        if distance > self.double_outside:
            return 0, OB
        # Inner BULL
        if distance < self.inbull:
            return 50, DBULL
        # Outer BULL
        if distance < self.outbull:
            return 25, BULL
        point = self.points[int(angle / angle_p + 10.5)]
        # Triple ring
        if self.triple_inside <= distance <= self.triple_outside:
            return point, TRIPLE
        # Double ring
        if self.double_inside <= distance <= self.double_outside:
            return point, DOUBLE
        return point, SINGLE


class ScorePanel:
    color = (0, 0, 0, 100)
    fontname = 'GDhighwayJapan-026b1.otf'
    def __init__(self, pos, size=(100, 100)):
        self.surface = pygame.Surface(size).convert_alpha()
        self.surface.fill(self.color)
        self.pos = pos
    def update(self):
        pass


class ThrowScorePanel(ScorePanel):
    def __init__(self, pos, size):
        ScorePanel.__init__(self, pos, size)
        self.playerfont = pygame.font.Font(self.fontname, 12)
        self.playerfont.set_bold(True)
        self.rfont = pygame.font.Font(self.fontname, 12)
        self.pfont = pygame.font.Font(self.fontname, 12)
        self.set_player('Player 1')
        self.set_round(1)
        self.points = []

    def set_player(self, player):
        self.player = player

    def set_round(self, r):
        self.round = r

    def add_point(self, throw, ring, point):
        if len(self.points) >= 3:
            self.points = []
        self.points.append((throw, ring, point))

    def ringpttostr(self, ring, point):
        if point <= 0:
            return ' 0 OutBoard'
        if ring == SINGLE:
            return '%2d Single%d' % (point, point)
        if ring == DOUBLE:
            return '%2d Double%d' % (point*2, point)
        if ring == TRIPLE:
            return '%2d Triple%d' % (point*3, point)
        if ring == BULL:
            return '25 BULL'
        if ring == DBULL:
            return '50 D-BULL'

    def update(self):
        self.surface.fill(self.color)
        x, y = self.surface.get_size()
        pygame.draw.rect(self.surface, (204, 0, 51), ((5, 5), (x-10, 30)))
        self.surface.blit(self.playerfont.render(self.player, True, color.Color('White')), (10, 10))
        self.surface.blit(self.rfont.render('Round %s' % str(self.round), True, color.Color('White')), (10, 40))

        ypos = 60
        for throw, ring, point in self.points:
            self.surface.blit(self.pfont.render(self.ringpttostr(ring, point), True, color.Color('White')), (10, ypos))
            ypos += 20


class SoundEffect:
    hit_se = pygame.mixer.Sound('hit.wav')
    hit_se_single = pygame.mixer.Sound('single.wav')
    hit_se_double = pygame.mixer.Sound('double.wav')
    hit_se_triple = pygame.mixer.Sound('triple.wav')
    hit_se_bull = pygame.mixer.Sound('bull.wav')
    hit_se_dbull = pygame.mixer.Sound('dbull.wav')
    def effect(self, ring):
        SoundEffect.hit_se.play()
        if ring == SINGLE:
            SoundEffect.hit_se_single.play()
        if ring == DOUBLE:
            SoundEffect.hit_se_double.play()
        if ring == TRIPLE:
            SoundEffect.hit_se_triple.play()
        if ring == BULL:
            SoundEffect.hit_se_bull.play()
        if ring == DBULL:
            SoundEffect.hit_se_dbull.play()

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
    screct = scr.get_rect()
    room = Room()
    tpanel = ThrowScorePanel((10, 350), (230, 120))
    tpanel.update()
    scr.blit(tpanel.surface, (10, 10))
    scr_x, scr_y = scr.get_size()
    boardshadow = BoardShadow()
    board = Board()
    board_x, board_y = board.image.get_size()
    board.move((scr_x/2 - board_x/2, scr_y/2 - board_y/2 - 20))
    bullets = []
    se = SoundEffect()
    allsprites = pygame.sprite.RenderPlain(board)
    #bg.blit(boardshadow.image, (scr_x/2 - board_x/2, scr_y/2 - board_y/2 - 10))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                start_pos = pygame.mouse.get_pos()
                start_t = time.time()

            if event.type == MOUSEBUTTONUP:
                end_pos = pygame.mouse.get_pos()
                end_t = time.time()
                bullets.append(Bullet(start_pos, end_pos, start_t, end_t))

        scr.blit(bg, (0, 0))
        scr.blit(tpanel.surface, tpanel.pos)
        allsprites.draw(scr)
        for i, bullet in enumerate(bullets):
            bullet.move()
            if outofrect(bullet.center, screct):
                pt, ring = (0, OB)
                tpanel.add_point(1, ring, pt)
                tpanel.update()
                del bullets[i]
                continue
            if bullet.z >= room.wall_distance:
                pt, ring = board.getpoint(bullet.center)
                tpanel.add_point(1, ring, pt)
                tpanel.update()
                se.effect(ring)
                del bullets[i]
                continue
            scr.blit(bullet.surface, bullet.pos)

        pygame.display.flip()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
