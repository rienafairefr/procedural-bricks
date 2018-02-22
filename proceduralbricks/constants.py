import os

import yaml
from enum import Enum
from ldraw.parts import Parts
from appdirs import user_config_dir

config_dir = user_config_dir('procedural-bricks')
config_path = os.path.join(config_dir, 'config.yml')
try:
  with open(config_path, 'r') as config_file:
    config = yaml.load(config_file)
except:
  if not os.path.exists(config_dir):
    os.makedirs(config_dir)
  if not os.path.exists(config_path):
    with open(config_path, 'w') as config_file:
      yaml.dump({'LDRAW_PARTS_PATH':None}, config_file)
  print('The config file %s is inexistent or empty' % config_path)
  exit(-1)

if config is None or config.get('LDRAW_PARTS_PATH') is None:
  print('The config file %s is invalid' % config_path)
  exit(-1)


p = Parts(config['LDRAW_PARTS_PATH'])


# Connections
BRICK_EVEN = 1
BRICK_ODD = 2

class Facing(Enum):
  FRONT = (0, 1, 2, 1)
  BACK = (0, 1, 2, -1)
  LEFT = (2, 1, 0, 1)
  RIGHT = (2, 1, 0, -1)
  def __init__(self, x, y, z, flip):
    self.x = x
    self.y = y
    self.z = z
    self.flip = flip

# Parts
BRICK_1X1 = p.parts['Brick  1 x  1']
BRICK_1X2 = p.parts['Brick  1 x  2']
BRICK_2x2 = p.parts['Brick  2 x  2']
BRICK_2x3 = p.parts['Brick  2 x  3']
BRICK_2x4 = p.parts['Brick  2 x  4']
BRICK_1X3 = p.parts['Brick  1 x  3']
BRICK_1X4 = p.parts['Brick  1 x  4']

BRICK_1X2_MASONRY = '98283'
WINDOW_1X2X2 = '60592C01'
WINDOW_1X2X3 = '60593C01'
GLASS_1X4X6 = '57895'
DOOR_1X4X6_FRAME = '30179'
DOOR_1X4X6_3_PANE = '30178C01'
DOOR_1X4X6_4_PANE = '60623'

# Colors

class Colors(Enum):
  black = 0
  blue = 1
  green = 2
  teal = 3
  red = 4
  darkpink = 5
  brown = 6
  grey = 7
  darkgrey = 8
  lightblue = 9
  brightgreen = 10
  turquoise = 11
  lightred = 12
  pink = 13
  yellow = 14
  white = 15
  current = 16
  lightgreen = 17
  lightyellow = 18
  tan = 19
  lightpurple = 20
  glowinthedark = 21
  purple = 22
  violetblue = 23
  orange = 25
  magenta = 26
  lime = 27
  transblue = 33
  transgreen = 34
  transred = 36
  transpurple = 37
  smoke = 39
  lighttransblue = 41
  transneongreen = 42
  transpink = 45
  transyellow = 46
  clear = 47
  transorange = 57
  blackrubber = 256
  darkblue = 272
  darkred = 320
  chromegold = 334
  sandred = 335
  earthorange = 366
  sandviolet = 373
  greyrubber = 375
  sandgreen = 378
  sandblue = 379
  chromesilver = 383
  lightorange = 462
  darkorange = 484
  lightgrey = 503
