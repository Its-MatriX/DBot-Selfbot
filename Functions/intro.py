intro_text = ''' _____  ____        _      _____      _  __ _           _   
|  __ \|  _ \      | |    / ____|    | |/ _| |         | |
| |  | | |_) | ___ | |_  | (___   ___| | |_| |__   ___ | | 
| |  | |  _ < / _ \| __|  \___ \ / _ \ |  _| '_ \ / _ \| __|
| |__| | |_) | (_) | |_   ____) |  __/ | | | |_) | (_) | | 
|_____/|____/ \___/ \__| |_____/ \___|_|_| |_.__/ \___/ \__|
'''

intro_text_mini = ''' _____  ____        _ 
|  __ \|  _ \      | |
| |  | | |_) | ___ | |
| |  | |  _ < / _ \| __|
| |__| | |_) | (_) | |_
|_____/|____/ \___/ \__|
'''


def fore(color):
    return '\033[38;5;%dm' % color


def back(color):
    return '\033[48;5;%dm' % color


def get_color(id, mode):
    if mode == 'bg':
        return back(id)

    elif mode == 'fg':
        return fore(id)


colors = [
    93, 99, 105, 111, 117, 123, 122, 121, 120, 119, 118, 119, 120, 121, 122,
    123, 117, 111, 105, 99, 93
]


def intro(mini = False):

    if not mini:
        lines = intro_text.split('\n')
        index = 0

        for line in lines:
            print(get_color(colors[index], 'fg') + line)
            index += 1

    else:
        lines = intro_text_mini.split('\n')
        index = 0

        for line in lines:
            print(get_color(colors[index], 'fg') + line)
            index += 1