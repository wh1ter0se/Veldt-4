import opc, math, time
import Room as env
import utils.Color as cu
import math

pixels = [(0,0,0)] * 512
client_port = 'localhost:7892'

def create_ticker(init,stepover,max,enabled=True):
    return {'value':init, 'stepover':stepover, 
            'max':max, 'enabled':enabled}

def tick(ticker_dict):
    if ticker_dict['enabled']:
        ticker_dict['value'] += ticker_dict['stepover']
        ticker_dict['value'] %= ticker_dict['max']
    return ticker_dict

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
    offset = f_vars['tickers']['pos']['value']
    for strip_indx,label in enumerate(room.strips.keys()):
        for i in range(room.strips[label].length):
            hue = (offset+i)*config['pitch'] % (2**room.color_bits)
            room.strips[label].set_pixel_hsv(i,(hue,config['saturation'],config['brightness']))
        room.strips[label] 
        offset += room.strips[label].length if config['jump_gaps'] else strip_indx*64
    return room, f_vars

@pattern_init
def rainbow_2D_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['tickers']['pos'] = create_ticker(init=0, stepover=config['stepover'], max=512)
    return room, f_vars, config

@pattern_init
def rainbow_2D_vec_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['tickers']['pos'] = create_ticker(init=0, stepover=config['stepover'], max=512)
    f_vars['direction'] = input('Enter unit circle direction in degrees (0-360): ')
    return room, f_vars, config

@pattern ## TODO add support for multiple maps
def rainbow_2D(room:env.Room, f_vars:dict, config:dict):
    map_2D = list(room.maps_2D.values())[0] 

    def func_2D(x:float, y:float):
        offset = f_vars['tickers']['pos']['value']
        pxdir = config['direction'].lower()
        if pxdir == 'left': offset += x
        elif pxdir == 'right': offset -= x
        elif pxdir == 'down': offset += y
        elif pxdir == 'up': offset -= y
        else: # direction in degrees, unit circle
            try:
                vecdir = float(pxdir)
                offset += x*math.cos(vecdir) + y*math.sin(vecdir)
            except: pass

        hue = offset*config['pitch'] % (2**room.color_bits)
        return cu.hsv2rgb(hue, 1.0, config['brightness'])

    room.pixels = map_2D.get_pixels_from_func(func_2D)
    return room, f_vars

@pattern_init
def spinning_rainbow_2D_init(room:env.Room, f_vars:dict, config:dict):
    f_vars['tickers']['pos'] = create_ticker(init=0, stepover=config['stepover'], max=512)
    f_vars['tickers']['dir'] = create_ticker(init=0, stepover=config['angle_stepover'], max=360)
    return room, f_vars, config

@pattern ## TODO add support for multiple maps
def spinning_rainbow_2D(room:env.Room, f_vars:dict, config:dict):
    map_2D = list(room.maps_2D.values())[0] 

    def func_2D(x:float, y:float):
        offset = f_vars['tickers']['pos']['value']
        vecdir = f_vars['tickers']['dir']['value']
        offset += x*math.cos(vecdir) + y*math.sin(vecdir)
        hue = offset*config['pitch'] % (2**room.color_bits)
        return cu.hsv2rgb(hue, 1.0, config['brightness'])

    room.pixels = map_2D.get_pixels_from_func(func_2D)
    return room, f_vars