import manipulate_json as mj
import userinput
import encryption
from terminal import clear


def ask_create_account():
    """ Ask the user to create an account by:
    1) Ask account name
    2) Ask if account needs to be protected
    3) Ask name of the field + value of the vield
    4) Repeat until done
    5) Ask to save
    """
    account_name = ask_account_name()
    if not account_name:
        return
    is_protected, encryption_key = ask_protect()
    if is_protected:
        encryption_tip = ask_encryption_tip()
    else:
        encryption_tip = ""
    field_dictionnary = ask_field_loop(is_protected, encryption_key)
    ask_save_account(account_name, field_dictionnary, is_protected, encryption_tip)
    return account_name, field_dictionnary, is_protected, encryption_tip


def ask_account_name():
    try:
        category_name = userinput.ASK_QUESTION("ENTER ACCOUNT NAME", _exit=True)
    except userinput.EXCEPTION_USER_HELP:
        print("Enter a name for your account")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_account_name()
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        category_name = ""
    return category_name


def ask_field_loop(is_protected, encryption_key=""):
    field_dictionnary = {}
    while True:
        try:
            clear()
            protect_string = "ACCOUNT PROTECTED" if is_protected else "ACCOUNT NOT PROTECTED"
            print(protect_string)
            wrote_yet = ", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary])
            if wrote_yet:
                print(wrote_yet)
            key = userinput.ASK_QUESTION("NAME?", _remove=True, _help=True, _exit=True)
            value = userinput.ASK_QUESTION("VALUE?", _remove=True, _help=True, _exit=True)
            field_dictionnary[key] = value
            print(", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary]))
        except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
            try:
                wants_to_quit = userinput.ASK_CONFIRMATION("ARE YOU FINISHED?", _repeat=True, _default_answer=True)
                if wants_to_quit:
                    break
                else:
                    continue
            except KeyboardInterrupt:
                break
        except userinput.EXCEPTION_USER_HELP:
            print("Enter a field name, and a field value")
            userinput.PRINT_REMOVE()
            userinput.PRINT_HELP()
            userinput.PRINT_EXIT()
            userinput.ASK_CONTINUE()
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            field_dictionnary = ask_remove(field_dictionnary)
            continue
    if is_protected:
        return encryption.encrypt_dictionnary(field_dictionnary, encryption_key)
    else:
        return field_dictionnary


def ask_remove(field_dictionnary):
    try:
        clear()
        wrote_yet = ", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary])
        if wrote_yet:
            print(wrote_yet)
        key_to_remove = userinput.ASK_QUESTION("WHICH KEY TO REMOVE?", _help=True, _exit=True)
        field_dictionnary.pop(key_to_remove, None)
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print("You can remove any field by entering its name (= key)")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_remove(field_dictionnary)
    return field_dictionnary


def ask_protect():
    is_protected, encryption_key = False, ""

    def fail():
        print("INCORRECT INPUT")
    try:
        wants_to_protect = userinput.ASK_CONFIRMATION("PROTECT ACCOUNT?", _fail_function=fail, _repeat=True, _exit=True, _help=True)
        if wants_to_protect:
            is_protected, encryption_key = ask_encryption_key()
    except userinput.EXCEPTION_USER_HELP:
        print("Protect your account with a password, which will be asked before showing the account")
        userinput.PRINT_YES()
        userinput.PRINT_NO()
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_protect()
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    return is_protected, encryption_key


def ask_encryption_key():
    is_protected, encryption_key = False, ""
    try:
        encryption_key_one = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD", _help=True, _exit=True)
        encryption_key_two = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD AGAIN (CONFIRMATION)", _help=True, _exit=True)
        if encryption_key_one == encryption_key_two:
            is_protected = True
            encryption_key = encryption_key_one
        else:
            print("ERROR : PASSWORD DIFFERENT")
            return(ask_encryption_key())
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print("This password will protect your account, and be asked before showing the account")
        userinput.PRINT_EXIT()
        userinput.PRINT_HELP()
        userinput.ASK_CONTINUE()
        return ask_encryption_key()
    return is_protected, encryption_key


def ask_encryption_tip():
    encryption_tip = ""
    try:
        encryption_tip = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD TIP", _help=True, _exit=True)
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        print("YOU HAVE TO ENTER A TIP")
        return(ask_encryption_tip())
    except userinput.EXCEPTION_USER_HELP:
        print("This tip will help you remember which encryption password you've put on this account")
        userinput.PRINT_HELP()
        userinput.ASK_CONTINUE()
        return ask_encryption_tip()
    return encryption_tip


def ask_save_account(account_name, field_dictionnary, is_protected, encryption_tip):
    clear()
    s = ", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary])
    s += " | " if s else ""
    s += "PROTECTED" if is_protected else "NOT PROTECTED"
    s += f" | {encryption_tip}" if encryption_tip else ""
    print(s)
    try:
        file_name = userinput.ASK_QUESTION("FILE NAME FOR ACCOUNT?", _help=True, _exit=True)
        file_name = file_name.replace('.json', '')
        account_dictionnary = {'account_name': account_name, 'field_dictionnary': field_dictionnary,
                               'is_protect': is_protected, 'encryption_tip': encryption_tip}
        mj.save_file(account_dictionnary, f"data/account/{file_name}.json")
    except userinput.EXCEPTION_USER_HELP:
        print("Account will be saved under data/account/[name]. You can enter name with / to save it under a folder.")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_save_account(account_name, field_dictionnary, is_protected, encryption_tip)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    ask_create_account()
