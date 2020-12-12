WRITING_INPUT = "> "

class InputQuit(Exception):
    def __init__(self):
        super().__init__("User has quit")
USER_QUIT = InputQuit

class InputRemove(Exception):
    def __init__(self):
        super().__init__("User has quit")
USER_REMOVE = InputRemove


def EXIT_CONDITION(userinput):
    userinput = str(userinput)
    b = False
    b = b or userinput=="q"
    b = b or userinput==":q"
    return b

def REMOVE_CONDITION(userinput):
    userinput = str(userinput)
    b = False
    b = b or userinput==":r"
    return b

def ASK_USER(question):
    userinput = str(input(question + "\n" + "> "))
    if EXIT_CONDITION(userinput):
        raise USER_QUIT
    elif REMOVE_CONDITION(userinput):
        raise USER_REMOVE
    return userinput