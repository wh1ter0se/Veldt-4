from serial import Serial
from threading import Thread
import asyncio
# import serial_asyncio

class MSGEQ7():
    def __init__(self, port:str, stereo:bool=False, stale_buffer:int=3):
        self.port = port # '/dev/ttyUSB0' usually
        self.stereo = stereo
        self.stale_buffer = stale_buffer
        
        try: self.ser = Serial(self.port,115200,timeout=1)
        except:
            print(f'[MSGEQ7]: Serial port \'{self.port}\' could not be opened.')
            raise

        self.bands = 14 if self.stereo else 7
        self.empty_levels = [0 for i in range(self.bands)]
        self.levels = self.empty_levels
        self.stale_levels = [self.empty_levels for i in range(self.stale_buffer)]

        self.queue = asyncio.Queue()

    def open(self):
        try:
            print(f'[MSGEQ7]: Opening serial port \'{self.port}\'.')
            self.ser.open(timeout=1)
            self.ser.flush()
            return True
        except:
            print(f'[MSGEQ7] Serial port \'{self.port}\' could not be opened.')
            return False

    def close(self):
        print(f'[MSGEQ7]: Closing serial port \'{self.port}\'.')
        self.ser.close()

    def start_listener(self):
        def asyncloop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        
        async def listener(self, q:asyncio.Queue):
            levels = self.read_levels()
            q.put(levels)

        loop = asyncio.new_event_loop()
        t = Thread(target=asyncloop, args=(loop,), daemon=True)
        t.start()
        asyncio.run_coroutine_threadsafe(listener(self.queue), loop)

    def update(self):
        def update_stale_levels(self):
            for i in reversed(range(self.stale_buffer-1))+1:
                self.stale_buffer[i] = self.stale_buffer[i-1]
            self.stale_buffer = self.stale_buffer[:-1]
            self.stale_buffer[0] = self.levels

        try:
            levels = self.queue.get_nowait()
            for level in levels:
                if type(level) is not int or level < 0: return
            self.levels = levels
            update_stale_levels()
        except asyncio.QueueEmpty: pass

    def read_levels(self):
        if(self.ser.in_waiting>0):
            while(self.ser.in_waiting>0): # get most recent line
                line = self.ser.readline().decode('utf-8')+ ' '
            try:
                levels = [int(n) for n in line.split()]
            except ValueError: pass
            if self.is_valid(levels):
                return levels

    def set_stale_buffer(self,buf:int):
        if buf < self.stale_buffer:
            self.stale_levels = self.stale_levels[buf]
        elif buf > self.stale_buffer:
            for i in range(self.stale_buffer-buf):
                self.stale_levels.append(self.empty_levels)
        self.stale_buffer = buf