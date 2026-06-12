import numpy as np
from PIL import Image

img = Image.open('input.png').convert("L")
arr = np.array(img)
matrix = np.where(arr < 128, 255, 0).astype(np.uint8)
'''for row in matrix:
    print(*row)'''
drawarr = (255 - matrix).astype(np.uint8)
newimg = Image.fromarray(drawarr, mode='L')
newimg.save('output.png')
newimg.show()