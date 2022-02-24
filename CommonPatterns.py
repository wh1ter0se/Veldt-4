import opc, math, time
import Environments as env

pixels = [(0,0,0)] * 512
client_port = 'localhost:7892'

# FadeCandy can support 16 bit per channel (0-65536)
default_color_bits = 8 # 8 bit color (0-255)


## Utils

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
    r, g, b = int(r * res), int(g * res), int(b * res)
    return r, g, b

def create_ticker(init,stepover,max,enabled=True):
    return {'value':init, 'stepover':stepover, 
            'max':max, 'enabled':enabled}

def tick(ticker_dict):
    if ticker_dict['enabled']:
        ticker_dict['value'] += ticker_dict['stepover']
        ticker_dict['value'] %= ticker_dict['max']
    return ticker_dict

## Decorators

def pattern_init(init_func):
    def func_wrapper(room:env.Room, f_vars:dict, config:dict):
        f_vars['tickers'] = {}
        if 'color_bits' in config.keys():
            room.set_color_bits(config['color_bits'])
        room_, f_vars_, config_ = init_func(room,f_vars,config)
        return room_, f_vars_, config_
    return func_wrapper

def pattern(func):
    def func_wrapper(room:env.Room, f_vars:dict, config:dict):
        client = opc.Client(client_port)
        if 'tickers' in f_vars.keys():
            for ticker in f_vars['tickers'].values():
                ticker = tick(ticker)
        room_, f_vars_ = func(room,f_vars,config)
        client.put_pixels(room.get_pixels())
        return room_, f_vars_
    return func_wrapper

## Patterns

@pattern_init
def solid_color_init(room:env.Room, f_vars:dict, config:dict):
    print(" 0      60     120    180     240    300")
    print("Red   Violet   Blue   Cyan   Green  Yellow")
    hue = float(int(input("Hue (0-360): ")))
    config['hue'] = int(hue*((2**room.color_bits) / 360.0))
    f_vars['lines_printed'] = 3
    return room, f_vars, config

@pattern
def solid_color(room:env.Room, f_vars:dict, config:dict):
    room.fill_hsv(config['hue'], config['saturation'], config['brightness'])
    return room, f_vars

@pattern_init
def solid_rainbow_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['tickers']['hue'] = create_ticker(init=0, stepover=config['hue_stepover'], max=2**room.color_bits)
    return room, f_vars, config

@pattern
def solid_rainbow(room:env.Room, f_vars:dict, config:dict):
    f_vars['last_detect'] = time.time()
    room.fill_hsv(f_vars['tickers']['hue']['value'], config['saturation'], config['brightness'])
    return room, f_vars

@pattern_init
def rainbow_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['tickers']['pos'] = create_ticker(init=0, stepover=config['stepover'], max=512)
    return room, f_vars, config

@pattern
def rainbow(room:env.Room, f_vars:dict, config:dict):
    offset = 0
    for strip_indx,label in enumerate(room.strips.keys()):
        for i in range(room.strips[label].length):
            hue = (offset+i)*config['pitch']
            room.strips[label].set_pixel_hsv(i,(hue,config['saturation'],config['brightness']))
        room.strips[label] 
        offset += room.strips[label].length if config['jump_gaps'] else strip_indx*64
    return room, f_vars