def foreground_sequence(color):
        return '\033[38;5;%dm' % color

def background_sequence(color):
    return '\033[48;5;%dm' % color

def get_color(color, mode='fg'):
    if mode == 'bg':
        color = background_sequence(color)
    elif mode == 'fg':
        color = foreground_sequence(color)
    else:
        return None

    return color

colors_main = [128, 129, 135, 141, 147, 153, 159, 153, 147, 141, 135, 129]
colors_text = [57, 63, 69, 75, 81, 87, 117, 111, 105, 99, 93, 99, 105, 111, 117, 87, 81, 75, 69, 63]
colors_text_v2 = [165, 171, 177, 183, 189, 195, 194, 193, 192, 191, 190, 191, 192, 193, 194, 195, 189, 183, 177, 171]
colors_error = [196, 202, 208, 214, 220, 226, 226, 220, 214, 208, 202]

def print_line(line_length):
    resp = ''
    color_index = 0
    reverse_mode = False

    for x in range(line_length):
        if reverse_mode == False:
            color_index += 1
        else:
            color_index -= 1

        if color_index == len(colors_main):
            reverse_mode = True
            color_index = len(colors_main) - 1
        
        if color_index == -1:
            reverse_mode = False
            color_index = 0

        resp += get_color(colors_main[color_index]) + '_'

    print(resp)

def gradient_horizontal(string, colors = colors_main):
    resp = ''
    color_index = 0
    reverse_mode = False

    for letter in string:
        if reverse_mode == False:
            color_index += 1
        else:
            color_index -= 1

        if color_index == len(colors):
            reverse_mode = True
            color_index = len(colors) - 1
        
        if color_index == -1:
            reverse_mode = False
            color_index = 0

        resp += get_color(colors[color_index]) + letter

    return resp

def gradient_vertical(string, colors = colors_main):
    resp = ''
    color_index = 0
    reverse_mode = False

    string = string.split('\n')

    for line in string:
        if reverse_mode == False:
            color_index += 1
        else:
            color_index -= 1

        if color_index == len(colors):
            reverse_mode = True
            color_index = len(colors) - 1
        
        if color_index == -1:
            reverse_mode = False
            color_index = 0

        resp += get_color(colors[color_index]) + line + '\n'

    return resp