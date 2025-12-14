import os
from PIL import Image

def process_masks(folder):
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        img = Image.open(path)
        pixels = img.load()

        width, height = img.size

        for y in range(height):
            for x in range(width):
                if pixels[x, y] > 0:     
                    pixels[x, y] = 255     

        img.save(path)


process_masks('./data/masks')

