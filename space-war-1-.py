# Imports
import pygame
import random
import sys
import pygame.sprite as sprite
import xbox360_controller

# Initialize game engine
pygame.init()

# Window
WIDTH = 900
HEIGHT = 675
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode((900,675))
pygame.display.set_caption(TITLE)

background = pygame.Surface(screen.get_size())
background.fill((250, 250, 250))

# Stages
START = 0
PLAYING = 1
END = 2

#Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("fonts/bingo.otf", 96)

#Background
theClock = pygame.time.Clock()

background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
w,h = background_size
x = 0
y = 0

x1 = 0
y1 = -h

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Images
ship_img = pygame.image.load('images/player.png')
laser_img = pygame.image.load('images/redlaser.png')
mob_img = pygame.image.load('images/mob.png')
bomb_img = pygame.image.load('images/bluelaser.png')
spacegod = pygame.image.load('images/spacegod.png')
spacebg = pygame.image.load('images/background.gif')
healthbar_img = pygame.image.load('images/healthbar.png')
health_img = pygame.image.load('images/health.png')
startscreen = pygame.image.load('images/startscreen.png')


# Sounds
explosion = pygame.mixer.Sound('sounds/explosion.wav')
shoot_s = pygame.mixer.Sound('sounds/shoot.wav')
background = pygame.mixer.Sound('sounds/background.wav')


# Xbox Controller
##my_controller = xbox360_controller.Controller(0)
##
##LEFT = pygame.K_LEFT
##RIGHT = pygame.K_RIGHT
##SHOOT = pygame.K_SPACE

# Game Sprite Classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 100

    def h_bar(self):
        #healthbar = Ship(self.rect.x, self.rect.y, healthbar_img)
        #health = Ship(self.rect.x, self.rect.y, healthbar_img)
        screen.blit(healthbar_img, (6,5))
        for health1 in range(self.shield):
            screen.blit(health_img, (health1+8, 8))
            #healthbar.rect.bottom = self.rect.bottom
            #healthbar.rect.bottom = self.rect.bottom

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        shoot_s.play()

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 25

        #Screen Collision
        if self.rect.x >= WIDTH - 96:
            self.rect.x =  WIDTH- 96
        elif self.rect.x <= 0:
            self.rect.x = 0

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            explosion.play()
            self.kill()

        
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.rect.y -= self.speed
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 3

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        global score

##        location = (self.rect.x, self.rect.y - 40, self.shield / 3, 15)
##        location2 = (self.rect.x - 1, self.rect.y - 41, (255 / 3) + 2, 17)
##        color = (-1 * (self.shield - 255), self.shield, 0)
##
##        pygame.draw.rect(screen, BLACK, location2)
##        pygame.draw.rect(screen, color, location)

        #Check if Hit
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            self.shield -= 1
        elif self.shield < 0:
            player.score += 1
            self.kill()
            explosion.play()



class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

def setup():
    global ship, mobs, stage, player, bombs, lasers, fleet, wave, score

    pygame.mixer.music.load("sounds/background.wav")
    pygame.mixer.music.play(-1)
    
    ship = Ship(384, 536, ship_img)
    
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    
    player.score = 0
    wave = 1
    score = 0

    stage = START

def start(wave):
    global ship, mobs, stage, player, bombs, lasers, fleet, score

    if score!= 0:
        wavestart.play()

    if wave == 1 or wave == 2:
        mob1 = Mob(128, 64, mob_img)
        mob2 = Mob(256, 64, mob_img)
        mob3 = Mob(384, 64, mob_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3)
        
    elif wave == 3 or wave == 4:
        mob1 = Mob(128, 64, mob_img)
        mob2 = Mob(256, 64, mob_img)
        mob3 = Mob(384, 64, mob_img)
        mob4 = Mob(256, 180, mob_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4)
        fleet.speed += 0.25
        
    elif wave == 5 or wave == 6:
        mob1 = Mob(128, 64, mob_img)
        mob2 = Mob(256, 64, mob_img)
        mob3 = Mob(384, 64, mob_img)
        mob4 = Mob(192, 180, mob_img)
        mob5 = Mob(320, 180, mob_img)
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4,mob5)

    else:
        mob1 = Mob(128, 64, mob_img)
        mob2 = Mob(256, 64, mob_img)
        mob3 = Mob(384, 64, mob_img)
        mob4 = Mob(192, 180, mob_img)
        mob5 = Mob(320, 180, mob_img)
        
        
        mobs = pygame.sprite.Group()
        mobs.add(mob1,mob2,mob3,mob4,mob5)
        fleet.speed += 0.25
# Make sprite groups

    lasers = pygame.sprite.Group()

    bombs = pygame.sprite.Group()

    fleet = Fleet(mobs)

#Game Helper Functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    space_to_play = FONT_MD.render("Press Space to Play!!", 1, WHITE)
    screen.blit(startscreen, (0, 1))
    screen.blit(title_text, [120, 204])
    screen.blit(space_to_play, [350, 350])

def show_stats(player):
    score_text = FONT_MD.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

def show_lose():
    title_text = FONT_XL.render("You lose!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_win():
    title_text = FONT_XL.render("You win!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def restart_screen():
    text = FONT_MD.render("Press R to play again!", 1, WHITE)
    screen.blit(text, [350, 350])
    stage = START

def draw_wave():
    wave_text = FONT_MD.render("Wave: " + str(wave), 1, WHITE)
    screen.blit(wave_text, [32, 50])

    
    

# Game loop
setup()
done = False
start(wave)

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()



    #pygame.display.flip()
    theClock.tick(60)
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
    if stage == PLAYING:
        if stage == PLAYING:
            if len(mobs) == 0:
                wave += 1
                start(wave)
            elif ship.shield == 0:
                stage = END
            elif wave >= 10:
                stage = END

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(spacebg,background_rect)
    y1 += 5
    y += 5
    screen.blit(spacebg,(x,y))
    screen.blit(spacebg,(x1,y1))
    if y > h:
        y = -h
    if y1 > h:
        y1 = -h
    
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)
    draw_wave()
    ship.h_bar()

    if stage == START:
        show_title_screen()

    elif stage == END:
        if len(mobs) == 0:
            show_win()
            restart_screen()
            restart = 1
        elif ship.shield == 0:
            show_lose()
            restart_screen()
            restart = 1
        elif wave >= 10:
            show_win()
            restart_screen()


    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
