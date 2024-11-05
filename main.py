from colorama import Fore
import subprocess
import platform

def open_new_terminal(module_name, function_name):
    command = f"python -c \"from {module_name} import {function_name}; {function_name}()\""
    system_name = platform.system()
    if system_name == "Windows":
        subprocess.run(f'start cmd /k "{command}"', shell=True) # Windows: use 'start' to open a new command prompt
    elif system_name == "Linux":
        subprocess.run(f'gnome-terminal -- bash -c "{command}; exec bash"', shell=True) # Linux: use 'gnome-terminal' or 'xterm'
    elif system_name == "Darwin":
        subprocess.run(['osascript', '-e', f'tell application "Terminal" to do script "{command}"']) # macOS: use osascript to run command in Terminal
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
            open_new_terminal("NMS_Server", "main") # Open a new terminal to run NMS_Server.main()
        elif option == 2:
            print(Fore.GREEN + "Starting Client...\n" + Fore.RESET)
            open_new_terminal("NMS_Agent", "main") # Open a new terminal to run NMS_Agent.main()
        else:
            print(Fore.RED + "Invalid option. Try again.\n" + Fore.RESET)

if __name__ == "__main__":
    main()