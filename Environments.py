from typing import Callable
from MSGEQ7 import MSGEQ7
import numpy as np
import CommonPatterns as cp

class Strip():
    # Lengths should be a list of ints in order to support brdiges in the strip
    def __init__(self, label, lengths:list, port:int, color_order:str='RGB', leds_per_m:int=30):
        self.label = label
        self.port = port
        self.enabled = True
        self.lengths = lengths
        self.length = sum(lengths)
        self.pixels = [(0,0,0) for i in range(self.length)]
        self.segments = {}
        for index, length in enumerate(lengths,1):
            seg_label = f'{label}-{index}' # index starts at 1
            self.segments[seg_label] = (self.Segment(self,
                seg_label, length, sum(lengths[:index]), port))

        self.color_order = color_order.upper()
        self.has_W_channel = 'W' in self.color_order
        self.leds_per_m = leds_per_m

    def flip_color_order(self,rgb):
        r,g,b = rgb
        if self.color_order == 'RGB': return r,g,b
        elif self.color_order == 'RBG': return r,b,g
        elif self.color_order == 'BRG': return b,r,g
        elif self.color_order == 'BGR': return b,g,r
        elif self.color_order == 'GBR': return g,b,r
        elif self.color_order == 'GRB': return g,r,b

    def set_pixel_rgb(self,strip_pos,rgb):
        r,g,b = self.flip_color_order(rgb)
        self.pixels[strip_pos] = (int(r),int(g),int(b))

    def set_pixel_hsv(self,strip_pos,hsv,color_bits=None):
        rgb = cp.hsv2rgb(*hsv,color_bits)
        self.set_pixel_rgb(strip_pos, rgb)

    def fill_rgb(self,rgb,color_bits=None):
        for i in range(self.length):
            self.set_pixel_rgb(i,rgb,color_bits)

    def fill_hsv(self,hsv,color_bits=None):
        for i in range(self.length):
            self.set_pixel_hsv(i,hsv,color_bits)
    
    def clear(self):
        self.fill_rgb((0,0,0))

    def get_pixel(self,strip_pos):
        return self.pixels[strip_pos]

    def get_pixels(self):
        return self.pixels
        
    def get_abs_pos(self,strip_pos):
        return (self.port*64) + strip_pos

    class Segment():
        def __init__(self, strip, label:str, length:int, offset:int ,port:int):
            self.strip = strip
            self.label = label
            self.length = length
            self.offset = offset
            self.port = port
        
        def get_strip_pos(self,seg_pos):
            return self.offset + seg_pos

        def get_abs_pos(self,seg_pos):
            return (self.port*64) + self.offset + seg_pos

    def as_segment(self):
        return self.Segment(self.label,self.length,0,self.port)
    
# 1 pixel = 3 lights
# 30 leds/m --> 1 pixel = 10cm ~ 3.94in
class Map_2D():
    def __init__(self,map_config):
        self.label = map_config['label']
        self.px_height = map_config['px_height']
        self.px_width = map_config['px_width']
        #self.px_buffer = 0 #map_config['px_buffer']
        self.segment_tuples = []

    def add_segment(self, segment:Strip.Segment, start_pos:tuple, direction:str=None):
        '''Adds segment info to 2D map.
           
           Arguments
           - segment -  Strip.Segment object to add
           - start_pos -  (x,y) tuple for segment position 0
           - direction -  'UP', 'DOWN', 'LEFT', 'RIGHT', or None'''
        self.segment_tuples.append((segment, start_pos, direction))

    def add_segments(self, segment_tuples:list):
        '''Adds a list of segment tuples directly.'''
        for segtup in segment_tuples:
            self.segment_tuples.append(segtup)

    def get_pixels_from_func(self, func_2D:Callable[[float,float],tuple]):
        '''Applies the mapped pixels to a function which takes
           only X and Y as parameters and returns an RGB tuple.
           Returns the pixel map for a single FadeCandy.'''
        pixels = [(0,0,0)] * 512
        for segment, start_pos, direction in self.segment_tuples:
            def add_tup(tup_a, tup_b):
                return tuple(map(sum, zip(tup_a, tup_b)))
            curr_pos = start_pos
            if direction == 'UP': 
                curr_pos = add_tup(curr_pos, (0,1)) 
            elif direction == 'DOWN': 
                curr_pos = add_tup(curr_pos, (0,-1)) 
            elif direction == 'LEFT': 
                curr_pos = add_tup(curr_pos, (-1,0)) 
            elif direction == 'RIGHT': 
                curr_pos = add_tup(curr_pos, (1,0)) 

            for i in range(segment.length):
                abs_pos = segment.get_abs_pos(i)
                pixels[abs_pos] = func_2D(*curr_pos)
        return pixels

class Map_3D():
    def __init__(self,map_config):
        self.label = map_config['label']
        self.px_height = map_config['px_height']
        self.px_width = map_config['px_width']
        self.px_depth = map_config['px_depth']
        self.px_buffer = map_config['px_buffer']

class Room():
    def __init__(self, label:str, color_bits:int=8):
        self.label = label
        self.color_bits = color_bits

        self.strip_count = 8
        self.pixel_count = 64 * self.strip_count
        self.strips = {}
        self.maps_2D = {}
        self.maps_3D = {}

        self.msgeq7 = None
        self.pixels = None

    def add_strips(self, strips:Strip or list):
        if type(strips) == list:
            for strip in strips:
                self.strips[strip.label] = strip
        elif type(strips) == Strip:
            self.strips[strips.label] = strips

    def add_2D_map(self, map:Map_2D):
        self.maps_2D[map.label] = map

    def add_MSGEQ7(self, msgeq7:MSGEQ7):
        if self.msgeq7 is not None:
            print('Overridding MSGEQ7')
        self.msgeq7 = msgeq7

    def get_segment(self,label):
        for strip in self.strips.values():
            if label in strip.segments.keys():
                return strip.segments[label]
        raise NameError(f'Segment \'{label}\' not found')
        
    def print_segments(self):
        for strip in self.strips.values():
            for label in strip.segments.keys():
                print(label)

    def set_strip_enabled(self,label,enabled=True):
        if label in self.strips.keys():
            self.strips[label].enabled = enabled

    def set_color_bits(self,color_bits):
        self.color_bits = color_bits

    def fill_rgb(self,r,g,b):
        for strip in self.strips.values():
            strip.fill_rgb((r,g,b),self.color_bits)

    def fill_hsv(self,h,s,v):
        for strip in self.strips.values():
            strip.fill_hsv((h,s,v),self.color_bits)

    def get_pixels(self):
        if self.pixels is not None:
            return self.pixels
        pixels = [(0,0,0) for i in range(64*self.strip_count)]
        for strip in self.strips.values():
            subpixels = strip.get_pixels()
            offset = strip.port * 64
            for i in range(strip.length):
                pixels[offset+i] = subpixels[i]
        return pixels

    def get_all_pixel_pos(self):
        px_pos = []
        for strip in self.strips.values():
            for px in range(strip.length):
                px_pos.append(64*strip.port + px)
        return px_pos


class House():
    def __init__(self, rooms:list=None):
        self.rooms = {}
        if rooms is not None:
            for room in rooms: 
                self.rooms[room.label] = room

    def add_room(self, room:Room):
        self.rooms[room.label] = room

    def get_room(self,room_label) -> Room: 
        if room_label in self.rooms.keys():
            return self.rooms[room_label]

# StateHouse = House()
# StateHouse.add_room(Room('Bedroom'))
# StateHouse.get_room('Bedroom').add_strips([
#     Strip('SplashA',[20,9],port=0,color_order='GBR'),
#     Strip('SplashB',[20,7,20],port=1,color_order='RBG'),
#     Strip('SplashC',[20,7],port=3,color_order='RBG'),
#     Strip('SplashD',[16,7],port=4,color_order='GBR'),
#     Strip('SplashE',[16,7],port=5,color_order='GBR'),
#     Strip('Desk',[16,6,16],port=2,color_order='GBR'),
#     Strip('Halo',[44],port=7,color_order='RBG')])


# curr_room = StateHouse.get_room('Bedroom')