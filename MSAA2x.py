import numpy as np
from PIL import Image

cal = 0
img = Image.open('input2x.png').convert("L")
arr = np.array(img)
matrix = np.where(arr < 128, 255, 0).astype(np.uint8)
drawarr = []
matrix = matrix.astype(np.int32)
for y in range(200):
    row = []
    for x in range(300):
        if matrix[y*2][x*2] == matrix[y*2][x*2+1] == matrix[y*2+1][x*2] == matrix[y*2+1][x*2+1]:
            row.append(255-matrix[y*2][x*2])
            cal += 1
            continue
        total = (
            matrix[y*2][x*2] +
            matrix[y*2][x*2+1] +
            matrix[y*2+1][x*2] +
            matrix[y*2+1][x*2+1]
        )
        row.append(255-(total // 4))
        cal += 4
    drawarr.append(row)
drawarr = np.array(drawarr, dtype=np.uint8)
newimg = Image.fromarray(drawarr, mode='L')
newimg.save('MSAA2x_output.png')
print(cal)
newimg.show()