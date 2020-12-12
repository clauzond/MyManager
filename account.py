import manipulate_json as mj
import userinput
from terminal import clear


def ask_create_account():
    """ Create an account :
    Ask the user to create a field (name + value) until exit (removal of any field possible)
    then ask to save
    """
    account_dictionnary = {}
    while True:
        try:
            clear()
            wrote_yet = ", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary])
            if wrote_yet:
                print(wrote_yet)
            key = userinput.ASK_QUESTION("NAME?", _remove=True, _help=True, _exit=True)
            value = userinput.ASK_QUESTION("VALUE?", _remove=True, _help=True, _exit=True)
            account_dictionnary[key] = value
            print(", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary]))
        except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
            try:
                wants_to_quit = userinput.ASK_CONFIRMATION("ARE YOU SURE YOU WANT TO EXIT?", _repeat=True, _default_answer=True)
                if wants_to_quit:
                    break
                else:
                    continue
            except KeyboardInterrupt:
                break
        except userinput.EXCEPTION_USER_HELP:
            userinput.PRINT_REMOVE()
            userinput.PRINT_EXIT()
            userinput.PRINT_HELP()
            input()
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            try:
                clear()
                wrote_yet = ", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary])
                if wrote_yet:
                    print(wrote_yet)
                key_to_remove = userinput.ASK_QUESTION("WHICH KEY TO REMOVE?", _help=True, _exit=True)
                account_dictionnary.pop(key_to_remove, None)
                continue
            except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
                continue
            except userinput.EXCEPTION_USER_HELP:
                userinput.PRINT_EXIT()
                userinput.PRINT_HELP()
            except:
                continue
    ask_save_account(account_dictionnary)
    return account_dictionnary


def ask_save_account(account_dictionnary):
    def fail():
        print("INCORRECT INPUT")
    clear()
    print(", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary]))
    try:
        wants_to_save = userinput.ASK_CONFIRMATION("SAVE ACCOUNT?", _fail_function=fail, _repeat=True, _exit=True, _help=True)
    except userinput.EXCEPTION_USER_HELP:
        userinput.PRINT_YES()
        userinput.PRINT_NO()
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
    except KeyboardInterrupt:
        wants_to_save = False
        return
    if wants_to_save:
        try:
            file_name = userinput.ASK_QUESTION("FILE NAME?", _help=True, _exit=True)
            file_name = file_name.replace('/','')
            mj.save_file(account_dictionnary, f"data/account/{file_name}.json")
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    print(ask_create_account())
