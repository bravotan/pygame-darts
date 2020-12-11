#!/usr/bin/env python

import pygame
from pygame.locals import *
pygame.init()

import math
import time
FONTNAME = 'GDhighwayJapan-026b1.otf'

class GameApp:
    SCREEN_SIZE = 640, 480
    TITLE = 'Spyder darts game'
    FPS = 60
    def __init__(self):
        self.display = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption(self.TITLE)
        pygame.mouse.set_visible(True)
    def mainloop(self):
        clock = pygame.time.Clock()
        seen = TitleSeen()
        while True:
            clock.tick(self.FPS)
            newseen = seen.update()
            if newseen == QUIT:
                return
            if isinstance(newseen, Seen):
                seen = newseen
            pygame.display.flip()

class Seen:
    def __init__(self):
        self._screen = pygame.display.get_surface()
        self._surface = pygame.Surface(self._screen.get_size()).convert_alpha()
    def update(self):
        pass

class GameSeen(Seen):
    def __init__(self):
        Seen.__init__(self)
        class Board(pygame.sprite.Sprite):
            IMAGE_FILE = 'dartsboard.png'
            inbull = 12.7/4.0
            outbull = 31.8/4.0
            triple_inside = 99/2.0
            triple_outside = 107/2.0
            double_inside = 162/2.0
            double_outside = 170/2.0
            points = 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6
            def __init__(self, pos=(0, 0)):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(self.IMAGE_FILE).convert_alpha()
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
        
        class BoardShadow(pygame.sprite.Sprite):
            image_fn = 'dartsboard-shadow.png'
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
        # setup darts board
        board = Board()
        boardshadow = BoardShadow()
        scr_x, scr_y = self._screen.get_size()
        board_x, board_y = board.image.get_size()
        board.move((scr_x/2 - board_x/2, scr_y/2 - board_y/2 - 20)) 
        boardshadow.move((scr_x/2 - board_x/2, scr_y/2 - board_y/2 - 10))
        self.board = pygame.sprite.RenderPlain((boardshadow, board))
        # background
        self.bg = pygame.image.load('background.jpg').convert()
        # sound
        self.se_start = pygame.mixer.Sound('start.wav')
        self.se_end = pygame.mixer.Sound('end.wav')

        # game state
    def blitimage(self, surface):
        surface.blit(self.bg, (0, 0))
        self.board.draw(surface)
    def update(self):
        self._screen.blit(self.bg, (0, 0))
        self.board.draw(self._screen)

class Countup(GameSeen):
    def update(self):
        GameSeen.update(self)
        event = pygame.event.wait()
        if event.type == QUIT:
            return QUIT

class Cricket(GameSeen):
    def update(self):
        GameSeen.update(self)
        event = pygame.event.wait()
        if event.type == QUIT:
            return QUIT

def getseenbyname(name):
    if name == 'countup':
        return Countup()
    if name == 'cricket':
        return Cricket()

class TitleSeen(Seen):
    DARKNESS_COLOR = (0, 0, 0, 200)
    TITLE_FONT = pygame.font.Font(FONTNAME, 100)
    TITLE = 'spyder'
    TITLE_COLOR = color.Color('White')
    TITLE_POS = (50, 100)
    STRIPE_COLOR = (color.Color('Brown'))
    GAME_NAMES = 'countup', 'cricket'
    MENU_RIGHTMARGIN = 120
    def __init__(self):
        Seen.__init__(self)
        class Button(pygame.sprite.Sprite):
            FONT_SIZE = 20
            FONT = pygame.font.Font(FONTNAME, FONT_SIZE)
            DEFAULT_COLOR = color.Color('White')
            ROLLOVER_COLOR = color.Color('Red')
            def __init__(self, text, screen):
                pygame.sprite.Sprite.__init__(self)
                self.text = text
                self.default_img = self.FONT.render(text, True, self.DEFAULT_COLOR)
                self.rollover_img = self.FONT.render(text, True, self.ROLLOVER_COLOR)
                self.image = self.default_img
                self.rect = self.image.get_rect()
                sx, sy = screen.get_size()
                ix, iy = self.image.get_size()
                self.get_size = self.image.get_size
            def move(self, pos):
                self.rect = self.rect.move(pos)
            def chk_select(self, event):
                if event.type == MOUSEBUTTONDOWN and \
                  self.rect.colliderect(pygame.mouse.get_pos(), (0, 0)):
                    return self.text
            def update(self):
                if self.rect.colliderect(pygame.mouse.get_pos(), (0, 0)):
                    self.image = self.rollover_img
                else:
                    self.image = self.default_img

        self.title_text = self.TITLE_FONT.render(self.TITLE, True, self.TITLE_COLOR)
        tx, ty = self.title_text.get_size()
        tposx, tposy = self.TITLE_POS
        self.buttons = pygame.sprite.RenderPlain()
        for i, name in enumerate(self.GAME_NAMES):
            button = Button(name, self._screen)
            button.move((self._screen.get_size()[0]-button.get_size()[0]-self.MENU_RIGHTMARGIN,
                         ty+tposy+10+i*(Button.FONT_SIZE+10)))
            self.buttons.add(button)
            self.gameseen = GameSeen()
    def update(self):
        title_x, title_y = self.title_text.get_size()
        tpos_x, tpos_y = self.TITLE_POS
        scr_x, scr_y = self._screen.get_size()

        self.gameseen.blitimage(self._surface)
        darkness = pygame.Surface((scr_x, scr_y)).convert_alpha()
        darkness.fill(self.DARKNESS_COLOR)
        self._surface.blit(darkness, (0, 0))
        
        self._surface.blit(self.title_text, self.TITLE_POS)
        pygame.draw.rect(self._surface, self.TITLE_COLOR, (tpos_x, tpos_y-5, title_x, 5))
        pygame.draw.rect(self._surface, self.TITLE_COLOR, (tpos_x, tpos_y+title_y+5, title_x, 5))
        pygame.draw.rect(self._surface, self.STRIPE_COLOR, (scr_x - tpos_x - 50, title_y + tpos_y + 10, 50, 400))
        self.buttons.update()
        self.buttons.draw(self._surface)
        self._screen.blit(self._surface, (0, 0))

        event = pygame.event.wait()
        for button in self.buttons.sprites():
            name = button.chk_select(event)
            if name:
                print name
                return getseenbyname(name)

if __name__ == '__main__':
    GameApp().mainloop()
