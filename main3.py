import pygame as pg
from pygame.locals import *
import sys, random
from sprites import *


BLACK = (0,0,0)
COLOR_SCORE = (204, 153, 0)
COLOR_SCORE2 = (204, 0, 0)

WIN_GAME_SCORE = 1000

class Game:
    def __init__(self):
        
        self.screen = pg.display.set_mode((1280, 720))
        self.screen.fill(BLACK)
        self.bkg1 = pg.image.load("./resources/images/fondo2.jpg")
        '''
        self.ship = SpaceShip(100)
        self.playerGroup = pg.sprite.Group()
        self.playerGroup.add(self.ship)

        self.planet1 = Planet()
        self.planet2 = Planet()
        self.planet3 = Planet()
        self.planetsGroup = pg.sprite.Group()
        self.planetsGroup.add(self.planet1)
        self.planetsGroup.add(self.planet2)
        self.planetsGroup.add(self.planet3)

        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.playerGroup)
        self.allSprites.add(self.planetsGroup)

        self.spawnSprites = pg.sprite.Group()
        '''
        self.level_counter = 1

        self.status = 'Game'

        self.font = pg.font.Font("./resources/fonts/font.ttf", 40)
        self.fontGrande = pg.font.Font('./resources/fonts/font.ttf', 60)
        
        self.text_score = self.font.render("Score:", True, COLOR_SCORE)
        self.score = self.font.render("0", True, COLOR_SCORE)
        self.level1 = self.font.render("Mercury", True, COLOR_SCORE)
        self.level2 = self.font.render("Venus", True, COLOR_SCORE)
        self.level3 = self.font.render("Earth", True, COLOR_SCORE)

        self.escape = self.font.render("Press <ESC> for exit", True, COLOR_SCORE)
        self.next = self.font.render("Press <SPACE> for continue", True, COLOR_SCORE)
       
        self.text_game_over = self.fontGrande.render("GAME OVER", True, COLOR_SCORE)
        self.text_insert_coin = self.font.render('<SPACE> - Inicio partida', True, COLOR_SCORE2)

        pg.display.set_caption("SpaceX")


    def handlenEvent(self):

        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()

            if not self.score_time == WIN_GAME_SCORE:
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        self.ship.vy = -2
                    elif event.key == K_s:
                        self.ship.vy = 2
            else:
                self.ship.vy = 0
                    
        if not self.score_time == WIN_GAME_SCORE:
            key_pressed = pg.key.get_pressed()
            if key_pressed[K_w]:
                self.ship.vy -= 0.1
            elif key_pressed[K_s]:
                self.ship.vy += 0.1
            else:
                self.ship.vy = 0
        else:
            self.ship.vy = 0

        return False


    def loop_game(self):
        game_over = False
        self.score_time = 0
        self.final_score = 0
        self.clock = pg.time.Clock()# si lo pongo en el init, necesito el tic_busy_loop.
        #self.clock.tick_busy_loop()#resetear el tiempo
        timer = 10 
        second = self.clock.tick(30) / 1000 


        if self.level_counter == 1:
            self.spawn_enemy = 5
            self.spawn_time = 10
        if self.level_counter == 2:
            self.spawn_enemy = 10
            self.spawn_time = 5
        if self.level_counter == 3:
            self.spawn_enemy = 15
            self.spawn_time = 1

        self.spawn = []
        
        self.ship = SpaceShip(100)
        self.playerGroup = pg.sprite.Group()
        self.playerGroup.add(self.ship)

        self.planet1 = Planet()
        self.planet2 = Planet()
        self.planet3 = Planet()
        self.planetsGroup = pg.sprite.Group()
        self.planetsGroup.add(self.planet1)
        self.planetsGroup.add(self.planet2)
        self.planetsGroup.add(self.planet3)

        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.playerGroup)
        self.allSprites.add(self.planetsGroup)

        self.spawnSprites = pg.sprite.Group()

       
        while not game_over:
            game_over = self.handlenEvent()
            
            self.playerGroup.update(1280, 720)

            if not self.score_time == WIN_GAME_SCORE:
                if self.clock.tick():# Puntuación según el tiempo
                    self.score_time +=1
                    self.score = self.font.render(str(self.score_time), True, COLOR_SCORE)

                for i in range(self.spawn_enemy):#Spawn enemy cada segundo.
                    self.spawn_time -= second
                    if self.spawn_time <= 0:
                        self.spawn_time = 10
                        self.spawnSprites.add(Enemy())
                        
            self.spawnSprites.update(1280, 720)  
            
            colision = pg.sprite.groupcollide(self.spawnSprites, self.playerGroup, False, False)
            if not self.score_time == WIN_GAME_SCORE:
                if colision:
                    game_over = True

            if self.score_time == WIN_GAME_SCORE:
                #timer -= second
                #if timer <= 0:
                    self.planet1.update(1280, 720)
                    self.ship.landing()
                    
                    #self.ship.rotate()
                    self.final_score = self.score_time + 500
                    self.score = self.font.render(str(self.final_score), True, COLOR_SCORE2)
                    
                    key_pressed = pg.key.get_pressed()
                    if key_pressed[K_SPACE]:
                        game_over = True
                        self.level_counter +=1

            key_pressed = pg.key.get_pressed()
            if key_pressed[K_ESCAPE]:
                #self.spawnSprites.remove(self.spawnSprites)
                #self.allSprites.remove(self.allSprites)
                game_over = True
                

            self.screen.blit(self.bkg1, (0, 0))

            self.spawnSprites.draw(self.screen)
            self.allSprites.draw(self.screen)

            self.screen.blit(self.text_score, (10, 20))
            self.screen.blit(self.score, (150, 20))
            self.screen.blit(self.level1, (550, 20))
            self.screen.blit(self.escape, (900, 20))
            

            if self.score_time == WIN_GAME_SCORE:
                self.screen.blit(self.next, (400, 650))
                   
            pg.display.flip()

        self.status = 'Start'

    def start_game(self):
        start = False

        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        start = True

            
            self.screen.fill((BLACK))
            self.screen.blit(self.bkg1, (0, 0))
            self.screen.blit(self.text_game_over, (100, 100))
            self.screen.blit(self.text_insert_coin, (100, 200))
            
            pg.display.flip()

        self.status = 'Game'
    
    def main_loop(self):
        while True:
            if self.status == 'Game':
                self.loop_game()
            else:
                self.start_game()
   
    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()
