IS_COMPILED_TO_EXECUTABLE = False

from json import load
from os import get_terminal_size, listdir, name, system
from os.path import sep, split
from sys import executable

if IS_COMPILED_TO_EXECUTABLE:
    folder = split(executable)[0]
else:
    folder = split(__file__)[0]

if name == 'nt':
    system('title DBot: Запускается')

clear = lambda: system('cls') if name == 'nt' else system('clear')

clear()

from threading import Thread
from time import sleep as non_async_sleep

from colorama import Fore
from discord.ext import commands

from Commands.logger import log, recovery_logs
from intro import intro

loaded_extensions = 0

intro()

try:
    config = load(open(folder + sep + 'config.json', 'r'))
except FileNotFoundError:
    path_config = folder + sep + 'config.json'
    print(
        Fore.RED +
        f'Не удалось найти файл с конфигурацией. Расположение файла должно быть: {path_config}'
    )
    print('Создайте config.json по указанному пути!\n')
    print('Пример config.json:')
    print()
    print(Fore.CYAN + '{')
    print('    "TOKEN": "токен",')
    print('    "LOG_WEBHOOK": "вебхук",')
    print('    "LOG_DELETES": false,')
    print('    "LOG_EDITS": false,')
    print('    "ENABLE_CRASH": false')
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
    print(Fore.GREEN + 'Логин: ' + Fore.CYAN + str(bot.user))
    print(Fore.GREEN + 'ID: ' + Fore.CYAN + str(bot.user.id))
    print(Fore.GREEN + 'Префикс: ' + Fore.CYAN + config['COMMAND_PREFIX'])
    print()
    print(Fore.GREEN + 'Загружено расширений: ' + Fore.CYAN +
          str(loaded_extensions))


def terminal_resize_listener():
    global logged

    terminal_cols_old = 0

    while True:
        terminal_cols = get_terminal_size().columns

        if terminal_cols != terminal_cols_old:
            terminal_cols_old = get_terminal_size().columns
            clear()

            start_screen()

            print('_' * terminal_cols)

            recovery_logs()

        non_async_sleep(.2)


@bot.event
async def on_connect():

    if name == 'nt':
        system(f'title DBot: {bot.user}')

    global loaded_extensions

    extensions = listdir(folder + sep + 'Commands/')
    loaded_extensions = 0

    for file in extensions:
        if file.split('.')[-1] == 'py' and file.startswith('commands_'):
            file = '.'.join(file.split('.')[:-1:1])
            bot.load_extension(f'Commands.{file}')
            loaded_extensions += 1

    print()

    Thread(target=terminal_resize_listener).start()


@bot.event
async def on_command_error(ctx, error):
    lines = str(error).split('\n') if '\n' in str(error) else [str(error)]
    log('; '.join(lines), 'ОШИБКА', Fore.RED, 1)


@bot.event
async def on_command(ctx):
    log(ctx.invoked_with, 'КОМАНДА', Fore.YELLOW, 0)


try:
    bot.run(config['TOKEN'])
except Exception as e:
    if name == 'nt':
        system('title DBot: Ошибка')
    log(e, 'ОШИБКА', Fore.RED, 1)
    input()
