from uac_elevator import request_admin, is_admin

isadmin = is_admin()
request_admin()

from colorama import Fore
from os import _exit

if not isadmin:
    from os.path import split, sep
    folder = split(__file__)[0]

    file = open(folder + sep + 'INDICATOR_UPDATE_INSTALL.txt', 'w')
    file.close()

    _exit(0)

print(Fore.GREEN + 'DBot Updater')
print(Fore.CYAN + 'Устанавливаем обновление...')
print()

import git

from os.path import split, sep, isdir
from os import listdir, rename, remove, system, name
from shutil import rmtree

clear = lambda: system('cls') if name == 'nt' else system('clear')

folder = split(__file__)[0] + sep
folder_app = split(__file__)[0] + sep + 'DBot-Selfbot' + sep

print(Fore.GREEN + 'Скачиваем последнюю версию DBot...')

def delf(folder):
    if name == 'nt':
        system(f'del {folder} /f /q /s')
        rmtree(folder)
    
    else:
        rmtree(folder)

try:
    git.Git(folder).clone("https://github.com/Its-MatriX/DBot-Selfbot.git")
except:
    try:
        delf(folder_app)
        git.Git(folder).clone("https://github.com/Its-MatriX/DBot-Selfbot.git")
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

delf(folder_app)

if isdir(folder_app):
    print(Fore.YELLOW + 'Не удалось удалить папку ' + folder_app + ', удалите её самостоятельно.')

from intro import intro

clear()

intro()
print(Fore.GREEN + 'Обновление успешно установлено! Перезапустите DBot.')
input()
_exit(0)