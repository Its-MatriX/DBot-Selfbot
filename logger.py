from datetime import datetime
from colorama import Fore


class logged:
    written = ''


def log(content, message_type='ИНФО', color=Fore.GREEN, spaces=3):
    time_now = datetime.now().strftime('%H:%M:%S')
    to_write = f'{Fore.CYAN}{time_now} {Fore.YELLOW}{color}[{message_type}]{Fore.CYAN}{" " * spaces} : {Fore.GREEN}{content}{Fore.WHITE}'

    print(to_write)

    logged.written += '\n' + to_write

    if logged.written.count('\n') > 60:
        logged.written = logged.written.split('\n')
        logged.written = '\n'.join(logged.written[:50])


def recovery_logs():
    print(logged.written)