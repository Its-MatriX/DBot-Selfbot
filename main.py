from discord.ext import commands
from json import load
from os import listdir
from colorama import Fore
from Functions.intro import intro

intro()


config = load(open('config.json', 'r'))

bot = commands.Bot(config['COMMAND_PREFIX'], self_bot=True)
bot.remove_command('help')

bot.show_logs = config['SEND_CONSOLE_LOGS']
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
    if bot.show_logs:
        lines = str(error).split('\n') if '\n' in str(error) else [str(error)]

        print(Fore.GREEN + 'Произошла ошибка: ' + Fore.CYAN + lines[0])

        try:
            for line in lines[1:]:
                print(Fore.CYAN + ' ' * 18 + line)
        except:
            pass

try:
    bot.run(config['TOKEN'])
except Exception as e:
    print(Fore.RED + 'Критическая ошибка: ' + Fore.CYAN +
          f'Не удалось залогиниться ({e})' + Fore.RESET)
