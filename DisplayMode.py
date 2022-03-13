import CommonPatterns as cp
import Room as env

class DisplayMode():
    def __init__(self, dm_vars:dict, configs:dict=None):
        self.name = self.__class__.__name__

        self.label = dm_vars['label']
        self.func = dm_vars['func']
        self.init_func = dm_vars['init_func']
        self.dm_vars = dm_vars
        self.configs = configs
        self.config = list(configs.values())[0]
        self.func_vars = {}

    def get_config_labels(self) -> str:
        return self.configs.keys()

    def select_config(self,config_label:str):
        if config_label in self.configs.keys():
            self.config = self.configs[config_label]

    def get_config(self,config_label:str=None) -> dict:
        if config_label is None:
            return self.config
        else:
            return self.configs[config_label]

    def set_config(self,config:dict):
        self.config = config

    def init(self, room:env.Room):
        print(f'[{self.label}]: Starting')

        if len(self.configs) == 1:
            self.config = list(self.configs.values())[0]
        else:
            print(f'Select configuration (0-{len(self.config.keys())}): ')
            for indx, config in enumerate(self.configs.keys()):
                print(f'{indx+1}: {config}')
            choice = self.configs.values(input(''))
            pass # TODO write support for multiple configs

        self.room = room

        if self.room.msgeq7 is not None:
            self.room.msgeq7.start_listener()

        if self.init_func is not None:
            self.room, self.func_vars, self.config = self.init_func(self.room,self.func_vars,self.config)
        
        if 'lines_printed' in self.func_vars.keys():
            print('Press CTRL+C to exit the display mode')
            return self.func_vars['lines_printed'] 
        else: return 0
    
    def iter(self):
        if self.room.msgeq7 is not None:
            self.room.msgeq7.update()
        self.room, self.func_vars = self.func(self.room,self.func_vars,self.config)
        return self.func_vars['lines_printed'] if 'lines_printed' in self.func_vars.keys() else 0

    def pause(self):
        if self.room.MSGEQ7 is not None:
            self.room.MSGEQ7.close()
        print(f'[{self.label}]: Paused')

    def resume(self):
        if self.room.MSGEQ7 is not None:
            self.room.MSGEQ7.open()
        print(f'[{self.label}]: Resumed')
        print('Press CTRL+C to exit the display mode')



class DisplayModeList():
    def __init__(self, label:str, display_modes:list):
        self.label = label
        self.display_modes = display_modes

    def add_display_mode(self, display_mode:DisplayMode):
        self.display_modes.append(display_mode)

    def add_display_modes(self, display_modes:list):
        for display_mode in display_modes:
            self.display_modes.append(display_mode)