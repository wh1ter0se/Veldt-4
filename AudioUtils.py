from serial import Serial

class MSGEQ7():
    
    def __init__(self,port,stereo=False):
        self.ser = self.get_serial()
        self.port = port # '/dev/ttyUSB0' usually
        self.stereo = stereo

    def get_serial(self):
        print(f'[MSGEQ7]: Opening serial port \'{self.port}\'')
        ser = Serial(self.port,115200,timeout=1)
        ser.flush()
        return ser

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