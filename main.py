# this file was created by Julian Van Bruaene with a base platform from Chris Cozort
# Coding Help from Dominic Kirk on the Coins 
# Sources: goo.gl/2KMivS 
# now available in github

#Sound Sources:
#https://downloads.khinsider.com/zelda
#http://soundbible.com/tags-cha-ching.html
#https://themushroomkingdom.net/media/mg-n64/wav

'''
Main Developments for this game: 
- Create Moving Platforms
    - I created the new class in sprites, as well as the new variables in settings,
      and altered the code for platforms in main to make them slide on the screen.
    - Important Side Note: You can jump on them around 90% of the time, the other 10% it 
      cannot jump.
- Creating Coins
    - I created Gold and Silver Coin classes in sprites, and gave them different scoring systems.
      Gold is worth more in my game than silver, this was done in my settings page. 
- Creating A Cactus (One more enemy)
    - The cactus is the other enemy on my game, I used the base code for the coins and made it so that 
      the character would die if I hit them, editing the main code. This, and the other powerups, all reside
      only on the steady platforms, since I wanted to make it possible to win. 
- Visual Changes
    - I added a different background color, different types of platforms, a different enemy, and the sprites for 
      each of the new coins and cacti. The menu is also slightly different in font. 
- Sound Changes
    - Other than the powerup and jump sounds, all of the other sounds are different. The citations for these are found 
      above.                                                                                                                                                                                                                                
- Bugs
    - As previously mentioned, you can jump off the platforms the majority of the time, but not all of the time. 
'''
import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import time

class Game:
    def __init__(self):
        #init game xrwindow
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Doodle Jump")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
    def load_data(self):
        print("load data is called...")
        # sets up directory name
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # opens file with write options
        ''' with is a contextual option that handles both opening and closing of files to avoid
        issues with forgetting to close
        '''
        try:
            # changed to r to avoid overwriting error
            with open(path.join(self.dir, "highscore.txt"), 'r') as f:
                self.highscore = int(f.read())
                print(self.highscore)
        except:
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                self.highscore = 0
                print("exception")
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))       
        # load sounds
        # these were imported from various websites 
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = [pg.mixer.Sound(path.join(self.snd_dir, 'Jump18.wav')),
                            pg.mixer.Sound(path.join(self.snd_dir, 'Jump24.wav'))]
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'moneyReal.wav'))
        #Sounds for when you hit the evil bird things
        self.birdy_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump29.wav'))
        #When yoy hit them from anywhere not the top (when it kills you)
        self.birdyLeft_sound = pg.mixer.Sound(path.join(self.snd_dir, 'mario.wav'))
                
    def new(self):
        self.score = 0
        # add all sprites to the pg group
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create platforms group
        self.platforms = pg.sprite.Group()
        #creates the moving platforms group
        self.movingplatform = pg.sprite.Group()
        # add powerups 
        self.powerups = pg.sprite.Group()
        #add gold and silver coins 
        self.gold = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        #Adds the cactus 
        self.cactus = pg.sprite.Group()
        #Adds mob timer
        self.mob_timer = 0
        # add a player 1 to the group
        self.player = Player(self)
        # add mobs
        self.mobs = pg.sprite.Group()
        # instantiate new platform 
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        # instantiates the moving platform
        for mplat in MOVINGPFORM_LIST:
            MovingPlatform(self, *mplat)
        for i in range(8):
            m = MovingPlatform(self, *mplat)
            m.rect.y += 500
        # load background music
        pg.mixer.music.load(path.join(self.snd_dir, 'Background.mp3'))
        # call the run method
        self.run()
    def run(self):
        # game loop
        # play music
        pg.mixer.music.play(loops=-1)
        # set boolean playing to true
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(1000)

    def update(self):
        self.all_sprites.update()
        #spawning a mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
        # check for mob collisions
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            if self.player.pos.y - 35 < mob_hits[0].rect_top:
                print("hit top")
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.player.vel.y = -BOOST_POWER
                #indicating different sounds for death vs life
                self.birdy_sound.play()
            else:
                print("player is " + str(self.player.pos.y))
                print("mob is " + str(mob_hits[0].rect_top))
                self.playing = False
                #indicating different sounds for death vs life
                self.birdyLeft_sound.play()

        # check to see if player can jump - if falling from either type of platform
        # important note, I tried editing the {if hits} code for {if mhits},
        # but jumping on the {if mhits} was sporadic, sometimes it was successful,
        # othertimes it was not
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            mhits = pg.sprite.spritecollide(self.player, self.movingplatform, False)
            if hits:
                # set var to be current hit in list to find which to 'pop' to when two or more collide with player
                    find_lowest = hits[0]
            for hit in hits:
                if hit.rect.bottom > find_lowest.rect.bottom:
                    print("hit rect bottom " + str(hit.rect.bottom))
                    find_lowest = hit
                if self.player.pos.x < find_lowest.rect.right + 10 and self.player.pos.x > find_lowest.rect.left - 10:
                    if self.player.pos.y < find_lowest.rect.centery:
                            self.player.pos.y = find_lowest.rect.top
                            self.player.vel.y = 0
                            self.player.jumping = False 
            #Check to see if player 1 is on the moving platform 
            if mhits:
                find_mlowest = mhits[0]
            for mhit in mhits:
                if mhit.rect.bottom > find_mlowest.rect.bottom: 
                    find_mlowest = mhit
                if self.player.pos.x < find_mlowest.rect.right + 10 and self.player.pos.x > find_mlowest.rect.left - 10: 
                    if self.player.pos.y < find_mlowest.rect.centery:
                        self.player.pos.y = find_mlowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
        if self.player.rect.top <= HEIGHT / 4:
            # creates slight scroll at the top based on player y velocity
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                # creates slight scroll based on player y velocity
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                # creates slight scroll based on player y velocity
                # in the regular platforms
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT + 40:
                    plat.kill()
                    self.score += 10
            for mplat in self.movingplatform: 
                # creates a slight scroll based on player y velocity\
                # in the moving platforms
                mplat.rect.y += max(abs(self.player.vel.y), 2)
                if mplat.rect.top >= HEIGHT + 40:
                    mplat.kill()
                    self.score += 10
            #If the player hits a cactus on the plaforms
            for Cactus in self.cactus:
                Cactus.rect.y += max(abs(self.player.vel.y), 2)
        # if player hits a power up
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
        # if player gets a regular coin
        coin_hits = pg.sprite.spritecollide(self.player, self.coin, True)
        for coin in coin_hits:
            if coin.type == 'coin':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.score += 10
        #if player gets the gold coin
        gold_hits = pg.sprite.spritecollide(self.player, self.gold, True)
        for gold in gold_hits:
            if gold.type == 'gold':
                self.boost_sound.play()
                self.player.vel.y = -10
                self.score += 10 
        #if player hits the bad, evil, no good, very bad cactus
        cactus_hits = pg.sprite.spritecollide(self.player, self.cactus, True)
        for cactus in cactus_hits:
            if cactus.type == 'cactus':
                self.playing = False
                self.birdyLeft_sound.play()
        # Die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        if len(self.movingplatform) == 0:
            self.playing = False
        # generate new random platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            ''' removed widths and height params to allow for sprites'''
            Platform(self, random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30))
        #generates new random moving platforms
        while len(self.movingplatform) < 6:
            width = random.randrange(50, 100)
            MovingPlatform(self, random.randrange(0,WIDTH-width), 
                            random.randrange(-75, -30))
    
    #Events 
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        # cuts the jump short if the space bar is released
                        self.player.jump_cut()

    def draw(self):
        self.screen.fill(SKY_BLUE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # double buffering - renders a frame "behind" the displayed frame
        pg.display.flip()

    def wait_for_key(self): 
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        # game splash screen
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        #Instructs in the opening menu that the arrow keys need to be used 
        self.draw_text("Arrow keys to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game splash screen
        if not self.running:
            print("not running...")
            return
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/4)
        #Instructs that we have to use arrow keys. 
        self.draw_text("Arrow keys to move, Space to jump", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to play...", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("new high score!", 22, WHITE, WIDTH / 2, HEIGHT/2 + 60)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        else:
            self.draw_text("High score " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT/2 + 40)
            pg.display.flip()
            self.wait_for_key()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    try:
        g.show_go_screen()
    except:
        print("can't load go screen...")