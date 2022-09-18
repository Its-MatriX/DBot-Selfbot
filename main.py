from json import load
from os import get_terminal_size, listdir, name, system

clear = lambda: system('cls') if name == 'nt' else system('clear')

from threading import Thread
from time import sleep as non_async_sleep

from colorama import Fore
from discord.ext import commands

from intro import intro
from Commands.logger import log

loaded_extensions = 0

intro()

config = load(open('config.json', 'r'))

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')

# bot.show_logs = config['SEND_CONSOLE_LOGS']
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
    terminal_cols_old = 0

    while True:
        terminal_cols = get_terminal_size().columns

        if terminal_cols != terminal_cols_old:
            terminal_cols_old = get_terminal_size().columns
            clear()

            start_screen()

            print('_' * terminal_cols)
            print()

        non_async_sleep(.2)


@bot.event
async def on_connect():

    global loaded_extensions

    extensions = listdir('Commands/')
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
    log(e, 'ОШИБКА', Fore.RED)
