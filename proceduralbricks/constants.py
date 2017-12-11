from enum import Enum

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
        
BRICK_1X1 = '3005'
BRICK_1X2 = '3004'
BRICK_1X2_MASONRY = '98283'
WINDOW_1X2X2 = '60592C01'
WINDOW_1X2X3 = '60593C01'
GLASS_1X4X6 = '57895'
DOOR_1X4X6_FRAME = '30179'
DOOR_1X4X6_3_PANE = '30178C01'
DOOR_1X4X6_4_PANE = '60623'

# Colors

BLACK = 0
TAN = 19
SAND_BLUE = 379
TRANS_CLEAR = 47

