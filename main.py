#this file was created by Julian Van Bruaene 
# thanks Chris Bradfield  
# Kids Can Code is a 
# top quality resource which will be crucial for me editing my code and making it more original

# import libraries
import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # init game window, try:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
        # init pygame and create...
    def new(self):
        self.all_sprites = pg.sprite.Group()
        #create plaforms group 
        self.platforms = pg.sprite.Group()
        # adding a player 1 to the group
        self.player = Player(self)
        self.all_sprites.add(self.player)
        # instantiate new platform
        for plat in PLATFORM_LIST: 
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()
        # create new player object
    def run(self):
        # game loop
        self.playing = True
        while self.playing: 
            #  keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # updating things when necessary, useful for further developments
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT + 40: 
                    plat.kill()
        while len(self.platforms) < 6: 
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0,WIDTH-width),
                            random.randrange(-75, -30),
                            width, 
                            20
                        )
            self.platforms.add(p)
            self.all_sprites.add(p)
        

    def events(self):
        # listening to events
        for event in pg.event.get():
            # if (boolean) statement
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
        

    def draw(self):
        self.screen.fill(REDDISH)
        self.all_sprites.draw(self.screen)
        #double buffer
        pg.display.flip()
        
    
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
