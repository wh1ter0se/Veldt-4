import matplotlib.pyplot as plt
import numpy as np
from perlin_noise import PerlinNoise
from skimage import io
import utils.Color as cu

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

def generate_frame(fig,x_offset,y_offset):
    xpix, ypix = 100, 100
    pic = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            x = (i/xpix + x_offset)
            y = (j/ypix + y_offset)
            noise_val = noise1([x, y])
            noise_val += 0.5 * noise2([x, y])
            noise_val += 0.25 * noise3([x, y])
            noise_val += 0.125 * noise4([x, y])
            val = cu.hsv2rgb(noise_val*255.0,1.0,1.0)
            row.append(val)
        pic.append(row)
    pixels = np.array(pic,dtype=int).astype(np.uint8)
    io.imshow(pixels)
    fig.canvas.draw()
    fig.canvas.flush_events()

plt.ion()
pfig = plt.figure()
step = 0
while True: 
    try:
        generate_frame(pfig,step,step)
        step += .1
    except: break