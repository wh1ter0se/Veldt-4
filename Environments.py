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
        self.segments = []
        for index, length in enumerate(lengths):
            label = f'{label}-{index}'
            self.segments.append(self.Segment(
                label, length, sum(lengths[:index]), port))

        self.color_order = color_order.upper()
        self.has_W_channel = 'W' in self.color_order
        self.leds_per_m = leds_per_m

    def flip_color_order(self,rgb):
        r = rgb[self.color_order.index('R')]
        g = rgb[self.color_order.index('G')]
        b = rgb[self.color_order.index('B')]
        return (r,g,b)

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

    # Color order flipping happens here
    def get_pixel(self,strip_pos):
        # return self.flip_color_order(self.pixels[strip_pos])
        return self.pixels[strip_pos]

    # Color order flipping happens here
    def get_pixels(self):
        # out = self.pixels
        # for pixel in out:
        #     pixel = self.flip_color_order(pixel)
        # return out
        return self.pixels
        
    def get_abs_pos(self,strip_pos):
        return (self.port*64) + strip_pos

    class Segment():
        def __init__(self,label,length,offset,port):
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
        self.px_buffer = map_config['px_buffer']
        self.segments = map_config

class Map_3D():
    def __init__(self,map_config):
        self.label = map_config['label']
        self.px_height = map_config['px_height']
        self.px_width = map_config['px_width']
        self.px_depth = map_config['px_depth']
        self.px_buffer = map_config['px_buffer']

class Room():
    def __init__(self, label, color_bits=8):
        self.label = label
        self.color_bits = color_bits

        self.strip_count = 8
        self.strips = {}
        self.maps_2D = {}
        self.maps_3D = {}

    def add_strips(self,strips):
        if type(strips) == list:
            for strip in strips:
                self.strips[strip.label] = strip
        else:
            self.strips[strip.label] = strips

    def add_2D_map(self,map_config):
        self.maps_2D[map_config['label']] = Map_2D(map_config)

    def get_strip(self,label) -> Strip:
        if label in self.strips.keys():
            return self.strips[label]

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

    def add_room(self,room):
        self.rooms[room.label] = room

    def get_room(self,room_label) -> Room: 
        if room_label in self.rooms.keys():
            return self.rooms[room_label]

StateHouse = House()
StateHouse.add_room(Room('Bedroom'))
StateHouse.get_room('Bedroom').add_strips([
    Strip('SplashA',[20,9],port=0,color_order='GBR'),
    Strip('SplashB',[20,7,20],port=1,color_order='RBG'),
    Strip('SplashC',[20,7],port=3,color_order='RBG'),
    Strip('SplashD',[16,7],port=4,color_order='GBR'),
    Strip('SplashE',[16,7],port=5,color_order='GBR'),
    Strip('Desk',[16,6,16],port=2,color_order='GBR'),
    Strip('Halo',[44],port=7,color_order='RBG')])


curr_room = StateHouse.get_room('Bedroom')