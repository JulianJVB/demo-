# sprite classes for game
# i used some ideas from CodePylet https://www.youtube.com/watch?v=osDofIdja6s&t=1038s
# i also borrowed pretty much all of this from kids can code - thanks!
# on acceleration https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/v/average-velocity-for-constant-acceleration 
# on vectors: https://www.youtube.com/watch?v=ml4NSzCQobk 


import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint, randrange, choice
from settings import *

vec = pg.math.Vector2
class Spritesheet:
    # class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
        #This here adds the actual sprite sheet, it allows us to initialize this 
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        #This entire method returns the image into the game
        return image
class Player(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group - thanks pygame!
        #This is a built in pygame tool, stated in settings
        self._layer = PLAYER_LAYER
        #This is equal to the value associated with PLAYER_LAYER (2)
        # add player to game groups when instantiated
        #This means you do not have to call it everytime in the code
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        # self.image = pg.Surface((30,40))
        # self.image = self.game.spritesheet.get_image(614,1063,120,191)
        self.image = self.standing_frames[0]
        #The first image that will be shown

        self.image.set_colorkey(BLACK)
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT /2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        print("adding vecs " + str(self.vel + self.acc))
    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(690, 406, 120, 201),
                                #This goes back and forth continuously, loading upward 
                                self.game.spritesheet.get_image(614, 1063, 120, 191)
                                ]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                                self.game.spritesheet.get_image(692, 1458, 120, 207)
                                ]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        #Sets Player Acceleration
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # set player friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # jump to other side of screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos
    # cuts the jump short when the space bar is released
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -5:
                self.vel.y = -5
    def jump(self):
        print("jump is working")
        # check pixel below
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        mhits = pg.sprite.spritecollide(self, self.game.movingplatform, False)
        # adjust based on checked pixel
        self.rect.y -= 2
        # only allow jumping if player is on platform
        if hits and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
        #When it is jumping for the moving platform 
        if mhits and not self.jumping:
            # play sound only when space bar is hit and while not jumping
            self.game.jump_sound[choice([0,1])].play()
            # tell the program that player is currently jumping
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            print(self.acc.y)
    def animate(self):
        # gets time in miliseconds
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # checks state
        if not self.jumping and not self.walking:
            # gets current delta time and checks against 200 miliseconds
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                # reset bottom for each frame of animation
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


#Regular Platform Class
class Platform(Sprite):
    def __init__(self, game, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = PLATFORM_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        #Gets the images for each of the platforms
        images = [self.game.spritesheet.get_image(0, 288, 380, 94), 
                  self.game.spritesheet.get_image(213, 1662, 201, 100),
                  self.game.spritesheet.get_image(0, 672, 380, 94),
                  self.game.spritesheet.get_image(208, 1879, 201, 100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #Allows for various powerups and enemies to spawn on the platforms
        if random.randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
        if random.randrange(100) < COIN_SPAWN_PCT:
            Coin(self.game, self)
        if random.randrange(100) < GOLD_SPAWN_PCT:
            Gold(self.game, self)
        if random.randrange(100) < COIN_SPAWN_PCT:
            Cactus(self.game, self)

#Moving Platform Class
class MovingPlatform(Sprite):
    def __init__(self, game, x, y):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOVINGPFORM_LAYER
        # add Platforms to game groups when instantiated
        self.groups = game.all_sprites, game.movingplatform
        Sprite.__init__(self, self.groups)
        self.game = game
        #images for the moving platform class
        images = [self.game.spritesheet.get_image(0, 288, 380, 94), 
                  self.game.spritesheet.get_image(213, 1662, 201, 100),
                  self.game.spritesheet.get_image(0, 672, 380, 94),
                  self.game.spritesheet.get_image(208, 1879, 201, 100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        self.speed = randrange(1,3)
        #To spawn either right or left
        self.speed = randrange(1,3)
        self.ground_level = False
    #I intentionally didn't add the powerups to the moving platform
    #That would make the game too difficult 
    #Updating the moving platforms class to determine whether player lives
    def update(self):
        if self.rect.top > HEIGHT * 2: 
            self.kill
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.rect.x = -self.rect.width

#Powerups Class 
class Pow(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()

#Class for the silver coin
class Coin(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.coin
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['coin'])
        self.image = self.game.spritesheet.get_image(584, 406, 84, 84)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()
        
#Class for the rarer gold coins 
class Gold(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = POW_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.gold
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['gold'])
        self.image = self.game.spritesheet.get_image(698, 1931, 84, 84)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()

#Class for the Cactus 
class Cactus(Sprite):
    def __init__(self, game, plat):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.cactus
        Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['cactus'])
        self.image = self.game.spritesheet.get_image(707, 134, 117, 160)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top 
    def update(self):
        self.rect.bottom = self.plat.rect.top 
        # checks to see if plat is in the game's platforms group so we can kill the powerup instance
        if not self.game.platforms.has(self.plat):
            self.kill()

#Class for the Mob Sprites in the game 
class Mob(Sprite):
    def __init__(self, game):
        # allows layering in LayeredUpdates sprite group
        self._layer = MOB_LAYER
        # add a groups property where we can pass all instances of this object into game groups
        self.groups = game.all_sprites, game.mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet.get_image(382, 625, 174, 126)
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet.get_image(0, 1879, 206, 107)
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.rect_top = self.rect.top
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT/2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        self.rect_top = self.rect.top
        if self.vy > 3 or  self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect.center = center
        self.rect_top = self.rect.top
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
