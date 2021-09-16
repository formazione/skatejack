import pygame, time, random, math
from pygame.locals import *
from numba import jit
# THE LEVELS ARE HERE, they
# are created by this program with 's'

from locals.randomize_crystals import *


RED = (255, 0, 0) 
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
# Creating the list with particles ready to be drawn

particles3 = []
@jit
def fire(crd1, crd2, number=5, color=1):
    ''' a certain number of particles '''
    # mx, my = pygame.mouse.get_pos()


    for i in range(number):
        particles3.append([[crd1, crd2], 
            [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], 
            random.randint(1, 4)])
    # screen.fill((0,0,0))
    for particle in particles3:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= .1
        particle[1][1] += 0.15
        c1 = random.randrange(200,255)
        c2 = random.randrange(100,255)
        c3 = random.randrange(100,255)
        if color == 1:
            color = (c1,c2,c3)
        elif color == 2:
            color = (c1,c2,0)
        if particle[2] <= 0:
            particles3.remove(particle)
        pygame.draw.circle(screen, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))


def init():

    pygame.init()
    pygame.display.init()
    pygame.mixer.init()



# this function randomize the crystals
layout = randomize_crystals()
COUNTDOWN_LIMIT = 2000
init()

screen_ratio = 3
display = pygame.display.set_mode((480*screen_ratio + 64, 288*screen_ratio))
screen = pygame.Surface((480, 288))
pygame.display.set_caption("Crystals of Time by SmellyFrog")

# ================ I M A G E S =============== LOAD into Surfaces =====
spr_player = pygame.image.load("assets/player6.png").convert_alpha()
# ======================= IMAGES ==============================
player_rect = spr_player.get_rect()
ball1 = pygame.image.load("assets/ball1.png").convert_alpha()
ball2 = pygame.image.load("assets/ball2.png").convert_alpha()
spr_tiles = pygame.image.load("assets/tiles4.png").convert_alpha()
NUM_OF_TILES = spr_tiles.get_size()[0] // 32
spr_crystal1 = pygame.image.load("assets/crystal.png").convert_alpha()
spr_crystal2 = pygame.image.load("assets/crystal2.png").convert_alpha()
spr_particle = pygame.image.load("assets/particles.png").convert_alpha()
spr_number = pygame.image.load("assets/number.png").convert_alpha()
background = pygame.image.load("assets/background.png").convert()
title = pygame.image.load("assets/title.png").convert()

# ==================== SOUNDS ========================
sfx_crash = pygame.mixer.Sound("assets/crash.wav")
# sfx_crash.set_volume(0.5)
sfx_collect = pygame.mixer.Sound("assets/collect.wav")
sfx_crystal = pygame.mixer.Sound("assets/crystal.wav")
jump = pygame.mixer.Sound("assets/jump.mp3")

# THE SPRITE FOR THE PLAYER
class Player():
    def __init__(self, x, y):
       
        # Position
        self.x = x
        self.y = y
        # Speed
        self.xSpeed = 0
        self.ySpeed = 0
        # immagine iniziale
        self.frame = 0
        self.faceRight = True # rivolto a destra
        self.timer = 0
        self.jump_once = 0 # l'ho messo io per il doppio salto che non funziona più
        self.collision_reset()

    def collision_reset(self):
        self.bottomCollision = False
        self.topCollision = False
        self.leftCollision = False
        self.rightCollision = False

    def inertial_speed(self):
        if self.xSpeed > 0.3:
            self.xSpeed -= 0.2
        elif self.xSpeed < 0.3:
            self.xSpeed += 0.2
        else:
            self.xSpeed = 0
    def update(self):
        global comic_time

        self.x += self.xSpeed
        self.y += self.ySpeed
        if self.ySpeed < 8:
            self.ySpeed += 0.5


        if self.bottomCollision: # quando c'è un tile sotto non cade
            self.ySpeed = 0 # non cade
            # decelera in orizzontale (si trova sopra a 207)
            self.inertial_speed()

        # JUMP
        if keys[pygame.K_x] and self.bottomCollision:# or self.rightCollision or self.leftCollision):# and not self.topCollision:
            if self.jump_once < 1:
        # if keys[pygame.K_UP] and self.bottomCollision:
                if abs(self.xSpeed) > .5:
                    self.ySpeed = -8
                    self.jump_once += .5
                    pygame.mixer.Sound.play(jump)
                    # comic("Double jump")
                    self.bottomCollision = 0
                else:
                    comic("RUN")

        elif keys[pygame.K_LEFT] and self.xSpeed > -3:
            self.xSpeed -= 0.2
            self.faceRight = False
            self.frame = (timer % 16 < 8) # is 1 or 0
        elif keys[pygame.K_RIGHT] and self.xSpeed < 3:
            self.xSpeed += 0.2
            self.faceRight = True
            self.frame = (timer % 16 < 8) # is 1 or 0
        # else:
        # IT'S IN THE AIR ----------------- ATTEMPT TO MAKE AN ANIMATION
        if not self.bottomCollision and abs(self.ySpeed) > 1:
            self.frame = 1 + (timer % 16 < 1) # ADDED THIS TO ANIMATE IT?
        if self.timer > 0:
            self.frame = (timer % 16 < 8) + 3
            
        self.collision_reset()

            
    def draw(self):

        screen.blit(
            spr_player, 
            (int(self.x), int(self.y)),
            # Here is where he gets the sprite from the spritesheet
            (self.frame * 32, # x position for the pose
            (not self.faceRight) * 32, # y position 0 = left 1=left
            32, 32))
        # pygame.draw.rect(display, (0, 255, 0), (int(self.x), int(self.y), 32, 32))

class Terrain():
    def __init__(self, x, y, Type, level):
        self.x = x
        self.y = y
        self.level = level
        self.col = False
        self.type = Type
    def update(self):
        # Se il giocatore si trova sopra ad un tile... cos'è self.col



        if self.type == 4:
            if player.x + 31 > self.x and player.x < self.x + 16:# and not self.col:
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    player.ySpeed = -10
                    player.bottomCollision = False
                    pygame.mixer.Sound.play(jump)
                    remove.append(self)


        if self.type == 5:
            if player.x + 31 > self.x and player.x < self.x + 16:# and not self.col:
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    # player.ySpeed = +3
                    player.bottomCollision = False
                    pygame.mixer.Sound.play(sfx_collect)
                    remove.append(self)


        # il terzo gruppo di tiles
        elif self.level == 64:
            if player.x + 16 > self.x and player.x < self.x + 31 and not self.col: # collition with self?
            # Se i piedi del player si trovano all'altezza del tile, cioè sopra...
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    # il player viene piazzato esattamente sopra il tile
                    player.y = self.y - 32 # sarebbe che il player si trova 32 pixel sopra la base del tile
                    player.ySpeed = 0
                    player.bottomCollision = True # Collition with the bottom, the player is on the terrain
                    self.col = True #Vuol dire che il tile è in contatto con il player
                    player.jump_once = 0
                    
        
        else:
            if player.x + 16 > self.x and player.x < self.x + 31 and not self.col: # collition with self?
            # Se i piedi del player si trovano all'altezza del tile, cioè sopra...
                if player.y + 32 > self.y and player.y + 32 < self.y + 16:
                    # il player viene piazzato esattamente sopra il tile
                    player.y = self.y - 32 # sarebbe che il player si trova 32 pixel sopra la base del tile
                    player.ySpeed = 0
                    player.bottomCollision = True # Collition with the bottom, the player is on the terrain
                    self.col = True #Vuol dire che il tile è in contatto con il player
                    player.jump_once = 0

                    # Tipes of tiles

                    # BACK
                    if self.type == 3:
                        player.x -= 96
                        pygame.mixer.Sound.play(sfx_crystal)



                if player.x > self.x and player.x < self.x + 31:
                    if player.y > self.y + 16 and player.y < self.y + 31:
                        player.y = self.y + 31
                        player.ySpeed = 0 # non salta più
                        player.topCollision = True # collide col tile verso l'alto
                        self.col = True # la collisione del player c'è
            

            if player.y + 31 == self.y + 31 and not self.col:

                if player.x + 31 > self.x and player.x + 31 < self.x + 16:
                    player.x = self.x - 32
                    player.xSpeed = -0.4
                    player.rightCollision = True
                    self.col = True
                # COLLITION LEFT
                if player.x > self.x + 16 and player.x < self.x + 31:
                    player.x = self.x + 31
                    player.xSpeed = 0.4
                    player.leftCollision = True
                    self.col = True
            self.col = False
        
    def draw(self):
        # this blits the tiles at the position, but starting with 6*32 end ending 32 further
        if self not in remove:
            if self.type == 4:
                screen.blit(spr_tiles, (int(self.x), int(self.y)+ (timer % 16 < 8)), (self.type * 32, 0 + self.level, 32, 32))
                # screen.blit(spr_tiles, (int(self.x)+ (timer % 16 < 8), int(self.y)+ (timer % 16 < 8)), (self.type * 32 + (timer % 16 < 8) * 32, 0 + self.level, 32, 32))
            else:
                screen.blit(spr_tiles, (int(self.x), int(self.y)), (self.type * 32, 0 + self.level, 32, 32))

def rnd():
    return random.randrange(200,255), random.randrange(100,255), random.randrange(100,255)

class Crystal():
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
        self.particles3 = []
    def update(self):
        global countdown
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < 32 and countdown > 0:
            collected.append((self.x, self.y, room_num))
            print(f"Collezionate: {len(collected)} gemme")
            comic_time = 100
            comic(f"{len(collected)}")
            player.timer = 15
            countdown += 150
            

            player.xSpeed = 0
            pygame.mixer.Sound.play(sfx_collect)
        if (self.x, self.y, self.num) in collected:
            remove.append(self)



    def fire(self, crd1, crd2, number=5, color=1):
        for i in range(number):
            self.particles3.append([[crd1, crd2], 
                [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], 
                random.randint(1, 3)])
        for particle in self.particles3:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= .1
            particle[1][1] += 0.15
            if particle[2] <= 0:
                self.particles3.remove(particle)
            pygame.draw.circle(screen, rnd(), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

            
    def draw(self):
        if not self in remove:
            # fire(int(self.x)+15, int(self.y) + math.sin(timer*3 / 32) * 16 +15, number=5, color=2)

            self.fire(int(self.x) + math.cos(timer / 32) * random.randrange(8, 16, 8) +5,
             int(self.y) + math.sin(timer / 16) * 16 + 5,
             number=5, color=2)
            screen.blit(ball1, ((int(self.x) + math.cos(timer / 32) * random.randrange(8, 16, 8)), int(self.y) + math.sin(timer / 16) * 16), ((timer % 16 < 16) * 32, 0, 32, 32))


def game_over():
    """ Call this when the player game ends """
    display.fill(0)
    alive = False
    room_num = 0
    player_y = 42069
    countdown = COUNTDOWN_LIMIT
    player_x = 42069
    collected.clear()


   
player_y = 42069
player_x = 42069
collected = []
room_num = 0
timer = 0
countdown = COUNTDOWN_LIMIT
run = True

room_r = len(layout[room_num])
room_c = len(layout[room_num][0])

def music_on():
    music = pygame.mixer.music.load("assets/swinging in the night sky2.wav")
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1)

music_on()
color_line = 255, 255, 0
font = pygame.font.SysFont("Arial", 20)
def room_number():
    rn = font.render(f"{room_num}", 1, (255, 255, 255))
    return rn


def change_room():
    global room_num, player_x, player_y

    if player.x + 16 < 0:
        player_y = player.y
        player_x = 480 - 24
        room_num -= 1
    elif player.x + 16 > 480:
        player_y = player.y
        player_x = -8
        room_num += 1
    if player.y > 288:
        player.y = 0

def time_indicator():
    pygame.draw.line(screen, (200, 255, 255), (239, 280 - (countdown // 7)), (239, -4), 6)
    pygame.draw.circle(screen, (200, 255, 255), (240, 280 - (countdown // 7)), 8)
    pygame.draw.circle(screen, (255, 255, 255), (240, 280 - (countdown // 7)), 4)

font = pygame.font.SysFont("Arial", 14)
msg = font.render("Hello", 1, (0, 255, 0))
def message(text):
    global msg
    # screen0.fill(0, (0, 288, 480, 32))
    msg = font.render(text, 1, (0, 255, 0))
    return msg

comic_time = 100
mess = ">>>"
def comic(x):
    global comic_time

    if comic_time > 0:
        screen.blit(message(x), (player.x, player.y - 15))
    else:
        comic_time = 100
    print(f"{comic_time=}")


@jit
def show_map(player):
    for i in range(room_r):
        for j in range(room_c): # ================= Put the plauer in position
            if layout[room_num][i][j] == "P":
                player = Player(j*32, i*32)
                load.append(player)
                # ========================================== Here go the tiles
            elif layout[room_num][i][j] != " ":# and layout[room_num][i][j] != "P":
                if int(layout[room_num][i][j]) < 100:
                    level = 0
                    val = int(layout[room_num][i][j])
                    # if val == 10:
                    #     pass
                    if val > 10 and val < 22:
                        val = val - 11
                        level = 32
                        load.append(Terrain(j*32, i*32, val, level))
                    elif val > 20:
                        val = val - 22
                        level = 64
                        load.append(Terrain(j*32, i*32, val, level))
                    else:
                        load.append(Terrain(j*32, i*32, val, level))
                    # ======================================= CRYSTAL
                elif layout[room_num][i][j] == "100":
                    load.append(Crystal(j*32, i*32, room_num))
                elif layout[room_num][i][j] == "101":
                    load.append(LargeCrystal(j*32, i*32))

    if player not in load:# and room_num not in (0, 14, 15):
        load.append(player)

    return player

while run:
    ### level generation

    load = []
    remove = []
    player = Player(0, 0)

    player = show_map(player)


    if player_y != 42069:
        player.y = player_y
        player.x = player_x



    
    clock = pygame.time.Clock()
    alive = True
    while run and alive:


        comic_time -= 1
        timer += 1
        # Countdown starts from second room
        if countdown <= 3000 and room_num >= 1:
            countdown -= 1

        clock.tick(60)

        screen.fill((0, 0, 0))
        if room_num == 0:
            screen.blit(title, (0, 0))
        else:
            screen.blit(background, (0, 0))

        # meteor

        # WHEN TIME'S OVER
        if countdown == 0:
            pygame.mixer.Sound.play(sfx_crash)
            pygame.mixer.music.stop()
        # This draws the the circle
        if countdown < 0:
            pygame.draw.circle(screen, (255, 255, 255), (240, 204), -10 * countdown)
        if countdown < -100:
            alive = False
            room_num = 0
            countdown = 1500
            player_y = 42069
            player_x = 42069
            collected = []

        if player.timer > 0:
            player.timer -= 1
            countdown += 11
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # 
        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            
            load.remove(obj)
        # load = []
        remove = []

        if player.x + 16 > 480 or player.x + 16 < 0:
            alive = False

        # counter

        if countdown > 0 and countdown < COUNTDOWN_LIMIT and room_num >= 1:
            for i in range(len(str(countdown))):
                screen.blit(spr_number, (16 + i *16, 16), (int(str(countdown)[i]) * 16, 0, 16, 32))

        if room_num == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            room_num += 1
            alive = False

            player_y = 42069
            countdown = COUNTDOWN_LIMIT
            player_x = 42069
            collected = []
        

        # COLOR OF THE BACKGROUND OF THE PRIMARY SCREEN
        display.fill((0, 255, 255))
        

        if countdown > 0:
            if countdown < 300 and countdown > 200:
                color_line = 255, 100, 0
            elif countdown < 200:
                color_line = 255, 0, 0



            # INDICATES THE TIME PASSING ON THE RIGHT OF THE SCREEN
            pygame.draw.line(display,
                color_line, # color
                (488*2 + 32, 0 - countdown // 10), # (x, y)
                (488*2 + 32, 100 - countdown // 10), # (x, y)
                100)

        # generate()

        display.blit(pygame.transform.scale(screen, (488*screen_ratio  , 288*screen_ratio)),(0, 0))
        display.blit(room_number(), (480, 288))
        msg = message(f"Crystals: {len(collected)}")
        display.blit(msg, (10, 10))

        pygame.display.flip()
        change_room()


pygame.quit()
