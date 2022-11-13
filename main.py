# default status note:
# use null for dont use default status

from os import system
from os.path import sep, split

folder = split(__file__)[0]

try:
    from json import load
    from os import _exit, get_terminal_size, listdir, name

    from discord import Activity, ActivityType, Game, Status, Streaming
except Exception:
    from Functions.requirements_installer import \
        install_modules_from_requirements
    install_modules_from_requirements()

if name == 'nt':
    system('title DBot: Запускается')


def clear():
    if name == 'nt':
        system('cls')

    else:
        system('clear')


clear()

try:
    from threading import Thread
    from time import sleep as non_async_sleep

    from colorama import Fore
    from discord.ext import commands

    from Functions.intro import intro
    from Functions.logger import log, log_error, recovery_logs
except Exception:
    from Functions.requirements_installer import \
        install_modules_from_requirements
    install_modules_from_requirements()

from theme import LOGIN_INFO_KEY_COLOR

login_info_key_color = Fore.GREEN if LOGIN_INFO_KEY_COLOR == 1 else (
    Fore.BLUE if LOGIN_INFO_KEY_COLOR == 2 else
    (Fore.CYAN if LOGIN_INFO_KEY_COLOR == 3 else
     (Fore.MAGENTA if LOGIN_INFO_KEY_COLOR == 4 else
      (Fore.YELLOW if LOGIN_INFO_KEY_COLOR == 5 else
       (Fore.WHITE if LOGIN_INFO_KEY_COLOR == 0 else None)))))

if not login_info_key_color:
    log_error('Неверное значение для LOGIN_INFO_KEY_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 5.')

    try:
        input()

    except:
        pass

    _exit(1)

from theme import LOGIN_INFO_VAL_COLOR

login_info_val_color = Fore.CYAN if LOGIN_INFO_VAL_COLOR == 1 else (
    Fore.BLUE if LOGIN_INFO_VAL_COLOR == 2 else
    (Fore.GREEN if LOGIN_INFO_VAL_COLOR == 3 else
     (Fore.MAGENTA if LOGIN_INFO_VAL_COLOR == 4 else
      (Fore.YELLOW if LOGIN_INFO_VAL_COLOR == 5 else
       (Fore.WHITE if LOGIN_INFO_VAL_COLOR == 0 else None)))))

if not login_info_val_color:
    log_error('Неверное значение для LOGIN_INFO_VAL_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 1 до 5.')

    try:
        input()

    except:
        pass

    _exit(1)

from theme import SEP_LINE_COLOR

sep_line_color = Fore.CYAN if SEP_LINE_COLOR == 1 else (
    Fore.BLUE if SEP_LINE_COLOR == 2 else
    (Fore.GREEN if SEP_LINE_COLOR == 3 else
     (Fore.MAGENTA if SEP_LINE_COLOR == 4 else
      (Fore.YELLOW if SEP_LINE_COLOR == 5 else
       (Fore.WHITE if SEP_LINE_COLOR == 0 else None)))))

if not sep_line_color:
    log_error('Неверное значение для SEP_LINE_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 5.')

    try:
        input()

    except:
        pass

    _exit(1)

from theme import ALWAYS_MINI_INTRO

loaded_extensions = 0

intro(ALWAYS_MINI_INTRO)

try:
    config = eval(open(folder + sep + 'config.py', 'r').read())

except FileNotFoundError:
    path_config = folder + sep + 'config.py'

    print(Fore.RED + 'Не удалось найти файл с конфигурацией. ' +
          f'Расположение файла должно быть: {path_config}')

    print('Создайте config.py по указанному пути!\n')
    print('Пример config.py:')
    print()
    print(Fore.CYAN + '{')
    print('    "TOKEN": "токен",')
    print('    "LOG_WEBHOOK": "вебхук",')
    print('    "LOG_DELETES": False,')
    print('    "LOG_EDITS": False,')
    print('    "ENABLE_CRASH": False,')
    print('    "DEFAULT_STATUS": "game idle DBot",')
    print('    "SNIPE_NITRO": True')
    print('}')

    print()

    input(Fore.GREEN + 'Нажмите [Enter] для выхода > ')
    exit(0)

except Exception as e:
    print(Fore.RED + f'Ошибка чтения файла config.py')
    print(f'Ошибка: {e}')

    print()

    input(Fore.GREEN + 'Нажмите [Enter] для выхода > ')
    exit(0)

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')

bot.config = config


def start_screen(use_mini_intro=False):
    intro(use_mini_intro)

    print(login_info_key_color + 'Логин: ' + login_info_val_color +
          str(bot.user))
    print(login_info_key_color + 'ID: ' + login_info_val_color +
          str(bot.user.id))
    print(login_info_key_color + 'Префикс: ' + login_info_val_color +
          config['COMMAND_PREFIX'])
    print()

    print(login_info_key_color + 'Загружено расширений: ' +
          login_info_val_color + str(loaded_extensions) + ' (команд: ' +
          str(len(bot.all_commands)) + ')')


def terminal_resize_listener():
    terminal_cols_old = 0

    while True:
        terminal_cols = get_terminal_size().columns

        if terminal_cols != terminal_cols_old:
            terminal_cols_old = get_terminal_size().columns

            use_mini_intro = terminal_cols_old < 70

            clear()
            start_screen(use_mini_intro if not ALWAYS_MINI_INTRO else True)

            print()
            print(sep_line_color + '—' * terminal_cols)
            recovery_logs()

        non_async_sleep(.2)


@bot.event
async def on_connect():
    if name == 'nt':
        system(f'title DBot: {bot.user}')

    global loaded_extensions

    extensions = listdir(folder + sep + 'Commands/')
    loaded_extensions = 0

    try:
        for file in extensions:
            if file.split('.')[-1] == 'py' and file.startswith('commands_'):
                file = '.'.join(file.split('.')[:-1:1])
                bot.load_extension(f'Commands.{file}')
                loaded_extensions += 1

    except ModuleNotFoundError:
        print(Fore.RED + 'Ошибка загрузки расширений!')
        print(Fore.RED + 'Не установлены все необходимые модули. ' +
              'Нажмите [Enter] для начала установки')

        input()

        print(Fore.GREEN)

        from Functions.requirements_installer import \
            install_modules_from_requirements
        install_modules_from_requirements(False)

        input(Fore.GREEN + 'Модули успешно установлены. Перезапустите DBot.')

        _exit(0)

    except Exception as e:
        print(Fore.RED + f'Ошибка инициализации расширения Commands.{file}. ' +
              'Попробуйте переустановить DBot.' + f'\nОшибка: {e}')
        _exit(1)

    print()

    Thread(target=terminal_resize_listener).start()

    status = config['DEFAULT_STATUS']

    if status:
        if status == 'delete':
            await bot.change_presence(status=Status.online, activity=None)

        if status == 'online':
            await bot.change_presence(status=Status.online)
            return

        elif status == 'idle':
            await bot.change_presence(status=Status.idle)
            return

        elif status == 'dnd':
            await bot.change_presence(status=Status.dnd)
            return

        elif status == 'invisible':
            await bot.change_presence(status=Status.invisible)
            return

        if ' ' not in status:
            return

        status = status.split(' ')

        if status[0] == 'streaming':
            if 'https://' not in status[1] and 'http://' not in status[1]:
                status[1] = 'https://' + status[1]

            if 'youtube.com/watch?v=' not in status[
                    1] and 'twitch.tv/' not in status[1]:
                status[1] = 'https://youtube.com/watch?v=' + \
                    status[1].replace('https://', '').replace('http://', '')

            twitch_url = status[1]

            stream_name = ' '.join(status[2:])

            await bot.change_presence(
                activity=Streaming(name=stream_name, url=twitch_url))

            return

        elif status[0] == 'game':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await bot.change_presence(activity=Game(name=' '.join(status[2:])),
                                      status=status_icon)

        elif status[0] == 'watch':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await bot.change_presence(activity=Activity(
                type=ActivityType.watching, name=' '.join(status[2:])),
                                      status=status_icon)

        elif status[0] == 'listening':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await bot.change_presence(activity=Activity(
                type=ActivityType.listening, name=' '.join(status[2:])),
                                      status=status_icon)

        elif status[0] == 'competing':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await bot.change_presence(activity=Activity(
                type=ActivityType.competing, name=' '.join(status[2:])),
                                      status=status_icon)


@bot.event
async def on_command_error(ctx, error):
    lines = str(error).split('\n') if '\n' in str(error) else [str(error)]
    log_error('; '.join(lines), 'ОШИБКА', 1)


@bot.event
async def on_command(ctx):
    log(ctx.invoked_with, 'КОМАНДА', 0)


try:
    bot.run(config['TOKEN'])

except Exception as e:
    if name == 'nt':
        system('title DBot: Ошибка логина')
    log_error(e, 'ОШИБКА', 1)

    try:
        input()
    except Exception:
        pass
