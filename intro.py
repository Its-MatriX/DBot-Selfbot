from colorama import Fore

intro_text = '''┏━━━┳┓    ┏┓
┗┓┏┓┃┃   ┏┛┗┓
 ┃┃┃┃┗━┳━┻┓┏┛
 ┃┃┃┃┏┓┃┏┓┃┃
┏┛┗┛┃┗┛┃┗┛┃┗┓
┗━━━┻━━┻━━┻━┛
'''

def intro():
    print(Fore.GREEN + intro_text)