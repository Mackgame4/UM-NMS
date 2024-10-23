from colorama import Fore
import subprocess
import platform
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add the project root directory to sys.path

def open_new_terminal(command):
    system_name = platform.system()
    if system_name == "Windows":
        # Windows: use 'start' to open a new terminal
        subprocess.run(f'start cmd /k {command}', shell=True)
    elif system_name == "Linux":
        # Linux: use 'gnome-terminal' or 'xterm' depending on availability
        subprocess.run(f'gnome-terminal -- bash -c "{command}; exec bash"', shell=True)
    elif system_name == "Darwin":
        # macOS: use 'open' to start a new terminal
        subprocess.run(f'osascript -e \'tell application "Terminal" to do script "{command}"\'', shell=True)
    else:
        print(Fore.RED + "Unsupported OS." + Fore.RESET)

def main():
    option = -1
    while option != 0:
        print(Fore.YELLOW + "1" + Fore.RESET + ". Start Server (NMS_Server)")
        print(Fore.YELLOW + "2" + Fore.RESET + ". Start Client (NMS_Agent)")
        print(Fore.YELLOW + "0" + Fore.RESET + ". Exit")

        option = int(input(Fore.YELLOW + "Select an option: " + Fore.RESET))
        if option == 0:
            print(Fore.RED + "Exiting...\n" + Fore.RESET)
        elif option == 1:
            print(Fore.GREEN + "Starting Server...\n" + Fore.RESET)
            # Start server
            command = "python server/s_main.py"
            # open a new terminal and run the server
            open_new_terminal(command)
        elif option == 2:
            print(Fore.GREEN + "Starting Client...\n" + Fore.RESET)
            # Start client
            command = "python client/c_main.py"
            # open a new terminal and run the client
            open_new_terminal(command)
        else:
            print(Fore.RED + "Invalid option. Try again.\n" + Fore.RESET)

if __name__ == "__main__":
    main()