from enum import Enum
from ldraw.library import colours
from ldraw.library.parts.others import *
from ldraw.library.colours import *

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


Brick1X2Masonry = Brick1X2WithEmbossedBricks
Window1X2X2 = Window1X2X2WithoutSillW_Trans_ClearGlass_Complete_
Window1X2X3 = Window1X2X3WithoutSillW_Trans_ClearGlass_Complete_
Glass1X4X6 = GlassForWindow1X4X6
Door1X4X6Frame = Door1X4X6FrameType1
Door1X4X6With3Panes = Door1X4X6With3Panes_Complete_
Door1X4X6With4Panes = Door1X4X6With4PanesAndStudHandle

AllColors = list(ColoursByCode.values())
Colors = colours

stud = 20
brick_height = 24