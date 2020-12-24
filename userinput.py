from terminal import clear
from termcolor import colored


class EXCEPTION_USER_EXIT(Exception):
    def __init__(self):
        super().__init__("User has quit")


class EXCEPTION_USER_REMOVE(Exception):
    def __init__(self):
        super().__init__("User wants to remove a field")


class EXCEPTION_USER_HELP(Exception):
    def __init__(self):
        super().__init__("User wants to get some help")
        
class EXCEPTION_MENU_BACK(Exception):
    def __init__(self):
        super().__init__("Menu back")


WRITING_INPUT = "> "

EXIT_ACCEPT_LIST = ['q', ':q']
REMOVE_ACCEPT_LIST = [':r']
HELP_ACCEPT_LIST = [':h']
CONFIRMATION_YES_LIST = ['y', 'o', 'yes', 'ye', 'oui']
CONFIRMATION_NO_LIST = ['n', 'N', 'no', 'non']

HELP_COLOR = "cyan"
QUESTION_COLOR = "blue"
CONFIRMATION_COLOR = "green"
EXCEPTION_COLOR = "red"
MENU_COLOR = "magenta"

def EXIT_CONDITION(userinput):
    return str(userinput) in EXIT_ACCEPT_LIST


def REMOVE_CONDITION(userinput):
    return str(userinput) in REMOVE_ACCEPT_LIST


def HELP_CONDITION(userinput):
    return str(userinput) in HELP_ACCEPT_LIST


def ASK_QUESTION(question, _remove=False, _help=False, _exit=False):
    userinput = str(input(colored(question, QUESTION_COLOR) + f"\n{WRITING_INPUT}"))
    if _exit and EXIT_CONDITION(userinput):
        raise EXCEPTION_USER_EXIT
    elif _remove and REMOVE_CONDITION(userinput):
        raise EXCEPTION_USER_REMOVE
    elif _help and HELP_CONDITION(userinput):
        raise EXCEPTION_USER_HELP
    return userinput


def ASK_CONFIRMATION(question, _fail_function=lambda: None, _repeat=False, _default_answer=False, _exit=False, _help=False):
    userinput = str(input(colored(question, CONFIRMATION_COLOR) + f" (y/n)\n{WRITING_INPUT}"))
    if _exit and EXIT_CONDITION(userinput):
        raise EXCEPTION_USER_EXIT
    elif _help and HELP_CONDITION(userinput):
        raise EXCEPTION_USER_HELP

    if userinput.lower() in CONFIRMATION_YES_LIST:
        return True
    elif userinput.lower() in CONFIRMATION_NO_LIST:
        return False
    elif _repeat:
        _fail_function()
        return(ASK_CONFIRMATION(question, _fail_function, _repeat, _default_answer, _exit, _help))
    else:
        return _default_answer


def ASK_CONTINUE(question="PRESS ENTER TO CONTINUE"):
    input(question)


def PRINT_HELP():
    print(colored(f"HELP: {', '.join(HELP_ACCEPT_LIST)}", HELP_COLOR))


def PRINT_REMOVE():
    print(colored(f"REMOVE FIELD: {', '.join(REMOVE_ACCEPT_LIST)}", HELP_COLOR))


def PRINT_EXIT():
    print(colored(f"EXIT: {', '.join(EXIT_ACCEPT_LIST)}", HELP_COLOR))


def PRINT_YES():
    print(colored(f"YES: {', '.join(CONFIRMATION_YES_LIST)}", HELP_COLOR))


def PRINT_NO():
    print(colored(f"NO: {', '.join(CONFIRMATION_NO_LIST)}", HELP_COLOR))


def MENU_PRINT(*args):
    clear()
    for string in args:
        print(colored(string, MENU_COLOR))

def MENU_ASK(*args):
    def get_index(userinput):
        if len(userinput)==1 and userinput.isnumeric:
            return int(userinput) - 1
        elif len(userinput)==2 and userinput[0]==":" and userinput[1].isnumeric:
            return int(userinput[1]) - 1
        else:
            return None
    try:
        userinput = str(input(colored(f"{WRITING_INPUT}", MENU_COLOR)))
        index = get_index(userinput)
        if index is None:
            return
        else:
            args[index]()
    except KeyboardInterrupt:
        raise EXCEPTION_MENU_BACK