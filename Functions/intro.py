from time import sleep

intro_text = '''▓█████▄  ▄▄▄▄    ▒█████  ▄▄▄█████▓
▒██▀ ██▌▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
░██   █▌▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
░▓█▄   ▌▒██░█▀  ▒██   ██░░ ▓██▓ ░
░▒████▓ ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░
 ▒▒▓  ▒ ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░
 ░ ▒  ▒ ▒░▒   ░   ░ ▒ ▒░     ░
 ░ ░  ░  ░    ░ ░ ░ ░ ▒    ░
   ░     ░          ░ ░
 ░            ░
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


def intro(resize_window = False):
    lines = intro_text.split('\n')
    index = 0

    for line in lines:
        print(get_color(colors[index], 'fg') + line)
        index += 1

        if not resize_window:
            sleep(.02*index)