from colorama import Fore, Back

DEBUG = True

def notify(type, message):
    if type == 'info':
        print(Back.BLUE + "[INFO]" + Back.RESET + " " + Fore.BLUE + message + Fore.RESET)
    elif type == 'warning':
        print(Back.YELLOW + "[WARNING]" + Back.RESET + " " + Fore.YELLOW + message + Fore.RESET)
    elif type == 'error':
        print(Back.RED + "[ERROR]" + Back.RESET + " " + Fore.RED + message + Fore.RESET)
    elif type == 'success':
        print(Back.GREEN + "[SUCCESS]" + Back.RESET + " " + Fore.GREEN + message + Fore.RESET)
    elif type == 'debug':
        if DEBUG:
            print(Back.CYAN + "[DEBUG]" + Back.RESET + " " + Fore.CYAN + message + Fore.RESET)
    elif type == 'message':
        print(Back.WHITE + "[MESSAGE]" + Back.RESET + " " + Fore.WHITE + message + Fore.RESET)
    else:
        print(message)