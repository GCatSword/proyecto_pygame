import pygame as pg
from pygame.locals import *
import sys, random


DARK_GREY = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 3

class Enemy(pg.sprite.Sprite):
    vx = 0
    vy = 0
    num_sprites = 12

    def __init__(self):
        super().__init__()
        self.image = pg.Surface((50, 50), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image_ovni = pg.image.load("./resources/images/ovni33.png")
        #self.images = self.loadImages()
        #elf.image_act = 0
        self.image.blit(self.image_ovni, (0, 0))
        self.reset()

        self.soyToxica = False
        
        #self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        #self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')

    def loadImages(self):
        pass
        '''
        images = []
        for i in range(self.num_sprites):
            image = pg.image.load("./resources/sprites/f_{}.png".format(i))
            images.append(image)
        return images
        '''
        # Compresión del for en una línea
        #return [pg.image.load("./resources/sprites/f_{}.png".format(i)) for i in range(self.num_sprites)]
        

    def reset(self):
        self.rect.w = random.randint(50, 100)
        self.rect.h = random.randint(50, 100)
        self.vx = random.choice([-1.5, -1,])
        self.vy = 0 
        self.rect.centerx = random.randint(1200, 1280)
        self.rect.centery = random.randint(50, 700)

    def colision(self, group):
        colision = pg.sprite.spritecollide(self, group, True)



    def update(self, limSupX, limSupY):
                        
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        #animar bola
        '''
        self.image_act += 1
        if self.image_act >= self.num_sprites:
            self.image_act = 0
        self.image_act +=1
        self.image_act = self.image_act % self.num_sprites
        '''

        #self.image_act = (self.image_act + 1) % self.num_sprites
        #self.image.blit(self.images[self.image_act], (0, 0))



class SpaceShip(pg.sprite.Sprite):
    vx = 0
    vy = 0
    __color = WHITE

    def __init__(self, centerx):
        super().__init__()
        
        self.image = pg.Surface((50, 51), pg.SRCALPHA, 32)
        
        self.rect = self.image.get_rect()
        self.image_ship = pg.image.load("./resources/images/nave2.png")
        self.image.blit(self.image_ship, (0, 0))
        self.rect.centerx = centerx
        self.rect.centery = 400
        #self.impacto = False

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)


    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2

    def landing(self):
        if self.rect.centery < 350:
            self.rect.centery += 2
        if self.rect.centery > 350:
            self.rect.centery -= 2
        
        self.rect.centerx += 1
        if self.rect.centerx >= 900:
            self.rect.centerx = 900


class Planet(pg.sprite.Sprite):
    vx = 0
    vy = 0
    __color = DARK_GREY

    def __init__(self):
        super().__init__()
        self.image = pg.Surface((500,500), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image_planet1 = pg.image.load("./resources/images/mercury.png")
        #self.image_planet2 = pg.image.load("./resources/images/venus.png")
        #self.image_planet3 = pg.image.load("./resources/images/earth.png")
        self.image.blit(self.image_planet1, (0,0))
        #self.image.blit(self.image_planet2, (0,0))
        #self.image.blit(self.image_planet3, (0,0))
        self.reset()

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, tupla_color):
        self.__color = tupla_color
        self.image.fill(self.__color)
       
    def update(self, limSupX, limSupY):
        
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centerx <= 1200:
            self.rect.centerx = 1200

    def reset(self):
        self.vx = -0.5
        self.vy = 0
        self.rect.centerx = 1600
        self.rect.centery = 350