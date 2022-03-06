import colorama


colorama.init(autoreset=True)


def print_error(s: str):
    print(colorama.Fore.RED + s)


def print_success(s: str):
    print(colorama.Fore.GREEN + s)


def print_warning(s: str):
    print(colorama.Fore.YELLOW + s)
