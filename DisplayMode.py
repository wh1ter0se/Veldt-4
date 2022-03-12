import AudioUtils as au
import CommonPatterns as cp
import Environments as env

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

        # self.MSGEQ7 = None
        # if 'uses_MSGEQ7' in self.dm_vars.keys():
        #     if self.dm_vars['uses_MSGEQ7']:
        #         self.MSGEQ7 = au.MSGEQ7(self.dm_vars['stereo'])
        #         bands = 14 if self.dm_vars['stereo'] else 7
        #         self.func_vars['levels'] = [-1 for i in range(bands)]
        #         self.func_vars['stale_levels'] = []
        #         self.stale_level_count = self.dm_vars['stale_level_count']

        if self.init_func is not None:
            self.room, self.func_vars, self.config = self.init_func(self.room,self.func_vars,self.config)
        
        if 'lines_printed' in self.func_vars.keys():
            print('Press CTRL+C to exit the display mode')
            return self.func_vars['lines_printed'] 
        else: return 0
    
    def iter(self):
        if self.room.msgeq7 is not None:
            self.room.msgeq7.update()
        #     levels = self.MSGEQ7.read_levels()
        #     if levels is not None:
        #         self.func_vars['stale_levels'].insert(self.func_vars['levels'])
        #         if len(self.func_vars['stale_levels']) > self.stale_level_count:
        #             self.stale_levels.pop()
        #         self.func_vars['levels'] = levels

        # self.room, self.func_vars = self.func(self.room,self.func_vars,self.config)
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


## DisplayModes

dm_white_striptest = DisplayMode(
    dm_vars={'label':'White Striptest', 'func':cp.solid_color,'init_func':None},
    configs={'default':{'hue':0, 'saturation':0, 'brightness':1.0,'color_bits':8}})

dm_solid_color = DisplayMode(
    dm_vars={'label':'Solid Color', 'func':cp.solid_color, 'init_func':cp.solid_color_init},
    configs={'default':{'hue':0, 'saturation':1.0, 'brightness':1.0,'color_bits':8}})

dm_solid_rainbow = DisplayMode(
    dm_vars={'label':'Solid Rainbow', 'func':cp.solid_rainbow, 'init_func':cp.solid_rainbow_init},
    configs={'default':{'hue_stepover':0.6, 'saturation':1.0, 'brightness':1.0,'color_bits':8}})

## DisplayModeLists

striptest_dm_list = DisplayModeList('Striptests',
                   [dm_white_striptest])
standard_dm_list = DisplayModeList('Standard Patterns',
                   [dm_solid_color,
                   dm_solid_rainbow])

## dm_list_dir
dm_list_dir = [striptest_dm_list,
               standard_dm_list]