from serial import Serial

class MSGEQ7():
    
    def __init__(self, port:str, stereo:bool=False, stale_buffer:int=3):
        self.port = port # '/dev/ttyUSB0' usually
        self.stereo = stereo
        self.stale_buffer = stale_buffer
        

    def init(self):
        self.ser = self.get_serial()

        self.bands = 14 if self.dm_vars['stereo'] else 7
        self.empty_levels = [0 for i in range(self.bands)]

        self.levels = self.empty_levels
        self.stale_levels = [self.empty_levels for i in range(self.stale_buffer)]

    def iter(self):
        pass

    def get_serial(self):
        print(f'[MSGEQ7]: Opening serial port \'{self.port}\'')
        ser = Serial(self.port,115200,timeout=1)
        ser.flush()
        return ser

    def update_stale_levels(self):
        for i in reversed(range(self.stale_buffer-1))+1:
            self.stale_buffer[i] = self.stale_buffer[i-1]
        self.stale_buffer = self.stale_buffer[:-1]

    def set_stale_buffer(self,buf:int):
        if buf < self.stale_buffer:
            self.stale_levels = self.stale_levels[buf]
        elif buf > self.stale_buffer:
            for i in range(self.stale_buffer-buf):
                self.stale_levels.append(self.empty_levels)
        self.stale_buffer = buf

    def read_levels(self):
        if(self.ser.in_waiting>0):
            while(self.ser.in_waiting>0): # get most recent line
                line = self.ser.readline().decode('utf-8')+ ' '
            try:
                levels = [int(n) for n in line.split()]
            except ValueError: pass
            if self.is_valid(levels):
                return levels

    def is_valid(levels):
        for i in range(7):
            try:
                if int(levels[i]) < 0: return False
            except: return False
        return True

    def open(self):
        try:
            print(f'[MSGEQ7]: Opening serial port \'{self.port}\'')
            self.ser.open(timeout=1)
            self.ser.flush()
            return True
        except:
            print(f'[MSGEQ7] Serial port could not be opened')
            return False

    def close(self):
        print(f'[MSGEQ7]: Closing serial port \'{self.port}\'')
        self.ser.close()