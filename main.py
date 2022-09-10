from json import load
from os import listdir
from colorama import Fore
from Functions.LogotypeIntro import intro

intro()

from discord.ext import commands

config = load(open('config.json', 'r'))

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')


@bot.event
async def on_connect():
    print(Fore.GREEN + 'Логин: ' + Fore.CYAN + str(bot.user))
    print(Fore.GREEN + 'ID: ' + Fore.CYAN + str(bot.user.id))
    print(Fore.GREEN + 'Префикс: ' + Fore.CYAN +
          config['COMMAND_PREFIX'])

    print()

    extensions = listdir('Commands/')
    loaded_extensions = 0

    for file in extensions:
        if file.split('.')[-1] == 'py':
            file = '.'.join(file.split('.')[:-1:1])
            bot.load_extension(f'Commands.{file}')
            loaded_extensions += 1

    print(Fore.GREEN + 'Загружено расширений: ' + Fore.CYAN +
          str(loaded_extensions))


bot.run(config['TOKEN'])