import sys
from colorama import Fore, Style, init
init()
import os
import json

def get_valid_input(prompt, valid_values=None, secret_numbers=None):
    """
    Accepts numeric choices, 'back', and optional secret numbers
    that bypass valid_values.
    """
    secret_numbers = set(secret_numbers or [])
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'back':
            return 'back'
        # secret numeric easter eggs
        if user_input.isdigit() and int(user_input) in secret_numbers:
            return int(user_input)
        try:
            if valid_values is None or int(user_input) in valid_values:
                return int(user_input)
            else:
                print(f"{Fore.RED}\nInvalid option. Please choose from {valid_values}.\n{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}\nInvalid input. Please enter a valid number.\n{Style.RESET_ALL}")

def push(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names):
    main_module = sys.modules['__main__']
    main_module.backbone(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names)

with open(os.path.join("storage", "settings.json"), 'r') as f:
    settings_data = json.load(f)
bootstrapper_type = settings_data.get("bootstrapper")

def bootstrapper():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), bootstrapper_type, 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]

    if not os.path.exists(base_path):
        print(f"{Fore.RED}{bootstrapper_type} not found{Style.RESET_ALL}")
    else:
        path = base_path
        for folder in nested_folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created folder: {path}")
            else:
                print(f"Folder already exists: {path}")

        print("All folders created successfully! Import your skyboxes into the opened folder.")
        os.startfile(path)

def run(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names):

    while True:
        options = get_valid_input(
            f"Asset replacements:\n"
            f"0:  {Fore.GREEN}Custom{Style.RESET_ALL}\n"
            f"1:  {Fore.GREEN}Custom skyboxes{Style.RESET_ALL}\n"
            f"2:  {Fore.GREEN}Custom hitsounds{Style.RESET_ALL}\n"
            f"3:  {Fore.GREEN}Custom gun sounds{Style.RESET_ALL}\n"
            f"4:  {Fore.GREEN}No arms{Style.RESET_ALL}\n"
            f"{Fore.MAGENTA}ProTip:{Style.RESET_ALL} Clearing full cache in 'Cache settings' will remove all custom changes!\n"
            f"Type 'back' to return to the previous menu.\n: ",
            valid_values=[0, 1, 2, 3, 4],
            secret_numbers=[67]  # ← secret code for No AR
        )

        if options == 'back':
            print(f"{Fore.CYAN}\nReturning to main menu.{Style.RESET_ALL}")
            skip = True
            return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

        try:
            # Secret code: 67 => apply NO AR
            if options == 67:
                print(f"{Fore.YELLOW}\nCongrats! You found a secret number.\n"
                      f"{Style.RESET_ALL}{Fore.CYAN}Applying NO AR…{Style.RESET_ALL}\n"
                      f"{Fore.RED}Use at your own risk. This may be bannable.{Style.RESET_ALL}")
                start_key = "assaultrifle"
                start_key2 = "mp5"
                return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

            match options:
                case 0:
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

                case 1:
                    while True:
                        sky_option = get_valid_input(
                            f"\nIs {bootstrapper_type} sky folder setup?\n"
                            f"1: {Fore.GREEN}yes{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}no{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )

                        if sky_option == 'back':
                            print(f"\n{Fore.CYAN}Returning to Asset replacements.{Style.RESET_ALL}")
                            break

                        match sky_option:
                            case 1:
                                start_key = "skyboxes"
                                start_key2 = "remove"
                                return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names
                            case 2:
                                bootstrapper()
                                start_key = "skyboxes"
                                start_key2 = "remove"
                                return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

                case 2:
                    start_key = "hitsounds"
                    start_key2 = "replacement sounds"
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

                case 3:
                    start_key = "gun sounds"
                    start_key2 = "replacement sounds"
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

                case 4:
                    # Directly apply NO ARMS (no submenu)
                    print(f"{Fore.CYAN}Applying NO ARMS…{Style.RESET_ALL}")
                    start_key = "arms"
                    start_key2 = "mp5"
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
