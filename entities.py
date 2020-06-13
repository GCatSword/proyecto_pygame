import pygame as pg
from pygame.locals import *
import sys, random

COLOR_SHIP = (175,0,0)
COLOR_ENEMIES = (0, 153, 51)
BLACK = (0,0,0)
FPS = 60

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
        super().__init__(50,51,centerx,350)
        self.color = COLOR_SHIP

        self.image = pg.Surface((50,51), pg.SRCALPHA, 32)
        self.image_ship = pg.image.load("./resources/images/nave2.png")
        self.image.blit(self.image_ship, (0,0))
                
        
    def move(self, limSupX, limSupY):

        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cy < self.h //2:
            self.Cy = self.h // 2

        if self.Cy > limSupY - self.h // 2:
            self.Cy = limSupY - self.h // 2

    
    def landing(self):

        if self.Cy < 350:
            self.Cy += 2
        if self.Cy > 350:
            self.Cy -= 2
        
        self.Cx += 1
        if self.Cx >= 900:
            self.Cx = 900

    def colision(self, something):
        
        if self.Cx == something.Cx:
            
            print("choque")
            game_over = True

    def rotate(self):
        pass
        


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
        self.Cx = random.randint(1200, 1280)
        self.Cy = random.randint(60, 600)


class Planet(Mobile):
    def __init__(self, centerx=0, centery=0):
        super().__init__(500, 500, centerx=centerx, centery=centery)
        self.reset()
        self.color = COLOR_ENEMIES
        self.image = pg.Surface((500,500), pg.SRCALPHA, 32)
        #self.image_planet1 = pg.image.load("./resources/images/mercury.png")
        #self.image_planet2 = pg.image.load("./resources/images/venus.png")
        self.image_planet3 = pg.image.load("./resources/images/earth.png")
        #self.image.blit(self.image_planet1, (0,0))
        #self.image.blit(self.image_planet2, (0,0))
        self.image.blit(self.image_planet3, (0,0))


       
    def move(self, limSupX, limSupY):
        
        self.Cx += self.vx
        self.Cy += self.vy

        if self.Cx <= 1200:
            self.Cx = 1200

    def reset(self):
        self.vx = -0.5
        self.vy = 0
        self.Cx = 1600
        self.Cy = 350