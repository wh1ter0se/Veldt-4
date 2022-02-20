import numpy as np

class Strip():
    # Lengths should be a list of ints in order to support brdiges in the strip
    def __init__(self, label, lengths:list, port:int, color_order:str='RGB'):
        self.label = label
        self.port = port
        self.lengths = lengths
        self.length = sum(lengths)
        self.segments = []
        for index, length in enumerate(lengths):
            label = f'{label}-{index}'
            self.segments.append(self.Segment(
                label, length, sum(lengths[:index]), port))

        self.color_order = color_order.upper()
        self.has_W_channel = 'W' in self.color_order

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

    def get_abs_pos(self,strip_pos):
        return (self.port*64) + strip_pos

class Room():
    def __init__(self, label):
        self.label = label
        self.canvas_width = 200
        self.canvas_height = 200
        self.canvas_buffer = 20

        self.strip_count = 8
        self.strips = {}

    def add_strip(self,strip):
        self.strips[strip.label] = strip

    def add_strips(self,strips):
        if type(strips) == list:
            for strip in strips:
                self.strips[strip.label] = strip
        else:
            self.strips[strip.label] = strips

    def get_strip(self,label) -> Strip:
        if label in self.strips.keys():
            return self.strips[label]

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
    Strip('SplashA',[20,9],port=0,color_order='RGB'),
    Strip('SplashB',[20,7,20],port=1,color_order='RGB'),
    Strip('SplashC',[20,7],port=3,color_order='RGB'),
    Strip('SplashD',[16,7],port=4,color_order='RGB'),
    Strip('SplashE',[16,7],port=5,color_order='RGB'),
    Strip('Desk',[16,6,16],port=2,color_order='RGB'),
    Strip('Halo',[44],port=7,color_order='RGB')])


curr_room = StateHouse.get_room('Bedroom')