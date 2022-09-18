from datetime import datetime
from colorama import Fore


def log(content, message_type='ИНФО', color=Fore.GREEN, spaces=3):
    time_now = datetime.now().strftime('%H:%M:%S')
    print(
        f'{Fore.CYAN}{time_now} {Fore.YELLOW}{color}[{message_type}]{Fore.CYAN}{" " * spaces} : {Fore.GREEN}{content}{Fore.WHITE}'
    )