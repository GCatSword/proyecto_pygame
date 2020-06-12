import pygame as pg
from pygame.locals import *
import sys, random

COLOR_SHIP = (175,0,0)
COLOR_ENEMIES = (0, 153, 51)
BLACK = (0,0,0)

class Mobile:
    vx = 0
    vy = 0
    __color = BLACK
    def __init__(self, w, h, centerx=0, centery=0):
        self.w = w
        self.h = h
        self.Cx = centerx
        self.Cy = centery

        self.image = pg.Surface((self.w, self.h))
        self.image.fill(self.__color)

    @property
    def posx(self):
        return self.Cx - self.w // 2
        
    @property
    def posy(self):
        return self.Cy - self.h // 2
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)
 
    def move(self, *args, **kwargs):
        pass


class Ship(Mobile):
    def __init__(self, centerx):
        super().__init__(50,25,centerx,350)
        self.color = COLOR_SHIP
        
    def move(self, limSupX, limSupY):

        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2


class Enemies(Mobile):
    def __init__(self, centerx=0, centery=0):
        super().__init__(25, 25, centerx=centerx, centery=centery)
        self.reset()
        self.color = COLOR_ENEMIES
    def move(self, limSupX, limSupY):

        self.Cx += self.vx
        self.Cy += self.vy

    def reset(self):
        self.vx = random.choice([-1,-2])
        self.vy = 0
        self.Cx = random.randint(900, 1100)
        self.Cy = random.randint(60, 600)