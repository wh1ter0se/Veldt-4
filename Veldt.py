import sys, os
import DisplayMode
from Room import House, Room
from devices.FadeCandy import FadeCandy

# def cls():
#     os.system('cls' if os.name=='nt' else 'clear')

class Veldt():
    def __init__(self, houses:House or list=None):
        if houses is None: self.houses = []  
        elif type(houses) == House: self.houses = [houses]
        elif type(houses) == list: self.houses = houses
        self.dispmode_lists = []
        self.fadecandys = []
        pass

    def add_houses(self, houses:House or list):
        if type(houses) == House:
            self.houses.append(houses)
        elif type(houses) == list: 
            for house in houses:
                self.houses.append(house)

    def add_fadecandys(self, fadecandys:FadeCandy or list):
        if type(fadecandys) == FadeCandy: 
            self.fadecandys.append(fadecandys)
        elif type(fadecandys) == list:
            for fadecandy in fadecandys:
                self.fadecandys.append(fadecandy)

    def create_display_mode_lists(self, display_mode_list_labels:list):
        for label in display_mode_list_labels:
            dispmode_list = DisplayMode.DisplayModeList(label,[])
            self.dispmode_lists.append(dispmode_list)

    def add_display_modes(self, display_mode_list_label:str, display_modes:DisplayMode or list):
        labels = [dml.label for dml in self.dispmode_lists]
        if display_mode_list_label in labels:
            indx = labels.index(display_mode_list_label)
            if type(display_modes) == DisplayMode:
                self.dispmode_lists[indx].add_display_mode(display_modes)
            else:
                self.dispmode_lists[indx].add_display_modes(display_modes)

    def start(self):
        vcli = self.VeldtCLI(self.houses, self.dispmode_lists)
        vcli.start()
    
    class VeldtCLI():
        def __init__(self, houses:list, dispmode_lists:dict):
            self.houses = houses
            self.dispmode_lists = dispmode_lists
            self.lines_written = 0
        
        def print(self, out:str):
            self.lines_written += 1
            print(out)

        def input(self, prompt:str) -> str:
            self.lines_written += 1
            return input(prompt)

        def cls(self, more_lines:int=0):
            for i in range(self.lines_written+more_lines):
                print('\033[A',' '*40,'\033[A')
            self.lines_written = 0
            # os.system('cls' if os.name=='nt' else 'clear')

        def pick_house(self) -> House:
            if len(self.houses) == 1:
                return self.houses[0]
            else:
                self.print('[Pick House]')
                self.print('MULTIPLE HOUSES NOT YET SUPPORTED') # TODO
                return self.houses[0]

        def pick_room(self, house:House) -> Room:
            if len(house.rooms) == 1:
                return list(house.rooms.values())[0]
            else:
                self.print('[Pick Room]')
                self.print('MULTIPLE ROOMS NOT YET SUPPORTED') # TODO
                return list(house.rooms.values())[0]

        def pick_display_mode_list(self) -> DisplayMode.DisplayModeList:
            self.cls()
            self.print('[Main Menu]')
            for indx, dispmode_list in enumerate(self.dispmode_lists):
                self.print(f'{str(indx+1)}) {dispmode_list.label}')
            choice = int(self.input('Pick directory ID: '))
            return self.dispmode_lists[choice-1]

        def pick_display_mode(self, dispmode_list:DisplayMode.DisplayModeList) -> DisplayMode.DisplayMode:
            self.cls()
            self.print('[Pick Display Mode]')
            for indx, dispmode in enumerate(dispmode_list.display_modes):
                self.print(f'{str(indx+1)}) {dispmode.label}')
            choice = int(self.input('Pick Display Mode ID: '))
            return dispmode_list.display_modes[choice-1]

        def pause_menu(self):
            self.cls()
            self.print('[Pause Menu]')
            options = ['Resume', 'Modify Configuration', 'Exit Display Mode']
            for indx,option in enumerate(options):
                self.print(f'{indx+1}) {option}')
            choice = int(self.input('Select an option ID: '))
            while choice not in [1,2,3]:
                choice = int(self.input(f'Select an option ID (1-{len(options)}): '))
            if choice == 1: return 'resume'
            elif choice == 2: return 'edit_config'
            elif choice == 3: return 'exit'
            
        def edit_config(self, config:dict):
            self.print('NOT YET IMPLEMENTED') # TODO
            return config

        def start(self):
            print()
            while True:
                house = self.pick_house()
                room = self.pick_room(house)
                dispmode_list = self.pick_display_mode_list()
                dispmode = self.pick_display_mode(dispmode_list)
                self.lines_written += dispmode.init(room) + 1 # display mode init statement
                while True:
                    try:
                        self.lines_written += dispmode.iter()
                    except KeyboardInterrupt:
                        try:
                            dispmode.pause()
                            choice = self.pause_menu()
                            if choice == 'resume':
                                dispmode.resume()
                            elif choice == 'edit_config':
                                old_conf = dispmode.get_config()
                                new_conf = self.edit_config(old_conf)
                                dispmode.set_config(new_conf)
                                dispmode.resume()
                                self.lines_written += 1
                            elif choice == 'exit': break
                        except KeyboardInterrupt: break