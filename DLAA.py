import numpy as np
import random
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
import math

wid = 240
hei = 160

def ssaa(arr):
    matrix = np.where(arr < 128, 255, 0).astype(np.uint8)
    drawarr = []
    matrix = matrix.astype(np.int32)
    for y in range(int(hei/2)):
        row = []
        for x in range(int(wid/2)):
            total = (
                matrix[y*2][x*2] +
                matrix[y*2][x*2+1] +
                matrix[y*2+1][x*2] +
                matrix[y*2+1][x*2+1]
            )
            row.append((total // 4))
        drawarr.append(row)
    drawarr = np.array(drawarr, dtype=np.uint8)
    return drawarr

def sangsung():
    x = np.zeros((hei, wid), dtype=np.uint8)

    xl = random.randint(int(wid * 0.1), int(wid * 0.9))
    yl = random.randint(int(hei * 0.1), int(hei * 0.9))

    theta = random.uniform(-80, 80)
    theta = math.radians(theta)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    cx = xl / 2
    cy = yl / 2

    for py in range(hei):
        for px in range(wid):
            dx = px - cx
            dy = py - cy
            xx = dx * cos_t + dy * sin_t
            yy = -dx * sin_t + dy * cos_t
            if abs(xx) <= xl/2 and abs(yy) <= yl/2:
                x[py, px] = 255
    return x

def datasave():
    global data_x, data_y, xd
    data_x.append(xd)
    data_y.append(ssaa(xd))
    
data_x = []
data_y = []

for i in range(300):
    xd = sangsung()
    datasave()

class dlaaClass(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.Sigmoid(),
            nn.Conv2d(32, 64, 3, padding=1, stride=2),
            nn.Sigmoid(),
            nn.Conv2d(64, 32, 3, padding=1),
            nn.Sigmoid(),
            nn.Conv2d(32, 1, 3, padding=1)
        )
    def forward(self, x):
        return self.net(x)
    
max_vel = np.max(np.abs(data_x)) + 1e-7

data_x = np.array(data_x, dtype=np.float32)
data_y = np.array(data_y, dtype=np.float32)

data_x /= max_vel
data_y /= max_vel

X = torch.tensor(data_x, dtype=torch.float32).unsqueeze(1)
Y = torch.tensor(data_y, dtype=torch.float32).unsqueeze(1)

model = dlaaClass()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
X = X.to(device)
Y = Y.to(device)

for epoch in range(500):
    pred = model(X)
    loss = criterion(pred, Y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if epoch % 5 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item()}')

resp = input("Save model? (y/n): ")
with torch.no_grad():
    if resp.lower() == 'y':
        torch.save(model.state_dict(), 'dlaa_model.pth')
        print("Model saved as dlaa_model.pth")
        field = sangsung()
        field_img = Image.fromarray(field, mode='L')
        field_img.save('dlaa_input.png')
        field_img.show()
        test_x = field.astype(np.float32) / max_vel
        test_x = torch.tensor(test_x, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(device)
        with torch.no_grad():
            pred = model(test_x)
        pred = pred.squeeze().cpu().numpy()
        pred = np.clip(pred * max_vel, 0, 255).astype(np.uint8)
        pred_img = Image.fromarray(pred, mode='L')
        pred_img.save('dlaa_output.png')
        pred_img.show()
