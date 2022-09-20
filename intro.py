from colorama import Fore
from Commands.colors import colors_text_v2, gradient_vertical


intro_text = '''┏━━━┳┓    ┏┓
┗┓┏┓┃┃   ┏┛┗┓
 ┃┃┃┃┗━┳━┻┓┏┛
 ┃┃┃┃┏┓┃┏┓┃┃
┏┛┗┛┃┗┛┃┗┛┃┗┓
┗━━━┻━━┻━━┻━┛
'''

def intro():
    print(gradient_vertical(intro_text, colors_text_v2))