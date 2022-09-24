from datetime import datetime

from Commands.colors import (colors_error, colors_text, colors_text_v2,
                             gradient_horizontal)


class logwriter:
    written = ''


def log(content, message_type='ИНФО', spaces=3):
    time_now = datetime.now().strftime('%H:%M:%S')
    to_write = f'{gradient_horizontal(time_now, colors_text)} {gradient_horizontal("[" + message_type + "]", colors_text_v2)}{" " * spaces} : {gradient_horizontal(content, colors_text)}'

    print(to_write)

    logwriter.written += '\n' + to_write

    if logwriter.written.count('\n') > 60:
        logwriter.written = logwriter.written.split('\n')
        logwriter.written = '\n'.join(logwriter.written[:50])


def log_error(content, message_type='ОШИБКА', spaces=1):
    time_now = datetime.now().strftime('%H:%M:%S')
    to_write = f'{gradient_horizontal(time_now, colors_text)} {gradient_horizontal("[" + message_type + "]", colors_error)}{" " * spaces} : {gradient_horizontal(content, colors_text)}'

    print(to_write)

    logwriter.written += '\n' + to_write

    if logwriter.written.count('\n') > 60:
        logwriter.written = logwriter.written.split('\n')
        logwriter.written = '\n'.join(logwriter.written[:50])


def recovery_logs():
    print(logwriter.written)
