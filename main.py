from json import load
from os import listdir

from colorama import Fore
from discord.ext import commands

from logger import log

from intro import intro

intro()

config = load(open('config.json', 'r'))

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')

# bot.show_logs = config['SEND_CONSOLE_LOGS']
bot.config = config


@bot.event
async def on_connect():
    print(Fore.GREEN + 'Логин: ' + Fore.CYAN + str(bot.user))
    print(Fore.GREEN + 'ID: ' + Fore.CYAN + str(bot.user.id))
    print(Fore.GREEN + 'Префикс: ' + Fore.CYAN + config['COMMAND_PREFIX'])

    print()

    extensions = listdir('Commands/')
    loaded_extensions = 0

    for file in extensions:
        if file.split('.')[-1] == 'py' and file.startswith('commands_'):
            file = '.'.join(file.split('.')[:-1:1])
            bot.load_extension(f'Commands.{file}')
            loaded_extensions += 1

    print(Fore.GREEN + 'Загружено расширений: ' + Fore.CYAN +
          str(loaded_extensions))

    print()


@bot.event
async def on_command_error(ctx, error):
    lines = str(error).split('\n') if '\n' in str(error) else [str(error)]
    log('; '.join(lines), 'ОШИБКА ', Fore.RED)


@bot.event
async def on_command(ctx):
    log(ctx.invoked_with, 'КОМАНДА')


try:
    bot.run(config['TOKEN'])
except Exception as e:
    log(e, 'ОШИБКА', Fore.RED)
