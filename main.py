from colorama import Fore
from notify import notify
import subprocess
import platform
import os
import sys

CLIENT_FILE = os.path.join(".", "NMS_Agent.py")
SERVER_FILE = os.path.join(".", "NMS_Server.py")
REQ_FILE = os.path.join(".", "requirements.txt")

def get_platform():
    return platform.system()

def install_dependencies():
    platform = get_platform()
    if platform == "Windows":
        os.system(f"pip install -r {REQ_FILE}")
    elif platform == "Linux":
        os.system(f"pip3 install -r {REQ_FILE}")
    elif platform == "Darwin":
        os.system(f"pip3 install -r {REQ_FILE}")
    else:
        notify("error", "Unsupported platform.")
        exit()

def open_terminal(file, args):
    platform = get_platform()
    args = " ".join(args)
    if platform == "Windows":
        subprocess.run(f'start cmd /k "python {file} {args}"', shell=True)
    elif platform == "Linux":
        subprocess.run(f'gnome-terminal -- python3 {file} {args}', shell=True)
    elif platform == "Darwin":
        subprocess.run(f'open -a Terminal python3 {file} {args}', shell=True)
    else:
        notify("error", "Unsupported platform.")
        exit()

def run_command(command, args):
    platform = get_platform()
    args = " ".join(args)
    if platform == "Windows":
        os.system(f"python {command} {args}")
    elif platform == "Linux":
        os.system(f"python3 {command} {args}")
    elif platform == "Darwin":
        os.system(f"python3 {command} {args}")
    else:
        notify("error", "Unsupported platform.")
        exit()

def run_client(new_process, args):
    install_dependencies()
    if new_process:
        open_terminal(CLIENT_FILE, args)
    else:
        run_command(CLIENT_FILE, args)

def run_server(new_process, args):
    install_dependencies()
    if new_process:
        open_terminal(SERVER_FILE, args)
    else:
        run_command(SERVER_FILE, args)

def showMenu():
    args = ["127.0.0.1", "8888"]
    option = -1
    while option != 0:
        print(Fore.YELLOW + "1" + Fore.RESET + ". Start Server (NMS_Server)")
        print(Fore.YELLOW + "2" + Fore.RESET + ". Start Client (NMS_Agent)")
        print(Fore.YELLOW + "3" + Fore.RESET + ". Start Development Server (NMS_Server)")
        print(Fore.YELLOW + "4" + Fore.RESET + ". Start Development Client (NMS_Agent)")
        print(Fore.YELLOW + "0" + Fore.RESET + ". Exit")
        option = int(input(Fore.YELLOW + "Select an option: " + Fore.RESET))
        if option == 0:
            exit()
        elif option == 1:
            run_server(False, args)
        elif option == 2:
            run_client(False, args)
        elif option == 3:
            run_server(True, args)
        elif option == 4:
            run_client(True, args)
        else:
            notify("error", "Invalid option. Try again.\n")

def exit():
    print(Fore.RED + "Exiting...\n" + Fore.RESET)
    sys.exit()

def main(args):
    if len(args) == 0:
        showMenu()
    command = args[0]
    if command == "client":
        run_client(False, args[1:])
    elif command == "server":
        run_server(False, args[1:])
    elif command == "dev-client":
        run_client(True, args[1:])
    elif command == "dev-server":
        run_server(True, args[1:])
    else:
        notify("error", "Invalid command. Try again.\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)