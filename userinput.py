WRITING_INPUT = "> "


class EXCEPTION_USER_EXIT(Exception):
    def __init__(self):
        super().__init__("User has quit")


class EXCEPTION_USER_REMOVE(Exception):
    def __init__(self):
        super().__init__("User wants to remove a field")


class EXCEPTION_USER_HELP(Exception):
    def __init__(self):
        super().__init__("User wants to get some help")


EXIT_ACCEPT_LIST = ['q', ':q']
REMOVE_ACCEPT_LIST = [':r']
HELP_ACCEPT_LIST = [':h']
CONFIRMATION_YES_LIST = ['y', 'o', 'yes', 'ye', 'oui']
CONFIRMATION_NO_LIST = ['n', 'N', 'no', 'non']


def EXIT_CONDITION(userinput):
    return str(userinput) in EXIT_ACCEPT_LIST


def REMOVE_CONDITION(userinput):
    return str(userinput) in REMOVE_ACCEPT_LIST


def HELP_CONDITION(userinput):
    return str(userinput) in HELP_ACCEPT_LIST


def ASK_QUESTION(question, _remove=False, _help=False, _exit=True):
    userinput = str(input(question + "\n> "))
    if _exit and EXIT_CONDITION(userinput):
        raise EXCEPTION_USER_EXIT
    elif _remove and REMOVE_CONDITION(userinput):
        raise EXCEPTION_USER_REMOVE
    elif _help and HELP_CONDITION(userinput):
        raise EXCEPTION_USER_HELP
    return userinput


def ASK_CONFIRMATION(question, _fail_function=lambda :None, _repeat=False, _default_answer=False, _exit=False, _help=False):
    userinput = str(input(question + " (y/n)\n> "))
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


def PRINT_HELP():
    print(f"HELP: {', '.join(HELP_ACCEPT_LIST)}")


def PRINT_REMOVE():
    print(f"REMOVE FIELD: {', '.join(REMOVE_ACCEPT_LIST)}")


def PRINT_EXIT():
    print(f"EXIT: {', '.join(EXIT_ACCEPT_LIST)}")


def PRINT_YES():
    print(f"YES: {', '.join(CONFIRMATION_YES_LIST)}")


def PRINT_NO():
    print(f"NO: {', '.join(CONFIRMATION_NO_LIST)}")
