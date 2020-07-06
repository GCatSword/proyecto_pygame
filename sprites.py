import pygame as pg
from pygame.locals import *
import sys, random

VOLUMEN = 1

FPS60 = [-9,-8,-7,-6]
FPS30 = [-15,-14,-13,-11]
FPS120 = [4,-3,-2,-1]

class Enemy(pg.sprite.Sprite):
    vx = 0
    vy = 0

    def __init__(self, centerx=0, centery=0):
        super().__init__()

        self.w= random.randint(40, 80)
        self.h= random.randint(40, 80)
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.image2 = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.image3 = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)    
        self.rect = self.image.get_rect()
        
        self.image = pg.image.load("./resources/images/rock.png")
        self.image2 = pg.image.load("./resources/images/rock2.png")
        self.image3 = pg.image.load("./resources/images/ovni.png")
        self.image = pg.transform.scale(self.image,(self.w, self.h))
        self.image2 = pg.transform.scale(self.image2,(self.w, self.h))
        self.image3 = pg.transform.scale(self.image3,(self.w, self.h))
        self.image.blit(self.image, (0,0))
        self.reset()
       
    def reset(self):
        self.image = random.choice([self.image, self.image2, self.image3])
        self.vx = random.choice(FPS60)
        self.vy = 0 
        self.rect.centerx = 1300
        self.rect.centery = random.randint(50, 700)

    def update(self, limSupX, limSupY):              
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        
        if self.rect.centerx <= -50:
            self.kill()

class SpaceShip(pg.sprite.Sprite):
    vx = 0
    vy = 0
    num_sprites = 9
    
    def __init__(self, x, y):
        super().__init__()
        self.w= 50
        self.h= 50
        self.angle = 0

        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image_ship = pg.image.load("./resources/images/nave.png")
        self.image_ship = pg.transform.scale(self.image_ship,(self.w, self.h))
        self.image.blit(self.image_ship, (0, 0))
        self.rect.x = x
        self.rect.y = y

        self.image_act = 0
        self.num_sprites = 9
        self.animation_time = 200
        self.current_time = 0
        self.contador_sonido = 0
        self.colision = 0

        self.explosion_sound = pg.mixer.Sound('./resources/sounds/space_explosion.wav')  
        self.win_sound = pg.mixer.Sound('./resources/sounds/pax6.wav')
        
    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2

    def landing(self):
        if self.rect.centery < 350:
            self.rect.centery += 4
        if self.rect.centery > 350:
            self.rect.centery -= 4
        
        self.angle +=1
        if self.angle <= 180:
            self.rotate()
        else:    
            self.rect.centerx += 4
            if self.rect.centerx >= 930:
                self.rect.centerx = 930
                if self.contador_sonido == 0:
                    self.contador_sonido = 1
                    self.win_sound.play()
                    self.win_sound.set_volume(VOLUMEN)
                
    def rotate(self):
        #self.image = pg.transform.rotate(self.image, 180)
        self.image = pg.transform.rotate(self.image_ship, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def checkCollision(self, group, dt):
        lista = pg.sprite.spritecollide(self, group, False)
        
        if len(lista) > 0:
            self.colision += 1

        if self.colision > 0:
            self.current_time += dt
            self.images_explosion = [pg.image.load("./resources/sprites/e_{}.png".format(i)) for i in range(self.num_sprites)]
            
            if self.contador_sonido == 0:
                self.contador_sonido = 1
                self.explosion_sound.play()
                self.explosion_sound.set_volume(VOLUMEN)

            if self.current_time >= self.animation_time and self.image_act <= 7:
                self.current_time = 0
                self.image_act += 1

            self.image = self.images_explosion[self.image_act]
                
            if self.image_act >= len(self.images_explosion):
                self.image_act = 0

        return lista

class Planet(pg.sprite.Sprite):
    vx = 0
    vy = 0

    def __init__(self, x):
        super().__init__()
        self.x = x
        self.w= 500
        self.h= 500
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image,(self.w, self.h))
        self.image.blit(self.image, (0,0))
        self.reset()

    def LoadImages(self):
        if self.x == 1:
            self.image = self.image_planet1
        if self.x == 2:
            self.image = self.image_planet2
        if self.x == 3:
            self.image = self.image_planet3

    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centerx <= 1200:
            self.rect.centerx = 1200

    def reset(self):
        self.vx = -3
        self.vy = 0
        self.rect.centerx = 1600
        self.rect.centery = 350

        if self.x == 1:
            self.image = pg.image.load("./resources/images/mercury.png")
        if self.x == 2:
            self.image = pg.image.load("./resources/images/venus.png")
        if self.x == 3:
            self.image = pg.image.load("./resources/images/earth.png")

class Astronaut(pg.sprite.Sprite):
    vx = 0
    vy = 0
    
    def __init__(self, x, y):
        super().__init__()
        self.w= 40
        self.h= 80

        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image_astronaut = pg.image.load("./resources/images/astronaut.png")
        self.image_astronaut = pg.transform.scale(self.image_astronaut,(self.w, self.h))
        self.image.blit(self.image_astronaut, (0, 0))
        self.rect.x = x
        self.rect.y = y
     
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')

    def update(self, limSupX, limSupY):
        self.rect.top += self.vy
        self.rect.bottom += self.vy
        self.rect.left += self.vx
        self.rect.right += self.vx
        
        if self.rect.centery < self.rect.h // 2:
            self.rect.centery = self.rect.h // 2
        elif self.rect.centerx < self.rect.w // 2:
            self.rect.centerx = self.rect.w // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2
        elif self.rect.centerx > limSupX - self.rect.w // 2:
            self.rect.centerx = limSupX - self.rect.w // 2
                
    def rotate(self, angle):
        self.angle = angle
        self.image = pg.transform.rotate(self.image_astronaut, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def checkCollision(self, group):
        lista = pg.sprite.spritecollide(self, group, True)
        if len(lista) > 0:
            self.ping.play()

        return lista

class EnemyBonus(pg.sprite.Sprite):
    vx = 0
    vy = 0

    def __init__(self, centerx=0, centery=0):
        super().__init__()

        self.w= 50
        self.h= 50
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)    
        self.rect = self.image.get_rect()
        
        self.image = pg.image.load("./resources/images/alien.png")
        self.image = pg.transform.scale(self.image,(self.w, self.h))
        self.image.blit(self.image, (0,0))
        self.reset()
    
    def reset(self):
        self.vx = 0
        self.vy = random.randint(4,6)
        self.rect.centerx = random.randint(50, 1200)
        self.rect.centery = 0

    def update(self, limSupX, limSupY):              
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        
        if self.rect.centery >= 750:
            self.kill()
    
    