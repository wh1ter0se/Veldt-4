import math

default_color_bits = 8 # 8 bit color (0-255)

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

def hsv2rgb(h,s,v,color_bits=None):
    if color_bits is None: color_bits = default_color_bits
    h = float(h)*(360.0/((2**color_bits)-1)) # convert 0-res to 0-360
    s = float(s) # 0-1.0
    v = float(v) # 0-1.0
    # return hsi2rgb(h,s,v)
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

def hsi2rgb(H:float, S:float, I:float):
    #int r, g, b
    H %= 360.0 # cycle H around to 0-360 degrees
    H = 3.14159*H/180.0 # Convert to radians.
    # S = (S if S<1 else 1) if S>0 else 0 # clamp S and I to interval [0,1]
    # I = (I if I<1 else 1) if I>0 else 0
    S = clamp(S,0,1)
    I = clamp(I,0,1)

    I_mod = 0.85
    I /= I_mod

    # Math! Thanks in part to Kyle Miller.
    if (H < 2.09439):
        r = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
        g = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
        b = 255*I/3*(1-S)
    elif (H < 4.188787):
        H = H - 2.09439
        g = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
        b = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
        r = 255*I/3*(1-S)
    else:
        H = H - 4.188787
        b = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
        r = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
        g = 255*I/3*(1-S)
    return int(clamp(r,0,255)), int(clamp(g,0,255)), int(clamp(b,0,255))