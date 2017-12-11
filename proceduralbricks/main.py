from random import random

from buildings import ModularBuilding

def main():
  building = ModularBuilding()

  with open('test.ldr', 'w') as out:
    out.write(building.to_ldr())

if __name__ == '__main__':
  main()