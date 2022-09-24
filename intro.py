from Commands.colors import colors_text_v2, gradient_vertical

# Some remake logo and
# fix display on Pydroid 3 (for android)

intro_text = '''╔═══╦╗⠀⠀⠀⠀╔╗⠀⠀
╚╗╔╗║║⠀⠀⠀╔╝╚╗⠀⠀
⠀║║║║╚═╦═╩╗╔╝⠀⠀
⠀║║║║╔╗║╔╗║║⠀⠀
╔╝╚╝║╚╝║╚╝║╚╗⠀⠀
╚═══╩══╩══╩═╝⠀⠀
'''


def intro():
    print(gradient_vertical(intro_text, colors_text_v2))
