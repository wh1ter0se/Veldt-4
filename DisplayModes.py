import AudioUtils as au
import CommonPatterns as cp
import Environments as env

class DisplayMode():
    def __init__(self,dm_vars,config=None):
        self.name = self.__class__.__name__

        self.label = dm_vars['label']
        self.func = dm_vars['func']
        self.init_func = dm_vars['init_func']

        self.dm_vars = dm_vars
        self.config = config
        self.func_vars = {}

    def set_config(self,config):
        self.config = config

    def init(self):
        print(f'[{self.name}]: Init')

        self.MSGEQ7 = None
        if 'uses_MSGEQ7' in self.dm_vars.keys():
            if self.dm_vars['uses_MSGEQ7']:
                self.MSGEQ7 = au.MSGEQ7(self.dm_vars['stereo'])
                bands = 14 if self.dm_vars['stereo'] else 7
                self.func_vars['levels'] = [-1 for i in range(bands)]
                self.func_vars['stale_levels'] = []
                self.stale_level_count = self.dm_vars['stale_level_count']
        
        self.room = env.curr_room

        if self.init_func is not None:
            self.room, self.func_vars, self.config = self.init_func(self.room,self.func_vars,self.config)
        
        print('Press CTRL+C to exit the display mode')
    
    def run(self):
        if self.MSGEQ7 is not None:
            levels = self.MSGEQ7.read_levels()
            if levels is not None:
                self.func_vars['stale_levels'].insert(self.func_vars['levels'])
                if len(self.func_vars['stale_levels']) > self.stale_level_count:
                    self.stale_levels.pop()
                self.func_vars['levels'] = levels

        self.room, self.func_vars = self.func(self.room,self.func_vars,self.config)

    def pause(self):
        if self.MSGEQ7 is not None:
            self.MSGEQ7.close()
        print(f'[{self.name}]: Paused')

    def resume(self):
        if self.MSGEQ7 is not None:
            self.MSGEQ7.open()
        print(f'[{self.name}]: Resumed')

class DisplayModeList():
    def __init__(self,label,dms):
        self.label = label
        self.dms = dms


## DisplayModes

dm_white_striptest = DisplayMode(
    dm_vars={'label':'White Striptest', 'func':cp.solid_color,'init_func':None},
    config={'hue':0, 'saturation':0, 'brightness':1.0,'color_bits':8})

dm_solid_color = DisplayMode(
    dm_vars={'label':'Solid Color', 'func':cp.solid_color, 'init_func':cp.solid_color_init},
    config={'hue':0, 'saturation':1.0, 'brightness':1.0,'color_bits':8})

dm_solid_rainbow = DisplayMode(
    dm_vars={'label':'Solid Rainbow', 'func':cp.solid_rainbow, 'init_func':cp.solid_rainbow_init},
    config={'hue_stepover':2.0, 'saturation':1.0, 'brightness':1.0,'color_bits':8})

## DisplayModeLists

striptest_dm_list = DisplayModeList('Striptests',
                   [dm_white_striptest])
standard_dm_list = DisplayModeList('Standard Patterns',
                   [dm_solid_color,
                   dm_solid_rainbow])

## dm_list_dir
dm_list_dir = [striptest_dm_list,
               standard_dm_list]