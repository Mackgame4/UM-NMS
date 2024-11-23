from colorama import Fore
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
        print(Fore.RED + "Unsupported platform." + Fore.RESET)
        exit()

def open_terminal(file):
    platform = get_platform()
    if platform == "Windows":
        subprocess.run(f'start cmd /k "python {file}"', shell=True)
    elif platform == "Linux":
        subprocess.run(f'gnome-terminal -- python3 {file}', shell=True)
    elif platform == "Darwin":
        subprocess.run(f'open -a Terminal python3 {file}', shell=True)
    else:
        print(Fore.RED + "Unsupported platform." + Fore.RESET)
        exit()

def run_command(command):
    platform = get_platform()
    if platform == "Windows":
        os.system(f"python {command}")
    elif platform == "Linux":
        os.system(f"python3 {command}")
    elif platform == "Darwin":
        os.system(f"python3 {command}")
    else:
        print(Fore.RED + "Unsupported platform." + Fore.RESET)
        exit()

def run_client(new_process):
    install_dependencies()
    if new_process:
        open_terminal(CLIENT_FILE)
    else:
        run_command(CLIENT_FILE)

def run_server(new_process):
    install_dependencies()
    if new_process:
        open_terminal(SERVER_FILE)
    else:
        run_command(SERVER_FILE)

def showMenu():
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
            run_server(False)
        elif option == 2:
            run_client(False)
        elif option == 3:
            run_server(True)
        elif option == 4:
            run_client(True)
        else:
            print(Fore.RED + "Invalid option. Try again.\n" + Fore.RESET)

def exit():
    print(Fore.RED + "Exiting...\n" + Fore.RESET)
    sys.exit()

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        showMenu()
    command = args[0]
    if command == "client":
        run_client(False)
    elif command == "server":
        run_server(False)
    elif command == "dev-client":
        run_client(True)
    elif command == "dev-server":
        run_server(True)
    else:
        print(Fore.RED + "Invalid command." + Fore.RESET)

if __name__ == "__main__":
    main()