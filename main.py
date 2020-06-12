import pygame as pg
from pygame.locals import *
import sys, random
from entities import *


BLACK = (0,0,0)
COLOR_SCORE = (204, 153, 0)
COLOR_SCORE2 = (204, 0, 0)

WIN_GAME_SCORE = 100

class Game:
    def __init__(self):
        
        self.screen = pg.display.set_mode((1280, 720))
        self.screen.fill(BLACK)
        self.bkg = pg.image.load("./resources/images/fondo2.jpg")
        self.ship = Ship(100)

        self.e1 = Enemies()
        self.e2 = Enemies()
        self.e3 = Enemies()
        self.e4 = Enemies()
        self.e5 = Enemies()
        self.e6 = Enemies()
        self.e7 = Enemies()

        self.status = 'Game'

        self.font = pg.font.Font("./resources/fonts/font.ttf", 40)
        self.text_score = self.font.render("Score:", True, COLOR_SCORE)
        self.score = self.font.render("0", True, COLOR_SCORE)
        self.level1 = self.font.render("Mercury", True, COLOR_SCORE)
        self.level2 = self.font.render("Venus", True, COLOR_SCORE)
        self.level3 = self.font.render("Earth", True, COLOR_SCORE)
       


        self.clock = pg.time.Clock()


        
        pg.display.set_caption("SpaceX")


    def handlenEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
                        
            if event.type == KEYDOWN:
                if event.key == K_w:
                    self.ship.vy = -2
                if event.key == K_s:
                    self.ship.vy = 2

        key_pressed = pg.key.get_pressed()
        if key_pressed[K_w]:
            self.ship.vy -= 0.1
        elif key_pressed[K_s]:
            self.ship.vy += 0.1
        else:
            self.ship.vy = 0
        
        return False

    def loop_game(self):
        game_over = False
        self.score_time = 0
        self.final_score = 0
        timer = 10 
        second = self.clock.tick(30) / 1000  

        while not game_over:
            game_over = self.handlenEvent()
            self.ship.move(1280, 720)
            self.e1.move(1280, 720)


            if not self.score_time == WIN_GAME_SCORE:
                if self.clock.tick():
                    self.score_time +=1
                    self.score = self.font.render(str(self.score_time), True, COLOR_SCORE)
                    
    
            if self.score_time == WIN_GAME_SCORE:
                    timer -= second
                    if timer <= 0:
                        self.final_score = self.score_time + 500
                        self.score = self.font.render(str(self.final_score), True, COLOR_SCORE2)
                        #self.screen.blit(self.planet.image, (self.planet.posx, self.planet.posy))
            
                        #game_over = True

 
            self.screen.blit(self.bkg, (0, 0))
            self.screen.blit(self.ship.image, (self.ship.posx, self.ship.posy))
            self.screen.blit(self.e1.image, (self.e1.posx, self.e1.posy))
            self.screen.blit(self.text_score, (10, 20))
            self.screen.blit(self.score, (150, 20))
            self.screen.blit(self.level1, (550, 20))
            
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

            self.screen.fill((0,0,BLACK))
            self.screen.blit(self.bkg, (0, 0))
            
            pg.display.flip()  
    
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
