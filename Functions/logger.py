from datetime import datetime
from colorama import Fore


class logwriter:
    written = ''


def log(content, message_type='ИНФО', spaces=3, show_type=True):
    if show_type:
        time_now = datetime.now().strftime('%H:%M:%S')
        to_write = f'{Fore.GREEN}{time_now} {Fore.CYAN}[{message_type}]{" " * spaces}{Fore.GREEN}: {Fore.GREEN}{content}'
    else:
        to_write = Fore.GREEN + content

    print(to_write)

    logwriter.written += '\n' + to_write

    if logwriter.written.count('\n') > 60:
        logwriter.written = logwriter.written.split('\n')
        logwriter.written = '\n'.join(logwriter.written[:50])


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


def recovery_logs():
    print(logwriter.written)
