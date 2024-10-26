import oklab
import numpy as np
from PIL import Image

fg = oklab.okcolor([0.10, 0.01, 312])
fg1 = oklab.okcolor([0.30, 0.01, 12])
fg2 = oklab.okcolor([0.30, 0.01, 252])
bg = oklab.okcolor([0.95, 0.01, 132])
bg1 = oklab.okcolor([0.80, 0.01, 72])
bg2 = oklab.okcolor([0.80, 0.01, 192])
foreground = [oklab.okcolor([0.50, 0.09, c * 60 + 42]) for c in range(6)]
background = [oklab.okcolor([0.60, 0.09, c * 60 + 42]) for c in range(6)]


def generate_pixels(colours: list, name):
    width = 800
    height = 100
    block_width = int(width / len(colours))
    block_remainder = width % len(colours)

    for i, c in enumerate(colours):
        colour = np.array(c, dtype=np.uint8)
        if i == 0:
            pixels = np.tile(colour, (height, block_width + block_remainder, 1))
            continue
        block = np.tile(colour, (height, block_width, 1))
        pixels = np.concatenate((pixels, block), axis=1)

    Image.fromarray(pixels, mode="RGB").save(name)


colors = [bg, bg1, bg2, fg1, fg2, fg]
colors.extend(foreground)
colors.extend(background)
rgb = [color.rgb * 255 for color in colors]
generate_pixels(rgb, "theme.png")

luminance = [color.luminance + 0.05 for color in colors]
for i in luminance:
    print(i)

hexs = [color.hex for color in colors]
for i in hexs:
    print(i)
