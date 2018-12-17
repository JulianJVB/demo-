TITLE = "Jumping Game"
# screen dims
WIDTH = 480
HEIGHT = 600
# frames per second
FPS = 60
# colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
REDDISH = (240,55,66)
#Changes background colors and the font of the project. 
SKY_BLUE = (0, 0, 153)
FONT_NAME = 'comic sans'
SPRITESHEET = "spritesheet_jumper.png"
# data files
HS_FILE = "highscore.txt"
# player settings
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
# Spawn percentages of powerups and enemies 
BOOST_POWER = 60
POW_SPAWN_PCT = 7
COIN_SPAWN_PCT = 16
GOLD_SPAWN_PCT = 6
MOB_FREQ = 5000
#Player Layer
PLAYER_LAYER = 2
#Platform and Moving Platform Layers
PLATFORM_LAYER = 1
MOVINGPFORM_LAYER = 1
#Given Powerup Layers
POW_LAYER = 1
MOB_LAYER = 2

# platform settings
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (65, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (200, HEIGHT - 450)]

# moving platform settings 
MOVINGPFORM_LIST = [(0, HEIGHT - 40),
                 (65, HEIGHT - 300),
                 (20, HEIGHT - 350),
                 (200, HEIGHT - 150),
                 (200, HEIGHT - 450)]