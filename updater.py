from colorama import Fore
from os import _exit

print(Fore.GREEN + 'DBot Updater')
print(Fore.CYAN + 'Устанавливаем обновление...')
print()

import git

from os.path import split, sep, isdir
from os import listdir, rename, remove
from shutil import rmtree

folder = split(__file__)[0] + sep
folder_app = split(__file__)[0] + sep + 'DBot-Selfbot' + sep

print(Fore.GREEN + 'Скачиваем последнюю версию DBot...')

try:
    git.Git(folder).clone("https://github.com/Its-MatriX/DBot-Selfbot.git")
except:
    try:
        rmtree(folder_app)
        git.Git(folder).clone("https://github.com/Its-MatriX/DBot-Selfbot.git")
    except:
        try:
            rmtree(folder_app)
            git.Git(folder).clone(
                "https://github.com/Its-MatriX/DBot-Selfbot.git")
        except Exception as e:
            try:
                input(Fore.RED +
                      f'Не удалось установить обновление! Ошибка: {e}\n> ')
            except:
                print(Fore.RED +
                      f'Не удалось установить обновление! Ошибка: {e}\n')
            _exit(1)

for file in listdir(folder_app + 'Commands'):
    if file not in 'auto_response.json':
        print(Fore.GREEN + 'Перемещаем',
            Fore.YELLOW + folder_app + 'Commands' + sep + file, Fore.GREEN + 'в',
            Fore.YELLOW + folder + 'Commands' + sep + file)
        try:
            remove(folder + 'Commands' + sep + file)
        except:
            pass

        rename(folder_app + 'Commands' + sep + file,
            folder + 'Commands' + sep + file)

for file in listdir(folder_app):
    if not isdir(folder_app + file):
        if file not in ('config.json', 'updater.py'):
            print(Fore.GREEN + 'Перемещаем', Fore.YELLOW + folder_app + file,
                  Fore.GREEN + 'в', Fore.YELLOW + folder + sep + file)
            try:
                remove(folder + sep + file)
            except:
                pass

            rename(folder_app + file, folder + sep + file)

print(Fore.GREEN + 'Удаляем папку', Fore.YELLOW + folder_app)

try:
    rmtree(folder_app)
except:
    print(
        Fore.GREEN + 'Не удалось удалить папку', Fore.YELLOW + folder_app +
        Fore.GREEN + '.' + ' Удалите её самостоятельно.')

print()
print(Fore.GREEN + 'Обновление успешно установлено! Перезапустите DBot.')
input()
_exit(0)