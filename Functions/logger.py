from datetime import datetime
from colorama import Fore


def log_error(content, message_type='ОШИБКА', spaces=1, show_type=True):
    if show_type:
        time_now = datetime.now().strftime('%H:%M:%S')
        to_write = f'{Fore.RED}{time_now} [{message_type}]{" " * spaces}: {content}'
    else:
        to_write = Fore.RED + content

    print(to_write)

    logwriter.written += '\n' + to_write

    if logwriter.written.count('\n') > 60:
        logwriter.written = logwriter.written.split('\n')
        logwriter.written = '\n'.join(logwriter.written[:50])


from os import _exit

from theme import LOGS_TIME_AND_CONTENT_COLOR

logs_time_and_content_color = Fore.GREEN if LOGS_TIME_AND_CONTENT_COLOR == 1 else (
    Fore.BLUE if LOGS_TIME_AND_CONTENT_COLOR == 2 else
    (Fore.CYAN if LOGS_TIME_AND_CONTENT_COLOR == 3 else
     (Fore.MAGENTA if LOGS_TIME_AND_CONTENT_COLOR == 4 else
      (Fore.YELLOW if LOGS_TIME_AND_CONTENT_COLOR == 5 else
       (Fore.WHITE if LOGS_TIME_AND_CONTENT_COLOR == 0 else None)))))

if not logs_time_and_content_color:
    log_error('Неверное значение для LOGS_TIME_AND_CONTENT_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 5.')

    try:
        input()

    except:
        pass

    _exit(1)

from theme import LOGS_TYPE_COLOR

logs_type_color = Fore.CYAN if LOGS_TYPE_COLOR == 1 else (
    Fore.BLUE if LOGS_TYPE_COLOR == 2 else
    (Fore.GREEN if LOGS_TYPE_COLOR == 3 else
     (Fore.MAGENTA if LOGS_TYPE_COLOR == 4 else
      (Fore.YELLOW if LOGS_TYPE_COLOR == 5 else
       (Fore.WHITE if LOGS_TYPE_COLOR == 0 else None)))))

if not logs_type_color:
    log_error('Неверное значение для LOGS_TYPE_COLOR в "theme.py", ' + \
                              'значение должно быть в диапазоне от 0 до 5.')

    try:
        input()

    except:
        pass

    _exit(1)


class logwriter:
    written = ''


def log(content, message_type='ИНФО', spaces=3, show_type=True):
    if show_type:
        time_now = datetime.now().strftime('%H:%M:%S')
        to_write = f'{logs_time_and_content_color}{time_now} {logs_type_color}[{message_type}]{" " * spaces}{logs_time_and_content_color}: {content}'
    else:
        to_write = Fore.GREEN + content

    print(to_write)

    logwriter.written += '\n' + to_write

    if logwriter.written.count('\n') > 60:
        logwriter.written = logwriter.written.split('\n')
        logwriter.written = '\n'.join(logwriter.written[:50])


def recovery_logs():
    print(logwriter.written)
