import DisplayMode, subprocess, sys
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
    for dm_list in DisplayMode.dm_list_dir:
        print(str(i) + ') ' + dm_list.label)
        dm_lists.append(dm_list)
        i += 1
    choice = int(input('Pick directory ID: '))
    selected_dm_list = dm_lists[choice-1]
    return selected_dm_list

def start_fcserver():
    print('Starting fcserver')
    try:
        p = subprocess.Popen(['sudo','fcserver','fadecandy/server/config.json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True) #, creationflags=subprocess.CREATE_NEW_CONSOLE
        return p
    except:
        print('Could not start fcserver!')

def main():
    print(sys.argv)
    if len(sys.argv) > 1:
        fcserver = start_fcserver()
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