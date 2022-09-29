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

    from Functions.colors import (colors_error, colors_text, colors_text_v2,
                                  gradient_horizontal, print_line)
    from Functions.intro import intro
    from Functions.logger import log, log_error, recovery_logs
except Exception:
    from Functions.requirements_installer import \
        install_modules_from_requirements
    install_modules_from_requirements()

loaded_extensions = 0

intro()

try:
    config = load(open(folder + sep + 'config.json', 'r'))
except FileNotFoundError:
    path_config = folder + sep + 'config.json'

    print(Fore.RED + f'Не удалось найти файл с конфигурацией. ' +
          'Расположение файла должно быть: {path_config}')

    print('Создайте config.json по указанному пути!\n')
    print('Пример config.json:')
    print()
    print(Fore.CYAN + '{')
    print('    "TOKEN": "токен",')
    print('    "LOG_WEBHOOK": "вебхук",')
    print('    "LOG_DELETES": false,')
    print('    "LOG_EDITS": false,')
    print('    "ENABLE_CRASH": false,')
    print('    "DEFAULT_STATUS": "game idle DBot"')
    print('}')

    print()

    input(Fore.GREEN + 'Нажмите [Enter] для выхода > ')
    exit(0)
except Exception as e:
    print(Fore.RED + f'Ошибка чтения файла config.json')
    print(f'Ошибка: {e}')

    print()

    input(Fore.GREEN + 'Нажмите [Enter] для выхода > ')
    exit(0)

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')

bot.config = config

def start_screen():
    intro()

    print(Fore.GREEN + gradient_horizontal('Логин: ', colors_text_v2) +
          gradient_horizontal(str(bot.user), colors_text))

    print(Fore.GREEN + gradient_horizontal('ID: ', colors_text_v2) +
          Fore.CYAN + gradient_horizontal(str(bot.user.id), colors_text))

    print(Fore.GREEN + gradient_horizontal('Префикс: ', colors_text_v2) +
          Fore.CYAN +
          gradient_horizontal(config['COMMAND_PREFIX'], colors_text))

    print()

    print(Fore.GREEN +
          gradient_horizontal('Загружено расшрений: ', colors_text_v2) +
          Fore.CYAN + gradient_horizontal(str(loaded_extensions), colors_text))


def terminal_resize_listener():
    terminal_cols_old = 0

    while True:
        terminal_cols = get_terminal_size().columns

        if terminal_cols != terminal_cols_old:
            terminal_cols_old = get_terminal_size().columns
            clear()
            start_screen()

            print()
            print_line(terminal_cols)
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
    except Exception as e:
        if 'no module named' in str(e).lower():
            print(
                gradient_horizontal('Ошибка инициализации расширений!',
                                    colors_error))
            print(
                gradient_horizontal('Не установлены все необходимые модули. ' +
                                    'Нажмите [Enter] для начала установки.'))

            input()

            print(Fore.GREEN)

            from Functions.requirements_installer import \
                install_modules_from_requirements
            install_modules_from_requirements(False)

            input(
                gradient_horizontal(
                    'Модули успешно установлены. Перезапустите DBot.'))

            _exit(0)
        else:
            print(Fore.RED +
                  f'Ошибка инициализации расширения Commands.{file}. ' +
                  'Попробуйте переустановить DBot.')
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
    print(gradient_horizontal('Входим в учётную запись...'))
    bot.run(config['TOKEN'])

except Exception as e:
    if name == 'nt':
        system('title DBot: Ошибка логина')
    log_error(e, 'ОШИБКА', 1)

    try:
        input()
    except Exception:
        pass
