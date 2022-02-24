from Veldt import Veldt
from DisplayMode import DisplayMode
from FadeCandy import FadeCandy
from Environments import House, Room, Strip
import CommonPatterns as cp

veldt = Veldt()

StateHouse = House()
StateHouse.add_room(Room('Bedroom'))
StateHouse.get_room('Bedroom').add_strips([
    Strip('SplashA',[20,9],port=0,color_order='GRB'),
    Strip('SplashB',[20,7,20],port=1,color_order='RGB'),
    Strip('SplashC',[20,7],port=3,color_order='GRB'),
    Strip('SplashD',[16,7],port=4,color_order='GRB'),
    Strip('SplashE',[16,7],port=5,color_order='GRB'),
    Strip('Desk',[16,6,16],port=2,color_order='GRB'),
    Strip('Halo',[44],port=7,color_order='RGB')])
veldt.add_houses(StateHouse)
veldt.add_fadecandys(FadeCandy('fc1','/dev/ttyUSB0'))

veldt.create_display_mode_lists(['Striptests', 'Standard Patterns'])

veldt.add_display_modes('Striptests', [
    DisplayMode(
        dm_vars={'label':'White Striptest', 'func':cp.solid_color,'init_func':None},
        configs={'default':{'hue':0, 'saturation':0, 'brightness':1.0,'color_bits':8}})])

veldt.add_display_modes('Standard Patterns', [
    DisplayMode(
        dm_vars={'label':'Solid Color', 'func':cp.solid_color, 'init_func':cp.solid_color_init},
        configs={'default':{'hue':0, 'saturation':1.0, 'brightness':1.0,'color_bits':8}}),
    DisplayMode(
        dm_vars={'label':'Solid Rainbow', 'func':cp.solid_rainbow, 'init_func':cp.solid_rainbow_init},
        configs={'default':{'hue_stepover':0.6, 'saturation':1.0, 'brightness':1.0,'color_bits':8}})])

veldt.start()