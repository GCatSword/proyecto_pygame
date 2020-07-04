import pygame as pg
from pygame.locals import *
import sys, os 

BLANCO = (250,250,250)
FPS = 60

class Cruz(pg.sprite.Sprite):
    w = 89
    h = 91
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.giraCentro = (x, y)


        self.animation_time = FPS//1000 * 3
        self.angle = 0
        self.current_time = 0

        self.frame = pg.image.load('./resources/images/nave2.png').convert_alpha()
        self.image.blit(self.frame, (0,0), (0, 0, self.w, self.h))

        self.rotando = False

    def update(self, dt):
        self.current_time += dt

        if self.rotando:
            self.angle = (self.angle + 1)%360
            self.image = pg.transform.rotate(self.frame, self.angle)
            rect = self.image.get_rect()
            newSemiW = rect.centerx
            newSemiH = rect.centery

            dX = newSemiW - self.w//2
            dY = newSemiH - self.h//2

            self.rect.centerx = self.giraCentro[0] - dX
            self.rect.centery = self.giraCentro[1] - dY

            if self.angle % 180 == 0:
                self.rotando = False

        else:
            self.rect.centerx += 5
            self.giraCentro = self.rect.center

        if self.rect.centerx > 800 + self.w/2:
            self.rect.centerx = -self.w/2


class Game():
    clock = pg.time.Clock()

    def __init__(self, width, height):
        self.display = pg.display
        self.screen = self.display.set_mode((width, height))
        self.display.set_caption('Corredor')
        self.w = width
        self.h = height


        self.girador = Cruz(400, 150)
        self.allSprites = pg.sprite.Group()
       
        self.allSprites.add(self.girador)

    def handleevent(self):
        for event in pg.event.get():
            if event == QUIT:
                return True
            if  event.type == KEYDOWN:
                if  event.key == K_q:
                    return True
                if event.key == K_t:
                   
                    self.girador.rotando = True
        return False

    def render(self, dt):
        self.screen.fill(BLANCO)

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen)

        self.display.flip()

    def mainloop(self):
        sal = False

        while sal == False:
            dt = self.clock.tick(FPS)

            sal = self.handleevent()
            print(sal)

            self.render(dt)

        self.game_over()

    def game_over(self):
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.mainloop()