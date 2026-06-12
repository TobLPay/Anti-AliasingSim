import numpy as np
from PIL import Image

cal = 0
img = Image.open('input4x.png').convert("L")
arr = np.array(img)
matrix = np.where(arr < 128, 255, 0).astype(np.uint8)
drawarr = []
matrix = matrix.astype(np.int32)
for y in range(200):
    row = []
    for x in range(300):
        if (matrix[y*4][x*4] == matrix[y*4][x*4+1] == matrix[y*4][x*4+2] == matrix[y*4][x*4+3] ==
            matrix[y*4+1][x*4] == matrix[y*4+1][x*4+1] == matrix[y*4+1][x*4+2] == matrix[y*4+1][x*4+3] ==
            matrix[y*4+2][x*4] == matrix[y*4+2][x*4+1] == matrix[y*4+2][x*4+2] == matrix[y*4+2][x*4+3] ==
            matrix[y*4+3][x*4] == matrix[y*4+3][x*4+1] == matrix[y*4+3][x*4+2] == matrix[y*4+3][x*4+3]):
            row.append(255-matrix[y*4][x*4])
            cal += 1
            continue
        total = (
            matrix[y*4][x*4] + matrix[y*4][x*4+1] + matrix[y*4][x*4+2] + matrix[y*4][x*4+3] +
            matrix[y*4+1][x*4] + matrix[y*4+1][x*4+1] + matrix[y*4+1][x*4+2] + matrix[y*4+1][x*4+3] +
            matrix[y*4+2][x*4] + matrix[y*4+2][x*4+1] + matrix[y*4+2][x*4+2] + matrix[y*4+2][x*4+3] +
            matrix[y*4+3][x*4] + matrix[y*4+3][x*4+1] + matrix[y*4+3][x*4+2] + matrix[y*4+3][x*4+3]
        )
        row.append(255-(total // 16))
        cal += 16
    drawarr.append(row)
drawarr = np.array(drawarr, dtype=np.uint8)
newimg = Image.fromarray(drawarr, mode='L')
newimg.save('MSAA4x_output.png')
print(cal)
newimg.show()