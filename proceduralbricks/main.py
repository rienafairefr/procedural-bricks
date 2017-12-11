"""
The structure is broken down recursively into interconnected subgroups.
"""

from random import random

from constants import *
from element import Element, ElementGroup, Connections

def window_wall(start, width, facing=Facing.FRONT, left=FillType.SOLID, right=FillType.SOLID):
  """ 
  A wall with windows

  Height is always 6 bricks 
  """

  els = []

  els.append(Wall((start[0], start[1], start[2]), (start[0] + 40, start[1] + 6 * 24, start[2]), connections=Connections(left=left,right=FillType.SOLID)))

  last_solid = True
  x = 40
  while x < start[facing.x] + width * 40 - 40:
    if last_solid:
      last_solid = False
      if random() > .5:
        # Door
        els.append(Element(relative_pos((start[0] + x + 20, start[1], start[2]), facing), facing, part=Parts.DOOR_1X4X6_FRAME.value, color = Colors.TAN.value))
        if random() > .5:
          els.append((relative_pos((start[0] + x - 12, start[1], start[2]), facing),Parts.DOOR_1X4X6_4_PANE.value, Colors.BLACK.value, facing))
        else:
          els.append((relative_pos((start[0] + x + 20, start[1] + 4, start[2]), facing),Parts.GLASS_1X4X6.value, Colors.TRANS_CLEAR.value, facing))
      else:
        els.append(Wall((start[0] + x, start[1] + 4 * 24, start[2]), (start[0] + x + 80, start[1] + 6 * 24, start[2]), connections=Connections(left=FillType.SOLID, right=FillType.SOLID)))
        els.append((relative_pos((start[0] + x, start[1], start[2]), facing),Parts.WINDOW_1X2X2.value, Colors.TAN.value, facing))
        els.append((relative_pos((start[0] + x + 40, start[1], start[2]), facing),Parts.WINDOW_1X2X2.value, Colors.TAN.value, facing))
        els.append((relative_pos((start[0] + x, start[1] + 48, start[2]), facing),Parts.WINDOW_1X2X2.value, Colors.TAN.value, facing))
        els.append((relative_pos((start[0] + x + 40, start[1] + 48, start[2]), facing),Parts.WINDOW_1X2X2.value, Colors.TAN.value, facing))
      x += 80
    else:
      last_solid = True
      els += wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2]))
      x += 40

  els += wall((start[0] + x, start[1], start[2]), (start[0] + x + 40, start[1] + 6 * 24, start[2]), right=right)

  return els

def relative_pos(pos, facing):
  ret = [0,0,0]

  ret[facing.x] = 20 + pos[0]
  ret[facing.y] = pos[1]
  ret[facing.z] = 10 + pos[2]

  return ret

class Wall(ElementGroup):
  def __init__(self, pos, pos_b, facing = Facing.FRONT, connections=Connections(left=FillType.EVEN, right=FillType.EVEN)):
    ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

    for x in range(pos[self.facing.x],pos_b[self.facing.x],20*2):
      for y in range(pos[self.facing.y],pos_b[self.facing.y],24):
        offset = 0
        part = Parts.BRICK_1X2.value
  
        if connections.left != FillType.SOLID and (y / 24) % 2 == connections.left.value:
          offset = 20
  
        if offset > 0:
          if x == pos_b[facing.x] - 40:
            if connections.right != FillType.SOLID:
              continue
            else:
              offset = 10
              part = Parts.BRICK_1X1.value
  
        if connections.right != FillType.SOLID and (y / 24) % 2 == connections.right.value and abs(pos_b[facing.x] - pos[facing.x]) == 40:
          offset = -10
          part = Parts.BRICK_1X1.value 
  
        position = relative_pos((x + offset,y,pos[facing.z]), facing)
        
        self.children.append(Element(position, facing, part=part, color=Colors.SAND_BLUE.value))
        

def wall(a, b, facing = Facing.FRONT, left=FillType.SOLID, right=FillType.SOLID):
  """ Returns a wall fill between a and b """
  els = []
  
  for x in range(a[facing.x],b[facing.x],20*2):
    for y in range(a[facing.y],b[facing.y],24):
      offset = 0
      part = Parts.BRICK_1X2.value

      if left != FillType.SOLID and (y / 24) % 2 == left.value:
        offset = 20

      if offset > 0:
        if x == b[facing.x] - 40:
          if right != FillType.SOLID:
            continue
          else:
            offset = 10
            part = Parts.BRICK_1X1.value

      if right != FillType.SOLID and (y / 24) % 2 == right.value and abs(b[facing.x] - a[facing.x]) == 40:
        offset = -10
        part = Parts.BRICK_1X1.value 

      position = relative_pos((x + offset,y,a[facing.z]), facing)
      
      els.append((position, part, Colors.SAND_BLUE.value, facing))

  return els

def el_to_line(el):
  if type(el) == tuple:
    if el[3] == Facing.LEFT:
      orientation = "0 0 1 0 1 0 -1 0 0"
    if el[3] == Facing.BACK:
      orientation = "-1 0 0 0 1 0 0 0 -1"
    if el[3] == Facing.FRONT:
      orientation = "1 0 0 0 1 0 0 0 1"
    if el[3] == Facing.RIGHT:
      orientation = "-0 0 -1 0 1 0 1 0 0"
  
    return "1 %d %d %d %d %s %s.dat" % (el[2], el[0][0], el[0][1], el[0][2], orientation, el[1])
  else:
    return el.to_ldr()

def as_ldr(els):
  lines = [el_to_line(e) for e in els]

  return '\n'.join(lines)

def wall_box(a, b, front = True):
  els = []

  if front:
    els.append(Wall(a,(b[0],b[1],a[2]), facing=Facing.FRONT, connections=Connections(left=FillType.EVEN, right=FillType.EVEN)))
  els.append(Wall(a,(a[0],b[1],b[2]), facing=Facing.LEFT, connections=Connections(left=FillType.ODD, right=FillType.ODD)))
  els.append(Wall((a[0],a[1],b[2] - 20),(b[0],b[1],b[2] - 20), facing=Facing.BACK, connections=Connections(left=FillType.EVEN, right=FillType.EVEN)))
  els.append(Wall((b[0] - 20,a[1],a[2]),(b[0] - 20,b[1],b[2]), facing=Facing.RIGHT, connections=Connections(left=FillType.ODD, right=FillType.ODD)))

  return els

def modular_building():
  els = []
  
  for y in range (0,8*8 * 24,8*24):
    els += wall_box((0,y,0), (31 * 40, y + 24 * 8, 20 * 16), front=False)

    els += [Wall((0,y,0), (31 * 40,y + 24 * 2, 0), connections=Connections(left=FillType.EVEN, right=FillType.EVEN))]
    els += window_wall((0,y + 24 * 2,0), 31, left=FillType.EVEN, right=FillType.EVEN)

  return els
    

def main():
  with open('test.ldr', 'w') as out:
    out.write(as_ldr(modular_building()))

if __name__ == '__main__':
  main()