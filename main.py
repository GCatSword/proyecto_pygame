import pygame as pg
from pygame.locals import *
import sys, random, sqlite3
from sprites import *

BLACK = (0,0,0)
COLOR_SCORE = (204, 153, 0)
COLOR_SCORE2 = (204, 0, 0)
COLOR_START = (51, 133, 255)

COLOR_E = (81, 186, 26)
COLOR_N = (189, 210, 30)
COLOR_H = (228, 138, 33)
COLOR_X = (228, 33, 33)

VOLUMEN = 0.5
FPS = 60

class Game:
    def __init__(self):
        # Creación ventana
        self.screen = pg.display.set_mode((1280, 720))
        self.screen.fill(BLACK)

        # Configuración inicial
        self.contador_nivel = 1
        self.contador_vidas = 3
        self.contador_colision = 0
        self.contador_sonido = 0
        self.word = " "
        self.final_score1 = 0
        self.final_score2 = 0
        self.final_score3 = 0
        self.bonus_score = 10
        self.win_game_score = 0 # Puntuación base
        self.win_score_level = 1000 # Puntuación por nivel
        self.angle = 0
        self.n = 0

        # Imagen fondo
        self.bkg3 = pg.image.load("./resources/images/fondo3.jpg")
        self.bkg1 = pg.image.load("./resources/images/fondo444.jpg")
        self.bkg2 = pg.image.load("./resources/images/fondo555.jpg")

        # Imagen vida
        self.live1 = pg.image.load("./resources/images/lives.png")
        self.live2 = pg.image.load("./resources/images/lives.png")
        self.live3 = pg.image.load("./resources/images/lives.png")

        # Imagenes Start
        self.bkg_start = pg.image.load("./resources/images/fondo_start.jpg")
        self.cockpit = pg.image.load("./resources/images/cabina.png")
        
        # Imagenes Score
        self.cup1 = pg.image.load("./resources/images/cup1.png")
        self.cup2 = pg.image.load("./resources/images/cup2.png")
        self.cup3 = pg.image.load("./resources/images/cup3.png")
        
        # Imagenes Info, credits, instruciones, input
        self.image_info = pg.image.load("./resources/images/fondo_info.jpg")

        # Imagenes Difficulty
        self.image_difficulty = pg.image.load("./resources/images/fondo_difficulty.jpg")

        # Música y sonidos
        self.intro_sound = pg.mixer.Sound('./resources/sounds/casa-asteroide.wav')
        self.difficulty_sound = pg.mixer.Sound('./resources/sounds/pax4.wav')
        self.level1_sound = pg.mixer.Sound('./resources/sounds/pax3.wav')
        self.level2_sound = pg.mixer.Sound('./resources/sounds/pax5.wav')
        self.level3_sound = pg.mixer.Sound('./resources/sounds/pax8.wav')
        self.gameover_sound = pg.mixer.Sound('./resources/sounds/pax7.wav')
        self.score_sound = pg.mixer.Sound('./resources/sounds/pax10.wav')
        
        # Status inicial
        self.status = 'Start'

        # Fuentes utilizadas
        self.font_mini = pg.font.Font("./resources/fonts/font.ttf", 20)
        self.font_small = pg.font.Font("./resources/fonts/font.ttf", 30)
        self.font = pg.font.Font("./resources/fonts/font.ttf", 40)
        self.font_big = pg.font.Font('./resources/fonts/font.ttf', 60)
        
        # Textos globales
        self.text_the_spacex = self.font_big.render("The SpaceX", True, COLOR_SCORE)
        self.escape = self.font.render("Press <ESC> for exit", True, COLOR_SCORE)
        self.next = self.font.render("Press <SPACE> for continue", True, COLOR_SCORE)
        
        # Textos input
        self.text_delete = self.font_mini.render('<SUPR> - Delete', True, COLOR_START)
        self.text_accepted = self.font_mini.render('Enter only numbers and letters', True, COLOR_START)

        # Textos Loop_Game
        self.text_score = self.font.render("Score:", True, COLOR_SCORE)
        self.text_winner = self.font_big.render("WINNER", True, COLOR_SCORE2)
        self.score = self.font.render("0", True, COLOR_SCORE)
        self.score_bonus = self.font.render(" ", True, COLOR_SCORE)
        self.text_restart = self.font.render("<R> - Restart level", True, COLOR_SCORE)
        self.level1 = self.font.render("Braxis", True, COLOR_SCORE)
        self.level2 = self.font.render("Aiur", True, COLOR_SCORE)
        self.level3 = self.font.render("Tarsonis", True, COLOR_SCORE)

        # Textos Gameover
        self.text_game_over = self.font_big.render("GAME OVER", True, COLOR_SCORE2)

        # Textos Start
        self.text_start_game = self.font_small.render('<SPACE> - Start game', True, COLOR_SCORE)
        self.text_instructions = self.font_small.render('<I> - Instructions', True, COLOR_SCORE)
        self.text_credits = self.font_small.render('<C> - Credits', True, COLOR_SCORE)
        self.text_puntuation = self.font_small.render('<H> - Hall of Fame', True, COLOR_SCORE)
        
        # Textos Info
        self.text_info1 = self.font_mini.render("Welcome to the SpaceX project", True, COLOR_START)
        self.text_info2 = self.font_mini.render("As you know, planet earth is in decline because of global warming", True, COLOR_START)
        self.text_info3 = self.font_mini.render("The world's best experts have come together to create the SpaceX project", True, COLOR_START)
        self.text_info4 = self.font_mini.render("The goal is to save humanity from inevitable extinction", True, COLOR_START)
        self.text_info5 = self.font_mini.render("We have high hopes of finding a habitable planet in the TRAPPIST-1 system", True, COLOR_START)
        self.text_info6 = self.font_mini.render("Let's not waste any more time! You must board immediately", True, COLOR_START)
        self.text_info7 = self.font_mini.render("Choose well the way to go and discover the secret (Easy, Normal, Hard, Xtrem)", True, COLOR_START)
        self.text_control = self.font_mini.render("Spaceship controls:", True, COLOR_SCORE)
        self.text_controlW = self.font_mini.render("<W> - Move up spaceship", True, COLOR_SCORE)
        self.text_controlS = self.font_mini.render("<S> - Move down spaceship", True, COLOR_SCORE)
        self.text_controlL = self.font_mini.render("<L> - Rotate...", True, COLOR_SCORE)
        self.text_controlUP = self.font_mini.render("<UP> - Move up...", True, COLOR_SCORE)
        self.text_controlDOWN = self.font_mini.render("<DOWN> - Move down...", True, COLOR_SCORE)
        self.text_controlLEFT = self.font_mini.render("<LEFT> - Move left...", True, COLOR_SCORE)
        self.text_controlRIGHT = self.font_mini.render("<RIGHT> - Move right...", True, COLOR_SCORE)
        
        # Textos Credits
        self.text_creator = self.font_small.render('Game creator: Genís Moix', True, COLOR_START)
        self.text_music = self.font_small.render('Game music: Pax una aventura espacial - Jaime Altozano', True, COLOR_START)
        self.text_translator = self.font_small.render('Translation: Google Translator :)', True, COLOR_START)
        self.text_game_created = self.font_small.render('Game created in Pygame', True, COLOR_START)

        # Texto Hall of Fame
        self.text_hall_of_fame = self.font_big.render('Hall of Fame', True, COLOR_SCORE)

        # Textos diffuculty
        self.text_easy = self.font_small.render("<E> - Easy", True, COLOR_E)
        self.text_normal = self.font_small.render("<N> - Normal", True, COLOR_N)
        self.text_hard = self.font_small.render("<H> - Hard", True, COLOR_H)
        self.text_xtrem = self.font_small.render("<X> - eXtrem", True, COLOR_X)
        self.text_difficulty = self.font.render("Choose the difficulty", True, COLOR_SCORE)

        pg.display.set_caption("SpaceX")


    def handlenEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()

            if not self.score_time == self.win_game_score:
                if self.contador_colision >= 1:
                    self.ship.vy = 0
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_w:
                            self.ship.vy = -1
                        elif event.key == K_s:
                            self.ship.vy = 1
            else:           
                self.ship.vy = 0 
                if event.type == KEYDOWN:     
                    if event.key == K_UP:
                        self.astronaut.vy = -1
                    elif event.key == K_DOWN:
                        self.astronaut.vy = 1
                    elif event.key == K_LEFT:
                        self.astronaut.vx = -1
                    elif event.key == K_RIGHT:
                        self.astronaut.vx = 1
                    elif event.key == K_l:
                        self.angle +=1

        if not self.score_time == self.win_game_score:
            if self.contador_colision >= 1:
                    self.ship.vy = 0
            else:
                key_pressed = pg.key.get_pressed()
                if key_pressed[K_w]:
                    self.ship.vy -= 1
                elif key_pressed[K_s]:
                    self.ship.vy += 1
                else:
                    self.ship.vy = 0 
        else:
            self.ship.vy = 0
            key_pressed = pg.key.get_pressed()
            if key_pressed[K_UP]:
                self.astronaut.vy -= 0.5
            elif key_pressed[K_DOWN]:
                self.astronaut.vy += 0.5
            elif key_pressed[K_LEFT]:
                self.astronaut.vx -= 0.5
            elif key_pressed[K_RIGHT]:
                self.astronaut.vx += 0.5
            elif key_pressed[K_l]:
                self.angle +=5
            else:
                self.astronaut.vy = 0
                self.astronaut.vx = 0

        return False

    def render(self):
        # Movimiento del fondo
        if self.contador_nivel == 1:
            self.screen.blit(self.bkg1, (self.x, 0))
            self.screen.blit(self.bkg1, (self.x+2560, 0))
        if self.contador_nivel == 2:
            self.screen.blit(self.bkg2, (self.x, 0))
            self.screen.blit(self.bkg2, (self.x+2560, 0))
        if self.contador_nivel == 3:
            self.screen.blit(self.bkg3, (self.x, 0))
            self.screen.blit(self.bkg3, (self.x+2560, 0))
        
        self.allSprites.draw(self.screen)

        self.screen.blit(self.text_score, (10, 20))
        self.screen.blit(self.score, (150, 20))
        self.screen.blit(self.escape, (900, 20))
        
        # Mostrar vidas
        if self.contador_vidas == 3:
            self.screen.blit(self.live1, (270, -10))
            self.screen.blit(self.live2, (340, -10))
            self.screen.blit(self.live3, (410, -10))
        if self.contador_vidas == 2:
            self.screen.blit(self.live1, (270, -10))
            self.screen.blit(self.live2, (340, -10))
        if self.contador_vidas == 1:
            self.screen.blit(self.live1, (270, -10))

        # Mostrar puntuación
        if self.contador_nivel == 1:
            self.score = self.font.render(str(self.final_score1), True, COLOR_SCORE2)
            self.screen.blit(self.level1, (550, 20))
        if self.contador_nivel == 2:
            self.score = self.font.render(str(self.final_score2), True, COLOR_SCORE2)
            self.screen.blit(self.level2, (550, 20))
        if self.contador_nivel == 3:
            self.score = self.font.render(str(self.final_score3), True, COLOR_SCORE2)
            self.screen.blit(self.level3, (550, 20))

        # Mostrar continue + restart
        if self.score_time == self.win_game_score:
            self.screen.blit(self.next, (400, 650))
            if self.contador_nivel == 3 and self.difficulty == 'Xtrem':
                self.score_bonus = self.font.render(str(self.bonus_score), True, COLOR_SCORE)
                self.screen.blit(self.score_bonus, (150, 60))
        if self.contador_colision > 0 and self.contador_vidas >= 1:   
            self.screen.blit(self.text_restart, (500, 500))
            
        pg.display.flip()

    def config_levels(self):
        if FPS == 30:
            self.reset_tiempo = 5
            self.win_score_level = 1000
        elif FPS == 60:
            self.reset_tiempo = 10
            self.win_score_level = 2000
        elif FPS == 120:
            self.reset_tiempo = 20
            self.win_score_level = 4000

        # Configuración de los niveles
        if self.difficulty == 'Easy':
            self.multiplier = 1
        elif self.difficulty == 'Normal':
            self.multiplier = 1.4
        elif self.difficulty == 'Hard':
            self.multiplier = 1.6
        elif self.difficulty == 'Xtrem':
            self.multiplier = 2.2

        if self.contador_nivel >= 4:
            self.contador_nivel = 1
            self.contador_vidas = 3
            self.win_game_score = 0
            self.bonus_score = 0

        if self.contador_nivel == 1:
            self.planet1 = Planet(1)
            self.planetsGroup.add(self.planet1)
            self.spawn_enemy = 400
            self.spawn_time = 0
            self.final_score1 = 0
            self.level1_sound.play(-1)
            self.level1_sound.set_volume(VOLUMEN)
            self.restar_tiempo = 0.1 * self.multiplier
        if self.contador_nivel == 2:
            self.planet2 = Planet(2)
            self.planetsGroup.add(self.planet2)
            self.spawn_enemy = 600
            self.spawn_time = 0
            self.final_score2 = 0
            self.level2_sound.play(-1)
            self.level2_sound.set_volume(VOLUMEN)
            self.restar_tiempo = 0.2 * self.multiplier
        if self.contador_nivel == 3:
            self.planet3 = Planet(3)
            self.planetsGroup.add(self.planet3)
            self.spawn_enemy = 1200
            self.spawn_time = 0
            self.final_score3 = 0
            self.level3_sound.play(-1)
            self.level3_sound.set_volume(VOLUMEN)
            self.restar_tiempo = 0.3 * self.multiplier

    def loop_game(self):
        gameover = False
        self.score_time = 1
        self.bonus_score = 0
        self.x = 0
        self.y = 0

        # Música y sonidos
        pg.mixer.set_num_channels(3)
       
        # Crear reloj
        self.clock = pg.time.Clock()
              
        # Grupos Sprites
        self.ship = SpaceShip(100, 350)
        self.playerGroup = pg.sprite.Group()
        self.playerGroup.add(self.ship)

        self.astronaut = Astronaut(660, 350)
        self.playerGroup2 = pg.sprite.Group()
        self.playerGroup2.add(self.astronaut)

        self.planetsGroup = pg.sprite.Group()
        self.enemySprites = pg.sprite.Group()
        self.enemyBonus = pg.sprite.Group()

        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.playerGroup)

        # Configuración niveles
        self.config_levels()
 
        # Puntuación
        self.win_game_score = self.win_score_level * self.contador_nivel * self.multiplier
        self.win_game_score = round(self.win_game_score)

        while not gameover:
            gameover = self.handlenEvent()
            #self.clock.tick(FPS)
            self.clock.tick_busy_loop(FPS) # + preciso pero + CPU
            
            # Partida (score final no obtenido)
            if not self.score_time == self.win_game_score:
                # Spawn enemigos/obstaculos
                self.spawn_time -= self.restar_tiempo
                
                if self.spawn_time <= 0 and self.spawn_enemy > 0:
                    self.spawn_enemy -= 1
                    self.spawn_time = self.reset_tiempo 
                    self.enemySprites.add(Enemy())
                    self.allSprites.add(self.enemySprites)
                    print(self.spawn_enemy)
                colisiones = self.ship.checkCollision(self.enemySprites, FPS)
                # Condiciones cuando hay colision
                for colision in colisiones:
                    self.contador_colision += 1
                    self.spawn_enemy = 0
                    self.score_time = 0
                
                if self.contador_colision < self.score_time:
                    self.score_time += 1 # Sumar puntuación

                    # Movimiento fondo
                    self.x -= 2
                    if self.x <= - 2560:
                        self.x = 0
  
                # Restar vida
                if self.contador_colision == 1:
                    self.contador_vidas -= 1
                    
                # Restart nivel
                if self.contador_colision > 0 and self.contador_vidas >= 1: 
                    key_pressed = pg.key.get_pressed()
                    if key_pressed[K_r]:
                        pg.mixer.stop()
                        self.contador_colision = 0
                        gameover = True

                # Render puntuación
                self.score = self.font.render(str(self.score_time), True, COLOR_SCORE)
           
            # Partida (score final obtenido) 
            if self.score_time == self.win_game_score:
                self.allSprites.add(self.planetsGroup)
                self.ship.landing()
                
                # Passar nivel        
                key_pressed = pg.key.get_pressed()
                if key_pressed[K_SPACE]:
                    self.contador_nivel +=1
                    pg.mixer.stop()
                    gameover = True

                # Juego bonus
                if self.contador_nivel == 3 and self.difficulty == 'Xtrem':
                    self.allSprites.add(self.playerGroup2)
                    self.astronaut.rotate(self.angle)
                    self.spawn_time -= self.restar_tiempo
                    
                    if self.spawn_time <= 0 and self.spawn_enemy > 0:
                        self.spawn_enemy -= 1
                        self.spawn_time = self.reset_tiempo
                        self.enemyBonus.add(EnemyBonus())
                        self.allSprites.add(self.enemyBonus)
                        aliens = self.astronaut.checkCollision(self.enemyBonus)
                        for alien in aliens:
                            self.bonus_score += 10

            # Update ALL sprites
            self.allSprites.update(1280,720)
                 
            # Puntuaciones por nivel
            if self.contador_nivel == 1: # Cada nivel suma 500
                self.final_score1 = self.score_time + 500  
            if self.contador_nivel == 2:
                self.final_score2 = self.score_time + 1000  
            if self.contador_nivel == 3:
                if self.contador_vidas == 3: # Cada vida suma 200
                    self.final_score3 = self.score_time + 1500 + 600
                if self.contador_vidas == 2:
                    self.final_score3 = self.score_time + 1500 + 400
                if self.contador_vidas == 1:
                    self.final_score3 = self.score_time + 1500 + 200
            # Puntuación total
            self.all_score = self.final_score1 + self.final_score2 + self.final_score3 + self.bonus_score
            
            # Salir partida
            key_pressed = pg.key.get_pressed()
            if key_pressed[K_ESCAPE]:
                pg.mixer.stop()
                self.contador_colision = 0
                self.contador_nivel = 5
                gameover = True
            # Render
            self.render()
                    
        if self.contador_nivel == 2:
            self.status = "Level2"
        elif self.contador_nivel == 3:
            self.status = "Level3"
        elif self.contador_nivel == 4:
            self.status = "End"
        elif self.contador_nivel <= 4 and self.contador_vidas > 0:
            self.status = "Game"
        elif self.contador_nivel == 5:
            self.status = "Game over"
        else:
            self.status = 'Start'

    def game_over(self):
        start = False

        pg.mixer.set_num_channels(1)
        pg.time.set_timer(USEREVENT+1, 20000)

        while not start:
            self.gameover_sound.play(0)
            self.gameover_sound.set_volume(VOLUMEN)
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.mixer.stop()
                        start = True

                if event.type == USEREVENT+1:
                    pg.mixer.stop()
                    start = True

            self.screen.fill((BLACK))
            if self.contador_nivel == 2:
                self.screen.blit(self.bkg1, (0, 0))
            if self.contador_nivel == 3:
                self.screen.blit(self.bkg2, (0, 0))
            if self.contador_nivel >= 4:
                self.screen.blit(self.bkg3, (0, 0))
            self.screen.blit(self.text_game_over, (480, 300))
            self.screen.blit(self.escape, (900, 20))
            self.text_input(":( your score is: {}".format(self.all_score), 450, 400, COLOR_SCORE)
            
            pg.display.flip()
       
        self.status = 'Start'
     
    def start_game(self):
        start = False
        intro = 0
        y = 170
        pg.time.set_timer(USEREVENT+1, 20000)
        pg.mixer.set_num_channels(1)
       
        while not start:    
            self.intro_sound.play(-1)
            self.intro_sound.set_volume(VOLUMEN)
            
            y -= 0.3
            if y <= 0:
                y = 0
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        intro = 1
                        start = True                       
                    if event.key == K_i:
                        intro = 2
                        start = True
                    if event.key == K_c:
                        intro = 3
                        start = True
                    if event.key == K_h:
                        intro = 4
                        start = True

                if event.type == USEREVENT+1:
                    intro = 4
                    start = True

            lista = [(self.bkg_start, (0, 0)),
                    (self.cockpit, (0, 100)),
                    (self.text_the_spacex, (500, 100)),
                    (self.text_start_game, (480, y+550)),
                    (self.text_instructions, (480, y+590)),
                    (self.text_credits, (480, y+630)),
                    (self.text_puntuation, (480, y+670))
                    ]

            self.screen.blits(lista)

            pg.display.flip()

        if intro == 1:
            pg.mixer.stop()
            self.status = 'Difficulty'
        if intro == 2:
            self.status = 'Info'
        if intro == 3:
            self.status = 'Credits'
        if intro == 4:
            self.status = 'Hall of fame'

    def text_input(self, word, x, y, color):
        text = self.font.render("{}".format(word), True, color)
        return self.screen.blit(text,(x,y))

    def inpt(self):
        self.word=""
        done = False
        Key_accepted = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"

        while not done:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if len(self.word) <= 2 and (event.key) and str.upper((chr(event.key))) in Key_accepted:
                            self.word += str.upper((chr(event.key)))
                            
                    if event.key == K_DELETE:
                        x = len(self.word)
                        self.word = self.word[:-x]
                    if event.key == K_SPACE:
                        intro = 2
                        done=True
                    if event.key == K_ESCAPE:
                        intro = 1
                        done=True


            lista = [(self.image_info, (0, 0)),
                    (self.escape, (900, 20)),
                    (self.next, (400, 650)),
                    (self.text_delete, (800, 500)),
                    (self.text_accepted, (300, 500)),
                    ]

            self.screen.blits(lista)

            self.text_input("Please enter your name", 450, 170, COLOR_SCORE)
            self.text_input("{}".format(self.word), 590, 300, COLOR_SCORE2)

            pg.display.flip()

        if intro == 1:
            self.status = "Start"
        if intro == 2:
            self.status = "Score"

    def score_list(self):
        start = False
        self.score_sound.play(0)
        self.score_sound.set_volume(VOLUMEN)
        pg.time.set_timer(USEREVENT+1, 20000)
        
        conn = sqlite3.connect('./data/score.db')
        cur = conn.cursor()

        datos = [self.word, self.all_score, self.final_score1, self.final_score2, self.final_score3]
        query = "INSERT INTO score (name, total, score1, score2, score3) values (?, ?, ?, ?, ?);"
        insert_score = cur.execute(query, datos)

        query = "SELECT name, total FROM score ORDER BY total DESC LIMIT 3;"
        tops = cur.execute(query)

        top_list = []
        for top in tops:
            top_list += top
       
        conn.commit()
        conn.close()

        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.mixer.stop()
                        start = True
                if event.type == USEREVENT+1:
                    pg.mixer.stop()
                    start = True
                       
            lista = [(self.bkg3, (0, 0)),
                    (self.escape, (900, 20)),
                    (self.cup1, (350, 250)),
                    (self.cup2, (350, 350)),
                    (self.cup3, (350, 450)),
                    ]
            self.screen.blits(lista)

            self.text_input("Congratulations {}, your score is: {}".format(self.word, self.all_score), 300, 150, COLOR_SCORE)

            try:
                self.text_input("Player: {} | Score: {}".format(top_list[0],top_list[1]), 450, 300, COLOR_SCORE2)
                self.text_input("Player: {} | Score: {}".format(top_list[2],top_list[3]), 450, 400, COLOR_SCORE2)
                self.text_input("Player: {} | Score: {}".format(top_list[4],top_list[5]), 450, 500, COLOR_SCORE2)
            except:
                pass

            pg.display.flip()
        
        self.status = 'Start'

    def game_info(self):
        start = False

        pg.time.set_timer(USEREVENT+1, 60000)

        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == USEREVENT+1:
                    start = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = True

            lista = [(self.image_info, (0, 0)),
                    (self.text_the_spacex, (500, 50)),
                    (self.escape, (900, 20)),
                    (self.text_info1, (270, 200)),
                    (self.text_info2, (270, 230)),
                    (self.text_info3, (270, 260)),
                    (self.text_info4, (270, 290)),
                    (self.text_info5, (270, 320)),
                    (self.text_info6, (270, 350)),
                    (self.text_info7, (270, 380)),
                    (self.text_control, (270, 470)),
                    (self.text_controlW, (470, 440)),
                    (self.text_controlS, (470, 470)),
                    (self.text_controlL, (470, 500)),
                    (self.text_controlUP, (750, 420)),
                    (self.text_controlDOWN, (750, 450)),
                    (self.text_controlLEFT, (750, 480)),
                    (self.text_controlRIGHT, (750, 510))
                    ]

            self.screen.blits(lista)

            pg.display.flip()

        self.status = 'Start'

    def credits(self):
        start = False
        intro = 0
        y = 100
        
        pg.time.set_timer(USEREVENT+1, 30000)

        while not start:
            y -= 0.2
            if y <= 0:
                y = 0
            
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == USEREVENT+1:
                    start = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = True
                    
            lista = [(self.image_info, (0, 0)),
                    (self.escape, (900, 20)),
                    (self.text_the_spacex, (500, y+170)),
                    (self.text_creator, (270, y+270)),
                    (self.text_music, (270, y+320)),
                    (self.text_translator, (270, y+370)),
                    (self.text_game_created, (270, y+420))
                    ]

            self.screen.blits(lista)

            pg.display.flip()

        self.status = 'Start'

    def hall_of_fame(self):
        start = False
        pg.time.set_timer(USEREVENT+1, 20000)
        
        conn = sqlite3.connect('./data/score.db')
        cur = conn.cursor()

        query = "SELECT name, total FROM score ORDER BY total DESC LIMIT 3;"
        tops = cur.execute(query)

        top_list = []
        for top in tops:
            top_list += top
     
        while not start:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == USEREVENT+1:
                    start = True

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        start = True
                    if event.key == K_DELETE:
                        cur.execute("DELETE FROM score;")
                        start = True
                 
            lista = [(self.bkg3, (0, 0)),
                    (self.escape, (900, 20)),
                    (self.cup1, (350, 250)),
                    (self.cup2, (350, 350)),
                    (self.cup3, (350, 450)),
                    (self.text_hall_of_fame, (500, 150)),
                    (self.text_delete, (1100, 680))
                    ]

            self.screen.blits(lista)
                        
            try:
                self.text_input("Player: {} | Score: {}".format(top_list[0],top_list[1]), 450, 300, COLOR_SCORE2)
                self.text_input("Player: {} | Score: {}".format(top_list[2],top_list[3]), 450, 400, COLOR_SCORE2)
                self.text_input("Player: {} | Score: {}".format(top_list[4],top_list[5]), 450, 500, COLOR_SCORE2)
            except:
                pass
            
            pg.display.flip()

        conn.commit()
        conn.close()
        
        self.status = 'Start'

    def game_difficulty(self):
        start = False
        pg.time.set_timer(USEREVENT+1, 90000)
        pg.mixer.set_num_channels(1)

        while not start:
            for event in pg.event.get():
                self.difficulty_sound.play(-1)
                self.difficulty_sound.set_volume(VOLUMEN)
                if event.type==pg.QUIT:
                    self.quit()

                if event.type == USEREVENT+1:
                        intro = 1
                        start = True

                if event.type == KEYDOWN:
                    if event.key == K_e:
                        intro = 2
                        self.difficulty = 'Easy'
                        start = True                       
                    if event.key == K_n:
                        intro = 2
                        self.difficulty = 'Normal'
                        start = True
                    if event.key == K_h:
                        intro = 2
                        self.difficulty = 'Hard'
                        start = True
                    if event.key == K_x:
                        intro = 2
                        self.difficulty = 'Xtrem'
                        start = True
                    if event.key == K_ESCAPE:
                        intro = 1
                        start = True
                    
            lista = [(self.image_difficulty, (0, 0)),
                    (self.escape, (900, 20)),
                    (self.text_difficulty, (450, 100)),
                    (self.text_easy, (280, 250)),
                    (self.text_normal, (280, 420)),
                    (self.text_hard, (800, 250)),
                    (self.text_xtrem, (800, 420))
                    ]

            self.screen.blits(lista)

            pg.display.flip()

        if intro == 1:
            pg.mixer.stop()
            self.status = "Start"
        if intro == 2:
            pg.mixer.stop()
            self.status = "Game"

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
            elif self.status == 'Info':
                self.game_info()
            elif self.status == 'Credits':
                self.credits()
            elif self.status == 'Hall of fame':
                self.hall_of_fame()
            elif self.status == 'Difficulty':
                self.game_difficulty()
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
