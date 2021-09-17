from PIL import Image
import numpy as np

im = Image.open('files/second_hint.bmp')
pixels = list(im.getdata())
new_pixels = [255 if pixel & 0x1 == 1 else 0 for pixel in pixels]
array = np.array(new_pixels, dtype=np.uint8)
new_image = Image.frombuffer("L", (512, 512), array)
new_image.save('2.bmp')