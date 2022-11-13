# Note: "theme.py"
# Цвет заголовка (HEADER_COLOR)
# 1 - Стандартный (градиент)
# 2 - Синий
# 3 - Голубой
# 4 - Зелёный
# 5 - Фиолетовый
# 6 - Жёлтый

# Стиль заголовка (HEADER_STYLE)
# 1 - Стандартный
# 2 - Bloody
# 3 - Colossal
# 4 - DOS Rebel

from theme import LOGO_COLOR, LOGO_STYLE
from colorama import Fore
from Functions.logger import log_error
from os import _exit

IntroText_Default = ''' _____  ____        _      _____      _  __ _           _   
|  __ \|  _ \      | |    / ____|    | |/ _| |         | |
| |  | | |_) | ___ | |_  | (___   ___| | |_| |__   ___ | | 
| |  | |  _ < / _ \| __|  \___ \ / _ \ |  _| '_ \ / _ \| __|
| |__| | |_) | (_) | |_   ____) |  __/ | | | |_) | (_) | | 
|_____/|____/ \___/ \__| |_____/ \___|_|_| |_.__/ \___/ \__|
'''

IntroText_Default_Mini = ''' _____  ____        _ 
|  __ \|  _ \      | |
| |  | | |_) | ___ | |
| |  | |  _ < / _ \| __|
| |__| | |_) | (_) | |_
|_____/|____/ \___/ \__|
'''

IntroText_Bloody = '''▓█████▄  ▄▄▄▄    ▒█████  ▄▄▄█████▓     ██████ ▓█████  ██▓      █████▒▄▄▄▄    ▒█████  ▄▄▄█████▓
▒██▀ ██▌▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒   ▒██    ▒ ▓█   ▀ ▓██▒    ▓██   ▒▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
░██   █▌▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░   ░ ▓██▄   ▒███   ▒██░    ▒████ ░▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
░▓█▄   ▌▒██░█▀  ▒██   ██░░ ▓██▓ ░      ▒   ██▒▒▓█  ▄ ▒██░    ░▓█▒  ░▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
░▒████▓ ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░    ▒██████▒▒░▒████▒░██████▒░▒█░   ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
 ▒▒▓  ▒ ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░      ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒░▓  ░ ▒ ░   ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
 ░ ▒  ▒ ▒░▒   ░   ░ ▒ ▒░     ░       ░ ░▒  ░ ░ ░ ░  ░░ ░ ▒  ░ ░     ▒░▒   ░   ░ ▒ ▒░     ░    
 ░ ░  ░  ░    ░ ░ ░ ░ ▒    ░         ░  ░  ░     ░     ░ ░    ░ ░    ░    ░ ░ ░ ░ ▒    ░      
   ░     ░          ░ ░                    ░     ░  ░    ░  ░        ░          ░ ░           
 ░            ░                                                           ░                   
 '''

IntroText_Bloody_Mini = '''▓█████▄  ▄▄▄▄    ▒█████  ▄▄▄█████▓
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

IntroText_Colossal = '''8888888b.  888888b.            888          .d8888b.           888  .d888 888               888    
888  "Y88b 888  "88b           888         d88P  Y88b          888 d88P"  888               888    
888    888 888  .88P           888         Y88b.               888 888    888               888    
888    888 8888888K.   .d88b.  888888       "Y888b.    .d88b.  888 888888 88888b.   .d88b.  888888 
888    888 888  "Y88b d88""88b 888             "Y88b. d8P  Y8b 888 888    888 "88b d88""88b 888    
888    888 888    888 888  888 888               "888 88888888 888 888    888  888 888  888 888    
888  .d88P 888   d88P Y88..88P Y88b.       Y88b  d88P Y8b.     888 888    888 d88P Y88..88P Y88b.  
8888888P"  8888888P"   "Y88P"   "Y888       "Y8888P"   "Y8888  888 888    88888P"   "Y88P"   "Y888 
'''

IntroText_Colossal_Mini = '''8888888b.  888888b.            888
888  "Y88b 888  "88b           888
888    888 888  .88P           888
888    888 8888888K.   .d88b.  888888
888    888 888  "Y88b d88""88b 888
888    888 888    888 888  888 888
888  .d88P 888   d88P Y88..88P Y88b.
8888888P"  8888888P"   "Y88P"   "Y888
'''

IntroText_DOSRebel = ''' ██████████   ███████████            █████        █████████           ████     ██████  █████               █████   
░░███░░░░███ ░░███░░░░░███          ░░███        ███░░░░░███         ░░███    ███░░███░░███               ░░███    
 ░███   ░░███ ░███    ░███  ██████  ███████     ░███    ░░░   ██████  ░███   ░███ ░░░  ░███████   ██████  ███████  
 ░███    ░███ ░██████████  ███░░███░░░███░      ░░█████████  ███░░███ ░███  ███████    ░███░░███ ███░░███░░░███░   
 ░███    ░███ ░███░░░░░███░███ ░███  ░███        ░░░░░░░░███░███████  ░███ ░░░███░     ░███ ░███░███ ░███  ░███    
 ░███    ███  ░███    ░███░███ ░███  ░███ ███    ███    ░███░███░░░   ░███   ░███      ░███ ░███░███ ░███  ░███ ███
 ██████████   ███████████ ░░██████   ░░█████    ░░█████████ ░░██████  █████  █████     ████████ ░░██████   ░░█████ 
░░░░░░░░░░   ░░░░░░░░░░░   ░░░░░░     ░░░░░      ░░░░░░░░░   ░░░░░░  ░░░░░  ░░░░░     ░░░░░░░░   ░░░░░░     ░░░░░  
'''

IntroText_DOSRebel_Mini = ''' ██████████   ███████████            █████
░░███░░░░███ ░░███░░░░░███          ░░███
 ░███   ░░███ ░███    ░███  ██████  ███████
 ░███    ░███ ░██████████  ███░░███░░░███░
 ░███    ░███ ░███░░░░░███░███ ░███  ░███
 ░███    ███  ░███    ░███░███ ░███  ░███ ███
 ██████████   ███████████ ░░██████   ░░█████
░░░░░░░░░░   ░░░░░░░░░░░   ░░░░░░     ░░░░░
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


def intro(mini=False):
    if not mini:
        if LOGO_STYLE == 1:
            lines = IntroText_Default.split('\n')

        elif LOGO_STYLE == 2:
            lines = IntroText_Bloody.split('\n')

        elif LOGO_STYLE == 3:
            lines = IntroText_Colossal.split('\n')

        elif LOGO_STYLE == 4:
            lines = IntroText_DOSRebel.split('\n')

        else:
            log_error('Неверное значение для HEADER_STYLE в "theme.py", ' + \
                              'значение должно быть в диапазоне от 1 до 4.')

            try:
                input()

            except:
                pass

            _exit(1)

        index = 0

        for line in lines:
            if LOGO_COLOR == 1:
                print(get_color(colors[index], 'fg') + line)

            else:
                if LOGO_COLOR == 2:
                    print(Fore.BLUE + line)

                elif LOGO_COLOR == 3:
                    print(Fore.CYAN + line)

                elif LOGO_COLOR == 4:
                    print(Fore.GREEN + line)

                elif LOGO_COLOR == 5:
                    print(Fore.MAGENTA + line)

                elif LOGO_COLOR == 6:
                    print(Fore.YELLOW + line)

                elif LOGO_COLOR == 0:
                    print(Fore.WHITE + line)

                else:
                    log_error('Неверное значение для HEADER_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 6.')

                    try:
                        input()

                    except:
                        pass

                    _exit(1)

            index += 1

    else:
        if LOGO_STYLE == 1:
            lines = IntroText_Default_Mini.split('\n')

        elif LOGO_STYLE == 2:
            lines = IntroText_Bloody_Mini.split('\n')

        elif LOGO_STYLE == 3:
            lines = IntroText_Colossal_Mini.split('\n')

        elif LOGO_STYLE == 4:
            lines = IntroText_DOSRebel_Mini.split('\n')

        else:
            log_error('Неверное значение для HEADER_STYLE в "theme.py", ' + \
                              'значение должно быть в диапазоне от 1 до 4.')

            try:
                input()

            except:
                pass

            _exit(1)

        index = 0

        for line in lines:
            if LOGO_COLOR == 1:
                print(get_color(colors[index], 'fg') + line)

            else:
                if LOGO_COLOR == 2:
                    print(Fore.BLUE + line)

                elif LOGO_COLOR == 3:
                    print(Fore.CYAN + line)

                elif LOGO_COLOR == 4:
                    print(Fore.GREEN + line)

                elif LOGO_COLOR == 5:
                    print(Fore.MAGENTA + line)

                elif LOGO_COLOR == 6:
                    print(Fore.YELLOW + line)

                elif LOGO_COLOR == 0:
                    print(Fore.WHITE + line)

                else:
                    log_error('Неверное значение для HEADER_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 6.')

                    try:
                        input()

                    except:
                        pass

                    _exit(1)

            index += 1