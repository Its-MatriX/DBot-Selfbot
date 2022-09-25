from os.path import sep, split
from os import system
from sys import executable

def install_modules_from_requirements(ask=True):
    folder = split(__file__)[0]

    required = open(folder + sep + 'requirements.txt', 'r').read().split('\n')

    from subprocess import run

    installed = run([executable, '-m', 'pip', 'freeze'],
                    capture_output=True,
                    text=True).stdout

    installed = installed.split('\n')
    installed_ = []

    for module in installed:
        installed_.append(module.split('==')[0].lower())

    installed = installed_
    install_modules = False

    for req in required:
        if req.lower() not in installed:
            if ask:
                print('У вас не установлены все необходимые модули!')
                input('Нажмите [Enter] для начала установки\n> ')
            install_modules = True
            break

    if install_modules:
        for req in required:
            system(f'{executable} -m pip install {req}')