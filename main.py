#this file was created by Julian Van Bruaene 
# thanks Chris Bradfield 

# import libs
import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # init game window, etc
        
        # init pygame and create window
        pg.init()
        # init sound mixer
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("jumpy")
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()
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
        # updates things as needed
        self.all_sprites.update()

    def events(self):
        # game loop events
        ### process input events section of game loop
        for event in pg.event.get():
            # check for window closing
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # game loop draw
        ### draw and render section of game loop
        self.screen.fill(REDDISH)
        self.all_sprites.draw(self.screen)
        # double buffering draws frames for entire screen
        pg.display.flip()
        # pygame.display.update() -> only updates a portion of the screen
    
    def show_start_screen(self):
        # game splash start screen
        pass

    def show_go_screen(self):
        # show game over screen
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()