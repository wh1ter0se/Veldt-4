import DisplayModes
# import keyboard

def pick_dm(dm_list):
    i = 1
    dms = []
    print()
    for dm in dm_list.dms:
        print(str(i) + ') ' + dm.label)
        dms.append(dm)
        i += 1
    choice = int(input('Pick Function ID: '))
    selected_dm = dms[choice-1]
    return selected_dm

def pick_dm_list():
    i = 1
    dm_lists = []
    print()
    for dm_list in DisplayModes.dm_list_dir:
        print(str(i) + ') ' + dm_list.label)
        dm_lists.append(dm_list)
        i += 1
    choice = int(input('Pick directory ID: '))
    selected_dm_list = dm_lists[choice-1]
    return selected_dm_list

def main():
    
    while True:
        dm_list = pick_dm_list()
        dm = pick_dm(dm_list)
        dm.init()
        while True:
            try:
                dm.run()
            except KeyboardInterrupt:
                dm.pause()
                try:
                    choice = input('Resume display mode (y/n)? ')
                    if 'y' in choice.lower():
                        dm.resume()
                    else: break
                except KeyboardInterrupt: break

main()