from random import random

from constants import *
from element import Element, ElementGroup, Connections


class Wall(ElementGroup):
  def __init__(self, pos, pos_b, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

    pos = self.relative_pos(pos)
    pos_b = self.relative_pos(pos_b)

    for x in range(pos[0],pos_b[0],20*2):
      for y in range(pos[1],pos_b[1],24):
        offset = 20
        part = Brick1X2

        if connections.left and (y / 24) % 2 == int(connections.left != BRICK_EVEN):
          offset = 40
          if x == pos_b[0] - 40:
            if connections.right:
              continue
            else:
              offset = 30
              part = Brick1X1

        last_one = (abs(pos_b[0] - pos[0]) == 40)
  
        if last_one and connections.right and (y / 24) % 2 == int(connections.right != BRICK_EVEN):
          offset = 10
          part = Brick1X1

        self.append(Element((x + offset,y,10 + pos[2]), facing, part=part, color=Colors.sandblue))

class WindowWall(ElementGroup):
  def __init__(self, start, width, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, start, facing, connections=connections)

    self.append(Wall((start[0], start[1], start[2]), (start[0] + 40, start[1] + 6 * 24, start[2]), connections=Connections(left=connections.left)))
  
    last_solid = True
    x = 40
    while x < start[facing.x] + width * 40 - 40:
      if last_solid:
        last_solid = False
        if random() > .5:
          # Door
          self.append(Element((start[0] + x + 40, start[1], start[2] + 10), facing, part=Door1X4X6Frame, color = Colors.tan))
          if random() > .5:
            self.append(Element((start[0] + x + 20 - 12, start[1], start[2] + 10), facing, part=Door1X4X6With4Panes, color=Colors.black))
          else:
            self.append(Element((start[0] + x + 40, start[1] + 4, start[2] + 10), facing, part=Glass1X4X6, color=Colors.clear))
        else:
          self.append(Wall((start[0] + x, start[1] + 4 * 24, start[2]), (start[0] + x + 80, start[1] + 6 * 24, start[2])))
          for wx in [start[0] + x + 20, start[0] + x + 60]:
            for wy in [start[1], start[1] + 48]:
              self.append(Element((wx, wy, start[2] + 10), facing, part=Window1X2X2, color=Colors.tan))
        x += 80
      else:
        last_solid = True
        self.append(Wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2])))
        x += 40
  
    self.append(Wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2]), connections=Connections(right=connections.right)))

class WallBox(ElementGroup):
  def __init__(self, a, b, Wall_cls, front=True, facing = Facing.FRONT, connections=Connections()):
    ElementGroup.__init__(self, a, facing, pos_b=b, connections=connections)

    if front:
      self.append(Wall_cls(a,(b[0],b[1],a[2]), facing=Facing.FRONT, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
    self.append(Wall_cls(a,(a[0],b[1],b[2]), facing=Facing.LEFT, connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))
    self.append(Wall_cls((a[0],a[1],b[2] - 20),(b[0],b[1],b[2] - 20), facing=Facing.BACK, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
    self.append(Wall_cls((b[0] - 20,a[1],a[2]),(b[0] - 20,b[1],b[2]), facing=Facing.RIGHT, connections=Connections(left=BRICK_ODD, right=BRICK_ODD)))

class ModularBuilding(ElementGroup):
  def __init__(self):
    ElementGroup.__init__(self, (0,0,0), Facing.FRONT)

    for y in range (0,8*8 * 24,8*24):
      self.append(WallBox((0,y,0), (31 * 40, y + 24 * 8, 20 * 16), Wall, front=False))
  
      self.append(Wall((0,y,0), (31 * 40,y + 24 * 2, 0), connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
      self.append(WindowWall((0,y + 24 * 2,0), 31, connections=Connections(left=BRICK_EVEN, right=BRICK_EVEN)))
