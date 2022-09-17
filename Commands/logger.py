from datetime import datetime
from colorama import Fore


def log(content, message_type='ИНФО   ', color=Fore.YELLOW):
    time_now = datetime.now().strftime('%H:%M:%S')
    print(f'{Fore.CYAN}{time_now}{Fore.WHITE} | {color}{message_type}{Fore.WHITE} | {Fore.GREEN}{content}{Fore.WHITE}')