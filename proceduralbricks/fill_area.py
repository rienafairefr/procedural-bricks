import random
import sys

from proceduralbricks.constants import Brick1X1, Brick1X2, Brick1X4, Brick2X2, Brick1X3, Facing, Colors, AllColors
from proceduralbricks.element import ElementGroup, Connections, ldu, get_width, get_depth, get_height, Element, get_z_offset, lduy

parts = [
    Brick1X1, Brick1X2, Brick1X3, Brick1X4,
    Brick2X2,
]


OpaqueColors = [c for c in AllColors if c.alpha==255]


widths = {code: get_width(code) for code in parts}
depths = {code: get_depth(code) for code in parts}
heights = {code: get_height(code) - 4 / 24 for code in parts}
z_offsets = {code: get_z_offset(code) for code in parts}

seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print("Seed was:", seed)


class FillArea(ElementGroup):
    def fits(self, position, part):
        n_rows = len(self.pixels)
        n_columns = len(self.pixels[0])
        width = widths[part]
        depth = depths[part]
        for xi in range(position[0], position[0] + width):
            for zi in range(position[2], position[2] + depth):
                if zi < 0 or zi >= n_rows:
                    return False
                if xi < 0 or xi >= n_columns:
                    return False
                if self.pixels[zi][xi] == 0 or self.occupied[zi][xi]:
                    return False
        return True

    def put(self, position, part):
        width = widths[part]
        depth = depths[part]
        height = heights[part]

        for xi in range(position[0], position[0] + width):
            for zi in range(position[2], position[2] + depth):
                self.occupied[zi][xi] = True
                self.positions.remove((xi, position[1], zi))

        x_element = position[0]
        y_element = position[1]
        z_element = position[2]
        pos_element = (x_element + width / 2.0, y_element + height /2.0, z_element + depth/2.0)
        ldu_pos_element = ldu(pos_element)

        if callable(self.color):
            element_color = self.color()
        else:
            element_color = self.color

        element = Element((ldu_pos_element[0]+self.pos[0],
                           ldu_pos_element[1]+self.pos[1],
                           ldu_pos_element[2]+self.pos[2]), self.facing, part=part, color=element_color)

        self.append(element)

    def __init__(self, pixels, pos, color, facing=Facing.FRONT, pos_b=None, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b=pos_b, connections=connections)

        self.color = color
        self.pixels = pixels
        self.occupied = [[False] * len(row) for row in self.pixels]
        # image top left to bottom right

        self.positions = []
        for index_row, row in enumerate(self.pixels):
            for index_column, pixel in enumerate(row):
                if pixel != 0:
                    self.positions.append((index_column, 0, index_row))

        while len(self.positions) > 0:
            position = random.choice(self.positions)
            print(position, len(self.positions))
            random.shuffle(parts)

            for part in parts:
                if self.fits(position, part):
                    self.put(position, part)
                    break


def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Later versions of Pillow (4.x) rename _makeself to _new
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)


def get_alpha(image):
    image = image.convert('RGBA')

    # Extract just the alpha channel
    alpha = image.split()[-1]

    return alpha


def get_paletted(image, palette):
    palette_img = Image.new('P', (1, 1), 0)
    palette_img.putpalette(palette)

    quantized = image.convert(mode='RGB')
    quantized = quantizetopalette(quantized, palette_img, dither=False)
    quantized = quantized.convert('RGBA')

    alpha = get_alpha(image)
    quantized.putalpha(alpha)


    return quantized


class LayeredImage(ElementGroup):
    def __init__(self, image_path, pos, facing=Facing.FRONT, pos_b=None, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b, connections=connections)

        size = 32, 32

        im = Image.open('logo.png')
        im.thumbnail(size)

        back = get_alpha(im)
        palette = [el for c in OpaqueColors for el in ImageColor.getrgb(c.rgb)]

        paletted = get_paletted(im, palette)
        back.save('~logoback.png')
        paletted.save('~logopaletted.png')

        self.append(PillowImageElement(back, pos, Colors.Black, facing, pos_b))
        self.append(ColoredPillowImageElement(paletted, (pos[0], pos[1] + lduy(1), pos[2]), facing, pos_b))


class ImageElement(FillArea):
    def __init__(self, image_path, pos, color, facing=Facing.FRONT, pos_b=None, connections=Connections()):
        im = Image.open(image_path)
        pixels = list(im.getdata())
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
        FillArea.__init__(self, pixels, pos, color, facing, pos_b, connections=connections)


class PillowImageElement(FillArea):
    def __init__(self, im, pos, color=Colors.Black, facing=Facing.FRONT, pos_b=None, connections=Connections()):
        pixels = list(im.getdata())
        width, height = im.size
        pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]
        FillArea.__init__(self, pixels, pos, color, facing, pos_b, connections=connections)


class ColoredPillowImageElement(ElementGroup):
    def __init__(self, im, pos, facing=Facing.FRONT, pos_b=None, connections=Connections()):
        ElementGroup.__init__(self, pos, facing, pos_b, connections)
        pixels = list(im.getdata())
        width, height = im.size
        present_colors = list(c for c in set(pixels) if c[3]==255)

        reverse_colors = {ImageColor.getrgb(c.rgb)+ (255,): c for c in OpaqueColors}
        
        for c in present_colors:
            if c[3] != 255:
                continue
            colored_pixels = [1 if x == c and x[3]>0 else 0 for x in pixels]
            colored_pixels = [colored_pixels[i * width:(i + 1) * width] for i in xrange(height)]
            self.append(FillArea(colored_pixels, pos, reverse_colors[c], facing, pos_b))


if __name__ == '__main__':
    from PIL import Image, ImageDraw, ImageColor

    layered_logo = LayeredImage('logo.png', (0, 0, 0))
    with open('logo.ldr', 'w') as out:
        out.write(layered_logo.to_ldr())

    im = Image.new(mode='1', size=(100, 100))

    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=1, width=10)
    draw.line((0, im.size[1], im.size[0], 0), fill=1, width=10)

    im.save('image.png', format='PNG')

    fill_area = PillowImageElement(im, (0, 0, 0), color=lambda: random.choice(OpaqueColors))
    with open('fill_area_random_color.ldr', 'w') as out:
        out.write(fill_area.to_ldr())
