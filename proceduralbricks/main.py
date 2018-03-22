from random import random, randint

from buildings import ModularBuilding
from walls import CWall


def main():
    building = ModularBuilding(cls_Wall=CWall, width=randint(2,10), depth=randint(2,10), height=8)

    with open('test.ldr', 'w') as out:
        out.write(building.to_ldr())


if __name__ == '__main__':
    main()
