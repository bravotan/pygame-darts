# A simple text box with support for readline-compatible keys and
# tab completion.

# Copyright (c)2004 Joe Wreschnig <piman@sacredchao.net>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

__author__ = "Joe Wreschnig"
__copyright__ = "Copyright (c)2003 Joe Wreschnig"
__license__ = "GNU GPL version 2"
__version__ = "1"

import os
import glob
import pygame; from pygame.locals import *

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [128, 128, 128]

class TextBox(object):
    def __init__(self, message, tabcomp = True, size = 28, width = 512):
        if message == None: message = ""

        font = pygame.font.Font(None, size)
        surf = pygame.Surface([width + 2, 2 * font.get_linesize() + 4])
        font.set_bold(True)
        question = font.render(message, True, GRAY)
        surf.fill(BLACK)
        pygame.draw.rect(surf, WHITE, surf.get_rect(), 1)
        surf.blit(question, [1, 1])
        font.set_bold(False)

        self._tabcomp = tabcomp
        self._font = font
        self._surface = surf

    def ask(self, screen, string = None):
        if string == None: string = ""
        idx = len(string)
        cut = ""

        r_q = self._surface.get_rect()
        r_q.center = screen.get_rect().center
        while True:
            x_off = 10
            screen.blit(self._surface, r_q)
            for i in range(len(string)):
                c = string[i]
                if i == idx: self._font.set_underline(True)                    
                img_a = self._font.render(c, True, WHITE)
                self._font.set_underline(False)
                r_a = img_a.get_rect()
                r_a.topleft = [r_q.x + x_off,
                               r_q.y + self._font.get_linesize() + 1]
                x_off += img_a.get_width()            
                screen.blit(img_a, r_a)

            if idx == len(string):
                img_a = self._font.render("_", True, WHITE)
                r_a = img_a.get_rect()
                r_a.topleft = [r_q.x + x_off,
                               r_q.y + self._font.get_linesize() + 1]
                screen.blit(img_a, r_a)

            pygame.display.update()

            ev = pygame.event.wait()
            while ev.type != KEYDOWN:
                ev = pygame.event.wait()

            if ev.key == K_ESCAPE: return None
            elif ev.key == K_F11: pygame.display.toggle_fullscreen()
            elif ev.key == K_BACKSPACE:
                string = string[:idx - 1] + string[idx:]
                idx -= 1
            elif ev.key == K_DELETE:
                string = string[:idx] + string[idx + 1:]
            elif ev.key == K_RETURN: break
            elif ev.key == K_END: idx = len(string)
            elif ev.key == K_HOME: idx = 0
            elif ev.key == K_LEFT: idx = max(0, idx - 1)
            elif ev.key == K_RIGHT: idx = min(len(string), idx + 1)
            elif ev.key == K_TAB:
                if self._tabcomp: string = self._complete(string)
                idx = len(string)
            elif ev.key < 128:
                if ev.mod & KMOD_CTRL:
                    if len(string) == 0: pass
                    elif ev.key == K_u:
                        string = ""
                        idx = 0
                    elif ev.key == K_h: string = string[0:-1]
                    elif ev.key == K_e: idx = len(string)
                    elif ev.key == K_a: idx = 0
                    elif ev.key == K_f: idx = min(len(string), idx + 1)
                    elif ev.key == K_b: idx = max(0, idx - 1)
                    elif ev.key == K_t:
                        if idx == 0: idx = 1
                        if len(string) == 1: pass
                        elif idx == len(string):
                            string = string[:-2] + string[-1] + string[-2]
                        else:
                            string = (string[:idx - 1] + string[idx] +
                                      string[idx - 1] + string[idx + 1:])
                            idx = min(len(string), idx + 1)
                    elif ev.key == K_k:
                        cut = string[idx:]
                        string = string[:idx]
                    elif ev.key == K_y:
                        string = string[:idx] + cut + string[idx:]
                        idx += len(cut)
                    elif ev.key == K_w:
                        if string[-1] == "/": string = string[:-1]
                        string = string[:string.rfind("/") + 1]
                else:
                    string = string[:idx] + ev.unicode + string[idx:]
                    idx += 1

        return string

    def _complete(self, string):
        if '*' not in string: string += "*"

        g = glob.glob(string)
        if len(g) == 0: s = string[:-1]
        elif len(g) == 1: s = g[0]
        else: # thanks, mu
            for i, chars in enumerate(zip(*g)):
                if min(chars) != max(chars):
                    j = i
                    break
            else: j = min([len(s) for s in g])
            s = g[0][:j]
        s = os.path.expanduser(s)
        if os.path.isdir(s) and s[-1] != "/": s += "/"
        return s

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([640, 240])
    box = TextBox("Please enter a filename:")
    print "You entered", box.ask(screen)
    pygame.quit()
