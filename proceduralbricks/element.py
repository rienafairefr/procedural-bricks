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
  def __init__(self, pos, facing=Facing.FRONT, part='3004', color=0, pos_b=None, connections=Connections()):
    self.pos = pos
    self.facing = facing
    self.connections = connections
    self.part = part
    self.color = color

  def to_ldr(self):
    if self.facing == Facing.FRONT:
      orientation = "1 0 0 0 1 0 0 0 1"
    elif self.facing == Facing.BACK:
      orientation = "-1 0 0 0 1 0 0 0 -1"
    elif self.facing == Facing.LEFT:
      orientation = "0 0 1 0 1 0 -1 0 0"
    elif self.facing == Facing.RIGHT:
      orientation = "0 0 -1 0 1 0 1 0 0"
    else:
      pass

    return("1 %d %d %d %d %s %s.dat" % (self.color.value, self.pos[0], self.pos[1], self.pos[2], orientation, self.part))

  def collides_with(self, other):
    part1 = p.part(code=self.part)
    part2 = p.part(code=other.part)
    pass

class ElementGroup:
  def __init__(self, pos, facing, pos_b=None, connections=Connections()):
    self.pos = pos
    self.pos_b = pos_b
    self.facing = facing
    self.connections = connections
    self.children = []

  def relative_pos(self, v):
    ret = [0,0,0]
  
    ret[self.facing.x] = v[0]
    ret[self.facing.y] = v[1]
    ret[self.facing.z] = v[2]
  
    return ret

  def append(self, child):
    child.pos = self.relative_pos(child.pos)
      
    self.children.append(child)

  def to_ldr(self):
    return('\n'.join([c.to_ldr() for c in self.children]))

  def collides_with(self, element):
    for child in self.children:
      if child.collides_with(element):
        return True
    return False