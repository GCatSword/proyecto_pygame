import pygame as pg
from pygame.locals import *
import sys, random, sqlite3
from sprites import *

BLACK = (0,0,0)
COLOR_SCORE = (204, 153, 0)
COLOR_SCORE2 = (204, 0, 0)
COLOR_START = (51,133, 255)

WIN_GAME_SCORE = 100
FPS = 120

class Game:
    def __init__(self):
        
        self.screen = pg.display.set_mode((1280, 720))
        self.screen.fill(BLACK)
        self.bkg1 = pg.image.load("./resources/images/fondo3.jpg")
        self.bkg1 = pg.image.load("./resources/images/fondo3.jpg")

        # Imagenes Start
        self.bkg_start = pg.image.load("./resources/images/fondo_start2.jpg")
        self.cockpit = pg.image.load("./resources/images/cabina.png")
        
        # Imagenes Score
        self.cup1 = pg.image.load("./resources/images/cup1.png")
        self.cup2 = pg.image.load("./resources/images/cup2.png")
        self.cup3 = pg.image.load("./resources/images/cup3.png")
        #self.bkg2 = BkgImage()
        
        self.level_counter = 0
        self.name = ' '
        self.word = " "
        
        self.final_score1 = 0
        self.final_score2 = 0
        self.final_score3 = 0

        self.status = 'Start'

        # Fuentes utilizadas
        self.font_small = pg.font.Font("./resources/fonts/font.ttf", 30)
        self.font = pg.font.Font("./resources/fonts/font.ttf", 40)
        self.fontGrande = pg.font.Font('./resources/fonts/font.ttf', 60)
        
        # Textos globales
        self.escape = self.font.render("Press <ESC> for exit", True, COLOR_SCORE)
        self.next = self.font.render("Press <SPACE> for continue", True, COLOR_SCORE)
        
        # Textos Loop_Game
        self.text_score = self.font.render("Score:", True, COLOR_SCORE)
        self.score = self.font.render("0", True, COLOR_SCORE)
        self.level1 = self.font.render("Mercury", True, COLOR_SCORE)
        self.level2 = self.font.render("Venus", True, COLOR_SCORE)
        self.level3 = self.font.render("Earth", True, COLOR_SCORE)

        # Textos Gameover
        self.text_game_over = self.fontGrande.render("GAME OVER", True, COLOR_SCORE)

        # Textos Start
        self.text_the_spacex = self.fontGrande.render("The SpaceX", True, COLOR_SCORE)
        self.text_start_game = self.font_small.render('<SPACE> - Start game', True, COLOR_SCORE)
        self.text_instructions = self.font_small.render('<i> - Instructions', True, COLOR_SCORE)
        self.text_credits = self.font_small.render('<c> - Credits', True, COLOR_SCORE)
        
        

        pg.display.set_caption("SpaceX")


    def handlenEvent(self):

        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()

            if not self.score_time == WIN_GAME_SCORE:
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        self.ship.vy = -5
                    elif event.key == K_s:
                        self.ship.vy = 5
            else:
                self.ship.vy = 0
                    
        if not self.score_time == WIN_GAME_SCORE:
            key_pressed = pg.key.get_pressed()
            if key_pressed[K_w]:
                self.ship.vy -= 1
            elif key_pressed[K_s]:
                self.ship.vy += 1
            else:
                self.ship.vy = 0
        else:
            self.ship.vy = 0

        return False

    def loop_game(self):
        gameover = False
        self.score_time = 0
        x = 0
        y = 0
        
        self.clock = pg.time.Clock()# si lo pongo en el init, necesito el tic_busy_loop.
        #self.clock.tick_busy_loop()#resetear el tiempo
        
        second = self.clock.tick(30) / 1000 
        
        self.top_list = []
        self.spawn = []
        
        self.ship = SpaceShip(200, 350)
        self.playerGroup = pg.sprite.Group()
        self.playerGroup.add(self.ship)

        #self.bkgGroup = pg.sprite.Group()
        #self.bkgGroup.add(self.bkg2)

        self.planetsGroup = pg.sprite.Group()
        self.spawnSprites = pg.sprite.Group()

        if self.level_counter >= 3:
            self.level_counter = 1

        if self.level_counter == 0:
            self.planet1 = Planet(1)
            self.planetsGroup.add(self.planet1)
            self.spawn_enemy = 10
            self.spawn_time = 10
            self.final_score1 = 0
        if self.level_counter == 1:
            self.planet2 = Planet(2)
            self.planetsGroup.add(self.planet2)
            self.spawn_enemy = 20
            self.spawn_time = 10
            self.final_score2 = 0
        if self.level_counter == 2:
            self.planet3 = Planet(3)
            self.planetsGroup.add(self.planet3)
            self.spawn_enemy = 30
            self.spawn_time = 10
            self.final_score3 = 0
            
        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.playerGroup)
        self.allSprites.add(self.planetsGroup)
        #self.allSprites.add(self.bkgGroup)


        while not gameover:
            gameover = self.handlenEvent()
            self.clock.tick(FPS)
            #self.bkgGroup.update(1280,720)
            self.playerGroup.update(1280, 720)

            colision = pg.sprite.groupcollide(self.spawnSprites, self.playerGroup, False, False)
            
            explosion = False
            while not explosion:
                if not self.score_time == WIN_GAME_SCORE:

                    x -= 2
                    if x <= - 2560:
                        x = 0

                    if colision:
                        self.spawn_enemy = 0
                        self.score_time = 0
                        x = 0
                        self.ship.explosion()
                        explosion = True
                        #gameover = True
                    else:
                        self.score_time += 1

                    self.score = self.font.render(str(self.score_time), True, COLOR_SCORE)
                    
                    for i in range(self.spawn_enemy):#Spawn enemy cada segundo.
                        self.spawn_time -= second
                        if self.spawn_time <= 0:
                            self.spawn_time = 10
                            self.spawnSprites.add(Enemy())

            self.spawnSprites.update(1280, 720)  

            if self.score_time == WIN_GAME_SCORE:
                self.landing_sound = pg.mixer.Sound('./resources/sounds/pax6.wav')
                self.landing_sound.play()
                self.landing_sound.set_volume(0.05)
                self.planetsGroup.update(1280, 720)
                self.ship.landing()
                self.landing_sound.stop()
                

                key_pressed = pg.key.get_pressed()
                if key_pressed[K_SPACE]:
                    self.level_counter +=1
                    self.landing_sound.stop()
                    gameover = True
                    

                if key_pressed[K_ESCAPE]:
                    self.landing_sound.stop()


            if self.level_counter == 0:
                self.final_score1 = self.score_time + 500  
            if self.level_counter == 1:
                self.final_score2 = self.score_time + 1000  
            if self.level_counter == 2:
                self.final_score3 = self.score_time + 2000  

            self.all_score = self.final_score1 + self.final_score2 + self.final_score3  

            key_pressed = pg.key.get_pressed()
            if key_pressed[K_ESCAPE]:
                self.level_counter = 0
                gameover = True
                

            self.screen.blit(self.bkg1, (x, 0))
            self.screen.blit(self.bkg1, (x+2560, 0))
            

            #self.spawnSprites.draw(self.screen)
            #self.playerGroup
            #self.planetsGroup.draw(self.screen)
            self.allSprites.draw(self.screen)

            #self.screen.blit(self.text_score, (10, 20))
            #self.screen.blit(self.score, (150, 20))
            #self.screen.blit(self.escape, (900, 20))
            #self.screen.blit(self.cockpit, (0, 200))
            '''
            if self.level_counter == 0:
                self.score = self.font.render(str(self.final_score1), True, COLOR_SCORE2)
                self.screen.blit(self.level1, (550, 20))
            if self.level_counter == 1:
                self.score = self.font.render(str(self.final_score2), True, COLOR_SCORE2)
                self.screen.blit(self.level2, (550, 20))
            if self.level_counter == 2:
                self.score = self.font.render(str(self.final_score3), True, COLOR_SCORE2)
                self.screen.blit(self.level3, (550, 20))
            '''
            

            #self.score = self.font.render(str(self.final_score), True, COLOR_SCORE2)

            if self.score_time == WIN_GAME_SCORE:
                self.screen.blit(self.next, (400, 650))
                   
            pg.display.flip()
        

        if self.level_counter == 1:
            self.status = "Level2"
        elif self.level_counter == 2:
            self.status = "Level3"
        elif self.level_counter == 3:
            self.level_counter = 0
            self.status = "End"
        elif self.level_counter == 0:
            self.status = "Game over"
        else:
            self.status = 'Start'

    def game_over(self):
        start = False

        pg.time.set_timer(USEREVENT+1, 10000)
        
        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = True

                if event.type == USEREVENT+1:
                    start = True

            
            self.screen.fill((BLACK))
            self.screen.blit(self.bkg1, (0, 0))
            self.screen.blit(self.text_game_over, (480, 300))
            self.screen.blit(self.escape, (900, 20))
            
            pg.display.flip()
       
        self.status = 'Start'
    
    def text_input(self, word, x, y):
        font = pg.font.Font("./resources/fonts/font.ttf", 40)
        text = font.render("{}".format(word), True, COLOR_SCORE)
        return self.screen.blit(text,(x,y))

    def inpt(self):
        self.word=""
        done = False
        #key = (chr(event.key))
        Key_accepted = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"

        while not done:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if len(self.word) <= 2 and (event.key) and str.upper((chr(event.key))) in Key_accepted:
                            self.word += str.upper((chr(event.key)))
                            print(self.word)
                            print(len(self.word))
                    if event.key == K_DELETE:
                        x = len(self.word)
                        self.word = self.word[:-x]
                    if event.key == K_SPACE:
                        done=True

            self.screen.blit(self.bkg1, (0, 0))
            self.text_word = self.font.render("{}".format(self.word), True, COLOR_SCORE)
            self.text_input("Please enter your name: {}".format(self.word),200,300)
            self.screen.blit(self.next, (400, 650))
            pg.display.flip()
        self.status = "Score"

    def start_game(self):
        start = False
        self.intro_sound = pg.mixer.Sound('./resources/sounds/casa-asteroide.wav')
        
        y = 170
        while not start:
            y -= 0.2
            if y <= 0:
                y = 0
            self.intro_sound.play()
            self.intro_sound.set_volume(0)
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        start = True
                        self.intro_sound.stop()



            self.screen.fill((BLACK))
            self.screen.blit(self.bkg_start, (0, 0))
            self.screen.blit(self.cockpit, (0, 100))
            self.screen.blit(self.text_the_spacex, (500, 100))
            self.screen.blit(self.text_start_game, (450, y+570))
            self.screen.blit(self.text_instructions, (450, y+610))
            self.screen.blit(self.text_credits, (450, y+650))

            pg.display.flip()

        self.status = 'Game'
        
    def score_list(self):
        start = False

        pg.time.set_timer(USEREVENT+1, 20000)
        
        conn = sqlite3.connect('./data/score.db')
        cur = conn.cursor()

        datos = [self.word, self.all_score]
        query = "INSERT INTO score (name, score1) values (?, ?);"
        insert_score = cur.execute(query, datos)

        score_list = []
        query = "SELECT name, score1 FROM score;"
        for x in cur.execute(query):
            score_list += x

        query = "SELECT name, score1 FROM score ORDER BY score1 DESC LIMIT 3;"
        top_list = []
        for y in cur.execute(query):
            top_list += y

        #self.text_select_score = self.font.render("Player: {} | Score: {}".format(score_list[-2:]), True, COLOR_SCORE2)
        self.text_select_score2 = self.font.render("Player: {} | Score: {}".format(top_list[0],top_list[1]), True, COLOR_SCORE2)
        self.text_select_score3 = self.font.render("Player: {} | Score: {}".format(top_list[2],top_list[3]), True, COLOR_SCORE2)
        self.text_select_score4 = self.font.render("Player: {} | Score: {}".format(top_list[4],top_list[5]), True, COLOR_SCORE2)
        conn.commit()
        conn.close()

        self.text_score_player = self.font.render("Congratulations {}, your score is: {}".format(self.word, self.all_score), True, COLOR_SCORE)
        
        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = True
                if event.type == USEREVENT+1:
                    start = True
                       
            self.screen.fill((BLACK))
            self.screen.blit(self.bkg1, (0, 0))
            self.screen.blit(self.escape, (900, 20))
            self.screen.blit(self.cup1, (300, 250))
            self.screen.blit(self.cup2, (300, 350))
            self.screen.blit(self.cup3, (300, 450))
            self.screen.blit(self.text_score_player, (300, 150))
            #self.screen.blit(self.text_select_score, (250, 200))
            self.screen.blit(self.text_select_score2, (400, 300))
            self.screen.blit(self.text_select_score3, (400, 400))
            self.screen.blit(self.text_select_score4, (400, 500))
            
            pg.display.flip()
        
        self.status = 'Start'

    def main_loop(self):
        while True:
            if self.status == 'Game':
                self.loop_game()
            elif self.status == 'Level2':
                self.loop_game()
            elif self.status == 'Level3':
                self.loop_game()
            elif self.status == 'End':
                self.inpt()
            elif self.status == 'Score':
                self.score_list()
            elif self.status == 'Game over':
                self.game_over()
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
