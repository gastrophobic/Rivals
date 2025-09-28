import sys
from colorama import Fore, Style, init
init(autoreset=True)
import os
import json

# ────────────────────────────────────────────────────────────────────────────────
# Input helpers
# ────────────────────────────────────────────────────────────────────────────────

def get_valid_input(prompt, valid_values=None, secret_numbers=None):
    """
    Accepts numeric choices, 'back', and optional secret numbers that bypass valid_values.
    Returns either 'back' or an int.
    """
    secret_numbers = set(secret_numbers or [])
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'back':
            return 'back'
        if user_input.isdigit():
            val = int(user_input)
            if (valid_values is None or val in valid_values) or (val in secret_numbers):
                return val
            print(f"{Fore.RED}Invalid option. Please choose from {valid_values}.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid input. Please enter a number or 'back'.{Style.RESET_ALL}")


def get_yes_no(prompt, default=None):
    """
    Professional yes/no confirmation.
    default: None | True | False
    """
    suffix = " [y/n]: "
    if default is True:
        suffix = " [Y/n]: "
    elif default is False:
        suffix = " [y/N]: "

    while True:
        resp = input(f"{prompt}{suffix}").strip().lower()
        if not resp and default is not None:
            return default
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print(f"{Fore.RED}Please answer 'y' or 'n'.{Style.RESET_ALL}")


# ────────────────────────────────────────────────────────────────────────────────
# Glue for returning to your backbone()
# ────────────────────────────────────────────────────────────────────────────────

def push(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names):
    main_module = sys.modules['__main__']
    main_module.backbone(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names)


# ────────────────────────────────────────────────────────────────────────────────
# Settings & bootstrapper
# ────────────────────────────────────────────────────────────────────────────────

with open(os.path.join("storage", "settings.json"), 'r') as f:
    settings_data = json.load(f)
bootstrapper_type = settings_data.get("bootstrapper")

def bootstrapper():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), bootstrapper_type, 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]

    if not os.path.exists(base_path):
        print(f"{Fore.RED}{bootstrapper_type} not found{Style.RESET_ALL}")
        return

    path = base_path
    for folder in nested_folders:
        path = os.path.join(path, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"{Fore.GREEN}Created folder:{Style.RESET_ALL} {path}")
        else:
            print(f"{Fore.BLUE}Folder exists:{Style.RESET_ALL} {path}")

    print(f"{Fore.GREEN}All folders verified. Import your skyboxes into the opened folder.{Style.RESET_ALL}")
    os.startfile(path)


# ────────────────────────────────────────────────────────────────────────────────
# UX helpers
# ────────────────────────────────────────────────────────────────────────────────

def banner():
    line = f"{Fore.MAGENTA}{'─' * 60}{Style.RESET_ALL}"
    title = f"{Fore.CYAN}ASSET REPLACEMENTS{Style.RESET_ALL}"
    print(f"\n{line}\n{title}\n{line}")

def toast_success(message):
    print(f"{Fore.GREEN}✔ {message}{Style.RESET_ALL}")

def toast_info(message):
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def toast_warn(message):
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def toast_error(message):
    print(f"{Fore.RED}✖ {message}{Style.RESET_ALL}")


# ────────────────────────────────────────────────────────────────────────────────
# Main menu
# ────────────────────────────────────────────────────────────────────────────────

def run(json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names):

    while True:
        banner()
        print(
            f"0:  {Fore.GREEN}Custom{Style.RESET_ALL}\n"
            f"1:  {Fore.GREEN}Custom skyboxes{Style.RESET_ALL}\n"
            f"2:  {Fore.GREEN}Custom hitsounds{Style.RESET_ALL}\n"
            f"3:  {Fore.GREEN}Custom gun sounds{Style.RESET_ALL}\n"
            f"4:  {Fore.GREEN}No arms{Style.RESET_ALL}\n"
            f"{Fore.MAGENTA}ProTip:{Style.RESET_ALL} Clearing full cache in 'Cache settings' removes all custom changes.\n"
            f"Type 'back' to return to the previous menu."
        )

        options = get_valid_input(
            prompt="Select an option: ",
            valid_values=[0, 1, 2, 3, 4],
            secret_numbers=[67]  # secret: No AR
        )

        if options == 'back':
            toast_info("Returning to main menu.")
            skip = True
            return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

        try:
            # Secret code: 67 => NO AR (with confirmation + warning)
            if options == 67:
                print()
                toast_warn("Secret detected: NO AR")
                print(f"{Fore.YELLOW}Applying this may be bannable. Proceed at your own risk.{Style.RESET_ALL}")
                if not get_yes_no("Do you want to apply NO AR now?", default=False):
                    toast_info("Secret action cancelled.")
                    continue
                start_key = "assaultrifle"   # NO AR
                start_key2 = "mp5"
                toast_success("NO AR applied.")
                return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

            match options:
                case 0:
                    toast_info("Keeping default custom behavior.")
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

                case 1:
                    while True:
                        print(f"\nIs {bootstrapper_type} sky folder set up?")
                        sky_option = get_valid_input(
                            f"1: {Fore.GREEN}Yes{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}No (create/verify folders){Style.RESET_ALL}\n"
                            f"Type 'back' to return.\nSelect: ",
                            valid_values=[1, 2]
                        )

                        if sky_option == 'back':
                            toast_info("Returning to Asset replacements.")
                            break

                        if sky_option == 2:
                            bootstrapper()

                        # Confirm applying skybox replacement
                        if get_yes_no("Apply custom skyboxes now?", default=True):
                            start_key = "skyboxes"
                            start_key2 = "remove"
                            toast_success("Custom skyboxes selected.")
                            return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names
                        else:
                            toast_info("Skybox change cancelled.")
                            break

                case 2:
                    if get_yes_no("Apply custom hitsounds?", default=True):
                        start_key = "hitsounds"
                        start_key2 = "replacement sounds"
                        toast_success("Custom hitsounds selected.")
                        return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names
                    else:
                        toast_info("Hitsounds change cancelled.")
                        continue

                case 3:
                    if get_yes_no("Apply custom gun sounds?", default=True):
                        start_key = "gun sounds"
                        start_key2 = "replacement sounds"
                        toast_success("Custom gun sounds selected.")
                        return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names
                    else:
                        toast_info("Gun sounds change cancelled.")
                        continue

                case 4:
                    print()
                    toast_warn("You are about to enable NO ARMS.")
                    if not get_yes_no("Proceed with applying NO ARMS?", default=True):
                        toast_info("No arms action cancelled.")
                        continue
                    start_key = "arms"   # NO ARMS
                    start_key2 = "mp5"
                    toast_success("NO ARMS applied.")
                    return json_data, start_key, start_key2, addon, addon2, skip, game_pre, display_names

        except Exception as e:
            toast_error(f"An error occurred: {e}")
