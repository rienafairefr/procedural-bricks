from constants import *

class Connections:
  def __init__(self, top=None, bottom=None, left=None, right=None, front=None, back=None):
    self.top = top
    self.bottom = bottom
    self.left = left
    self.right = right
    self.front = front
    self.back = back

class Element:
  def __init__(self, pos, facing, pos_b=None, connections=Connections(), color=None, part=None):
    self.pos = pos
    self.pos_b = pos_b
    self.facing = facing
    self.connections = connections
    self.part = part
    self.color = color
    self.children = []

  def to_ldr(self):
    print(self.part)
  
    if self.facing == Facing.LEFT:
      orientation = "0 0 1 0 1 0 -1 0 0"
    if self.facing == Facing.BACK:
      orientation = "-1 0 0 0 1 0 0 0 -1"
    if self.facing == Facing.FRONT:
      orientation = "1 0 0 0 1 0 0 0 1"
    if self.facing == Facing.RIGHT:
      orientation = "-0 0 -1 0 1 0 1 0 0"

    ldr = '\n'.join([c.to_ldr() for c in self.children])

    if self.part:
      ldr += "\n1 %d %d %d %d %s %s.dat" % (self.color, self.pos[0], self.pos[1], self.pos[2], orientation, self.part)

    return ldr    