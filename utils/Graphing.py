from skimage import io
from matplotlib import pyplot as plt
import Color as cu
import numpy as np
import sys, math
sys.path.insert(0, './utils')

def graph_2D_func(func_2D, height, width, stepover, x_start=0, y_start=0):
    ticker = 0
    plt.ion()
    fig = plt.figure()
    while True:
        ticker += stepover
        ticker %= 255
        pixels = []
        for y in range(y_start, height-y_start):
            row = []
            for x in range(x_start, width-x_start):
                row.append(list(func_2D(x,y,ticker)))
            pixels.append(row)
        np_pixels = np.array(pixels,dtype=int).astype(np.uint8)
        io.imshow(np_pixels)
        fig.canvas.draw()
        fig.canvas.flush_events()

def func_2D(x:float, y:float, offset:int):
    # offset = 0 #f_vars['tickers']['pos']['value']
    pxdir = '45'
    if pxdir == 'left': offset += x
    elif pxdir == 'right': offset -= x
    elif pxdir == 'down': offset += y
    elif pxdir == 'up': offset -= y
    else: # direction in degrees, unit circle
        try:
            vecdir = 0.1*(offset * (360.0/255.0)) % 360.0#float(pxdir)
            offset += x*math.cos(vecdir) + y*math.sin(vecdir)
        except: pass
        
    hue = offset*3.0 % (2**8)
    return cu.hsv2rgb(hue, 1.0, 1.0)

graph_2D_func(func_2D, 32, 128, .5)