import ctypes, sys
from os import name


def is_admin():
    if name != 'nt':
        return True

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def request_admin():
    if name != 'nt':
        return True

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,
                                            " ".join(sys.argv), None, 1)

    return is_admin()