import math

default_color_bits = 8 # 8 bit color (0-255)

def hsv2rgb(h,s,v,color_bits=None):
    if color_bits is None: color_bits = default_color_bits
    h = float(h)*(360.0/((2**color_bits)-1)) # convert 0-res to 0-360
    s = float(s) # 0-1.0
    v = float(v) # 0-1.0
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    if color_bits is None:
        color_bits = default_color_bits
    res = 2**color_bits
    r, g, b = int(r*(res-1)), int(g*(res-1)), int(b*(res-1))
    return r, g, b