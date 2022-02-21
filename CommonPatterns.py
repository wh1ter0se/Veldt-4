import opc, math
import Environments as env

pixels = [(0,0,0)] * 512
client_port = 'localhost:7892'

# FadeCandy can support 16 bit per channel (0-65536)
default_color_bits = 10 # 10 bit color (0-1024)


## Utils

def reorder_channels(rgb,RGB_order):
	a = RGB_order[0]
	b = RGB_order[1]
	c = RGB_order[2]
	return rgb[a], rgb[b], rgb[c]

def hsv2rgb(h,s,v,color_bits=None):
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
    r, g, b = int(r * res), int(g * res), int(b * res)
    return r, g, b


## Decorators

def pattern_init(init_func):
    def func_wrapper(room:env.Room, f_vars:dict, config:dict):
        if 'color_bits' in config.keys():
            room.set_color_bits(config['color_bits'])
        room, f_vars, config = init_func(room,f_vars,config)
        return room, f_vars, config
    return func_wrapper

def pattern(func):
    def func_wrapper(room:env.Room, f_vars:dict, config:dict):
        client = opc.Client(client_port)
        room, f_vars = func(room,f_vars,config)
        client.put_pixels(room.get_pixels())
        return f_vars
    return func_wrapper


## Patterns

@pattern_init
def solid_color_init(room:env.Room, f_vars:dict, config:dict):
    print(" 0      60     120    180     240    300")
    print("Red   Violet   Blue   Cyan   Green  Yellow")
    hue = int(input("Hue (0-360): "))
    config['hue'] = hue*(room.color_bits / 360.0)
    return room, f_vars, config

@pattern
def solid_color(room:env.Room, f_vars:dict, config:dict):
    # for x in room.get_all_pixel_pos(): 
    #     pixels[x] = hsv2rgb(h,s,b,config['color_bits'])
    room.fill_hsv(config['hue'], config['saturation'], config['brightness'])
    return room, f_vars

@pattern_init
def solid_rainbow_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['hue_tick'] = 0
    f_vars['hue_tick_max'] = room.color_bits
    f_vars['hue_tick_step'] = config['hue_stepover']
    return room, f_vars, config

@pattern
def solid_rainbow(room:env.Room, f_vars:dict, config:dict):
    f_vars['hue_tick'] += f_vars['hue_tick_step']
    f_vars['hue_tick'] %= f_vars['hue_tick_max']
    room.fill_hsv(f_vars['hue_tick'], config['saturation'], config['brightness'])
    return room, f_vars