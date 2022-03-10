from Veldt import Veldt
from DisplayMode import DisplayMode
from FadeCandy import FadeCandy
from Environments import House, Room, Map_2D, Strip
import CommonPatterns as cp

veldt = Veldt()

StateHouse = House()
StateHouse.add_room(Room('Bedroom'))
StateHouse.rooms['Bedroom'].add_strips([
    Strip('SplashA',[20,9],port=0,color_order='BRG'),
    Strip('SplashB',[20,7,20],port=1,color_order='RGB'),
    Strip('SplashC',[20,7],port=3,color_order='RGB'),
    Strip('SplashD',[16,7],port=4,color_order='BRG'),
    Strip('SplashE',[16,7],port=5,color_order='BRG'),
    Strip('Desk',[16,6,16],port=2,color_order='BRG'),
    Strip('Halo',[44],port=7,color_order='RGB')])
map_2D = Map_2D({'label':'Wall Map', 'px_height':32, 'px_width':128})
map_2D.add_segments([
    (StateHouse.rooms['Bedroom'].get_segment('SplashA-1'), (54,1), 'UP'),
    (StateHouse.rooms['Bedroom'].get_segment('SplashA-2'), (55,20), 'RIGHT'),
    (StateHouse.rooms['Bedroom'].get_segment('SplashB-1'), (65,1), 'UP'),
    (StateHouse.rooms['Bedroom'].get_segment('SplashB-2'), (66,19), 'RIGHT'),
    (StateHouse.rooms['Bedroom'].get_segment('SplashB-3'), (74,19), 'DOWN'),
    (StateHouse.rooms['Bedroom'].get_segment('Desk-1'), (66,6), 'NONE'),
    (StateHouse.rooms['Bedroom'].get_segment('Desk-2'), (66,6), 'RIGHT'),
    (StateHouse.rooms['Bedroom'].get_segment('Desk-3'), (74,6), 'NONE')])

StateHouse.get_room('Bedroom').add_2D_map(map_2D)
veldt.add_houses(StateHouse)
veldt.add_fadecandys(FadeCandy('fc1','/dev/ttyUSB0'))

veldt.create_display_mode_lists(['Striptests', 'Standard Patterns', '2D Patterns'])

veldt.add_display_modes('Striptests', [
    DisplayMode(
        dm_vars={'label':'White Striptest', 'func':cp.solid_color,'init_func':None},
        configs={'default':{'hue':0, 'saturation':0, 'brightness':1.0}})])

veldt.add_display_modes('Standard Patterns', [
    DisplayMode(
        dm_vars={'label':'Solid Color', 'func':cp.solid_color, 'init_func':cp.solid_color_init},
        configs={'default':{'hue':0, 'saturation':1.0, 'brightness':1.0}}),
    DisplayMode(
        dm_vars={'label':'Solid Rainbow', 'func':cp.solid_rainbow, 'init_func':cp.solid_rainbow_init},
        configs={'default':{'hue_stepover':0.6, 'saturation':1.0, 'brightness':1.0}}),
    DisplayMode(
        dm_vars={'label':'Rainbow', 'func':cp.rainbow, 'init_func':cp.rainbow_init},
        configs={'default':{'stepover':2.0, 'pitch':1.0, 'jump_gaps':True, 
                 'saturation':1.0, 'brightness':1.0}})])

veldt.add_display_modes('2D Patterns', [
    DisplayMode(
        dm_vars={'label':'2D Rainbow', 'func':cp.rainbow_2D, 'init_func':cp.rainbow_2D_init},
        configs={'default':{'stepover':1.0, 'pitch':5.0, 'direction':'up',
                 'brightness':1.0}})])

veldt.start()