import opc, math
import Environments

pixels = [(0,0,0)] * 512
client_port = 'localhost:7892'

# FadeCandy can support 16 bit per channel (0-65536)
default_color_bits = 10 # 10 bit color (0-1024)

def reorder_channels(rgb,RGB_order):
	a = RGB_order[0]
	b = RGB_order[1]
	c = RGB_order[2]
	return rgb[a], rgb[b], rgb[c]

def hsv2rgb(h,s,v,color_bits=None):
    h = float(h)
    s = float(s)
    v = float(v)
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
    r, g, b = int(r * res), int(g * res), int(b * res)
    return r, g, b

def hsvpos2rgb(h,s,v,pos,color_bits=None):
	r, g, b = hsv2rgb(h,s,v,color_bits=color_bits)
	RGB_order = Environments.curr_house.get_RGB_order(pos)
	r, g, b = reorder_channels([r,g,b],RGB_order)
	return r, g, b

def solid_color(f_vars,config):
    client = opc.Client(client_port)
    h = config['hue']
    s = config['saturation']
    b = config['brightness']
    if 'active_pixels' in config.keys():
        active_pixels = config['active_pixels']
    else:
        active_pixels = range(len(pixels))
    for x in active_pixels:
        # pixels[x] = hsvpos2rgb(h,s,b,x,config['color_bits'])
        pixels[x] = hsv2rgb(h,s,b,config['color_bits'])
    client.put_pixels(pixels)