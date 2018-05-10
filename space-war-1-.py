# Imports
import pygame
import random
import sys
import pygame.sprite as sprite

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
healthbar_img = pygame.image.load("images/healthbar.png")
health_img = pygame.image.load("images/health.png")


# Sounds
#EXPLOSION = pygame.mixer.Sound('sounds/explosion.ogg')

# Game classes
# Game classes
#def draw(self)

#draw_shield_bar(self.screen, 50, 50, player.shield)



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

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 25

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            #EXPLOSION.play()
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
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            self.shield -= 1
        elif self.shield < 0:
            player.score += 1
            self.kill()



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
    global ship, mobs, stage, player, bombs, lasers, fleet

    ship = Ship(384, 536, ship_img)
    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(256, 64, mob_img)
    mob3 = Mob(384, 64, mob_img)
    mob4 = Mob(128, 0, mob_img)
    mob5 = Mob(256, 0, mob_img)
    mob6 = Mob(384, 0, mob_img)

    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0


    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)

    stage = START

# set stage


    
# Make game objects

# Make sprite groups

#Game Helper Functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

def show_lose():
    title_text = FONT_XL.render("You lose!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_win():
    title_text = FONT_XL.render("You win!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def restart_screen():
    text = FONT_MD.render("Press R to play again!", 1, WHITE)
    screen.blit(text, [0, 100])

# Game loop
setup()
done = False

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
            elif restart == 1:
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
                stage = END
            elif ship.shield == 0:
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


    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
