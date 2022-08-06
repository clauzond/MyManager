import manipulate_json as mj
import userinput
import encryption
from terminal import clear
from manipulate_file import get_all_files_from
from termcolor import colored
import pyperclip
import pyautogui
import time
import os


def ask_create_account():
    """ Ask the user to create an account by:
    1) Ask account path
    2) Ask account name
    3) Ask if account needs to be protected
    4) Ask name of the field + value of the vield
    5) Repeat until done
    6) Ask which field is important to show
    7) Ask to save
    """
    account_path = ask_account_path()
    if not account_path:
        return
    account_name = ask_account_name(account_path)
    if not account_name:
        return
    is_protected, encryption_key = ask_protect(account_path)
    if is_protected:
        encryption_tip = ask_encryption_tip(account_path)
    else:
        encryption_tip = ""
    field_dictionnary = ask_field_loop(account_path, is_protected, encryption_key)
    if not field_dictionnary:
        return
    list_to_copy = ask_field_to_copy(account_path, field_dictionnary)
    if not list_to_copy:
        return
    return ask_save_account(account_path, account_name, field_dictionnary, is_protected, encryption_tip, encryption_key, list_to_copy)


LIST_FILES_COMMAND = userinput.GET_FILES_LIST


def ask_account_path(do_clear=True):
    if do_clear:
        clear()
    try:
        question = "ENTER PATH FOR YOUR ACCOUNT"
        account_path = userinput.ASK_QUESTION(question, _help=True, _exit=True)
        if account_path in LIST_FILES_COMMAND:
            print(", ".join(get_all_files_from("data/account")))
            userinput.ASK_CONTINUE()
            return ask_account_path(do_clear=False)
        if not (len(account_path) > 5 and account_path[-5:] == ".json"):
            account_path += ".json"
        full_path = "data/account/" + account_path
        if os.path.isfile(full_path):
            question = "ARE YOU SURE YOU WANT TO MODIFY THIS ACCOUNT?"
            try:
                wants_modify = userinput.ASK_CONFIRMATION(question)
            except KeyboardInterrupt:
                return ask_account_path(do_clear=True)
            if wants_modify:
                return account_path
            else:
                return ask_account_path(do_clear=True)
        else:
            return account_path
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        return
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter the path name of your account", userinput.HELP_COLOR))
        print(colored(f"LIST ALL LISTS: {', '.join(LIST_FILES_COMMAND)}", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_account_path(do_clear=True)


def ask_account_name(account_path):
    clear()
    account_name = ""
    if os.path.isfile(f"data/account/{account_path}"):
        dic = mj.load_file(f"data/account/{account_path}")
        account_name = dic['name']
        if account_name:
            question = f"DO YOU WANT TO KEEP THE ACCOUNT'S NAME ({account_name})?"
            try:
                wants_keep = userinput.ASK_CONFIRMATION(question)
            except KeyboardInterrupt:
                return ask_account_name(account_path)
            if wants_keep:
                return account_name
            else:
                pass
    try:
        account_name = userinput.ASK_QUESTION("ENTER ACCOUNT NAME", _exit=True)
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter a name for your account", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_account_name(account_path)
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    return account_name


def ask_protect(account_path):
    if os.path.isfile(f"data/account/{account_path}"):
        dic = mj.load_file(f"data/account/{account_path}")
        is_protected = dic['is_protected']
        real_hash = dic['hash']
        if is_protected:
            question = "ACCOUNT ALREADY PROTECTED. CONFIRM PASSWORD"
            temp_encryption_key = userinput.ASK_QUESTION(question)
            can_access = encryption.verify_hash(temp_encryption_key, real_hash)
            if can_access:
                return is_protected, temp_encryption_key
            else:
                raise Exception("PASSWORDS NOT MATCHING")
        else:
            pass

    is_protected, encryption_key = False, ""

    def fail():
        print(colored("INCORRECT INPUT", userinput.EXCEPTION_COLOR))
    try:
        clear()
        wants_to_protect = userinput.ASK_CONFIRMATION("PROTECT ACCOUNT?", _fail_function=fail, _repeat=True, _exit=True, _help=True)
        if wants_to_protect:
            is_protected, encryption_key = ask_encryption_key(account_path)
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Protect your account with a password, which will be asked before showing the account", userinput.HELP_COLOR))
        userinput.PRINT_YES()
        userinput.PRINT_NO()
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_protect(account_path)
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    return is_protected, encryption_key


def ask_encryption_key(account_path):
    is_protected, encryption_key = False, ""
    try:
        encryption_key_one = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD", _help=True, _exit=True)
        encryption_key_two = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD AGAIN (CONFIRMATION)", _help=True, _exit=True)
        if encryption_key_one == encryption_key_two:
            is_protected = True
            encryption_key = encryption_key_one
        else:
            print(colored("ERROR: PASSWORD DIFFERENT", userinput.EXCEPTION_COLOR))
            return(ask_encryption_key(account_path))
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print(colored("This password will protect your account, and be asked before showing the account", userinput.HELP_COLOR))
        userinput.PRINT_EXIT()
        userinput.PRINT_HELP()
        userinput.ASK_CONTINUE()
        return ask_encryption_key(account_path)
    return is_protected, encryption_key


def ask_encryption_tip(account_path):
    if os.path.isfile(f"data/account/{account_path}"):
        return mj.load_file(f"data/account/{account_path}")['encryption_tip']
    encryption_tip = ""
    try:
        encryption_tip = userinput.ASK_QUESTION("ENTER ENCRYPTION PASSWORD TIP", _help=True, _exit=True)
    except (userinput.EXCEPTION_USER_EXIT, KeyboardInterrupt):
        print(colored("YOU HAVE TO ENTER A TIP", userinput.EXCEPTION_COLOR))
        return(ask_encryption_tip(account_path))
    except userinput.EXCEPTION_USER_HELP:
        print(colored("This tip will help you remember which encryption password you've put on this account", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.ASK_CONTINUE()
        return ask_encryption_tip(account_path)
    return encryption_tip


def ask_field_loop(account_path, is_protected, encryption_key=""):
    if os.path.isfile(f"data/account/{account_path}"):
        dic = mj.load_file(f"data/account/{account_path}")
        if is_protected:
            field_dictionnary = encryption.decrypt_dictionnary(dic['field_dictionnary'], encryption_key)
        else:
            field_dictionnary = dic['field_dictionnary']
    else:
        field_dictionnary = {}
    while True:
        try:
            clear()
            protect_string = "ACCOUNT PROTECTED" if is_protected else "ACCOUNT NOT PROTECTED"
            print(protect_string)
            wrote_yet = ", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary])
            if wrote_yet:
                print(wrote_yet)
            key = userinput.ASK_QUESTION("FIELD NAME?", _remove=True, _help=True, _exit=True)
            value = userinput.ASK_QUESTION("FIELD VALUE?", _remove=True, _help=True, _exit=True)
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
            print(colored("Enter a field name, and a field value", userinput.HELP_COLOR))
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


def ask_field_to_copy(account_path, field_dictionnary):
    if os.path.isfile(f"data/account/{account_path}"):
        dic = mj.load_file(f"data/account/{account_path}")
        list_to_copy = dic['list_to_copy']
    else:
        list_to_copy = []
    while True:
        try:
            clear()
            string_keys = ", ".join([f"{key}" for key in field_dictionnary])
            string_copy_list = ", ".join([f"{i+1}. {list_to_copy[i]}" for i in range(len(list_to_copy))])
            print("FIELDS:", string_keys)
            print("COPY LIST:", string_copy_list)
            key_to_copy = userinput.ASK_QUESTION("ENTER FIELD TO COPY", _exit=True, _help=True, _remove=True)
            if key_to_copy in field_dictionnary.keys() and key_to_copy not in list_to_copy:
                list_to_copy.append(key_to_copy)
            continue
        except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
            break
        except userinput.EXCEPTION_USER_HELP:
            print(colored("Enter which field you'll need to copy (ORDER IS IMPORTANT)", userinput.HELP_COLOR))
            userinput.PRINT_REMOVE()
            userinput.PRINT_HELP()
            userinput.PRINT_EXIT()
            userinput.ASK_CONTINUE()
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            try:
                clear()
                string_keys = ", ".join([f"{key}" for key in field_dictionnary])
                string_copy_list = ", ".join([f"{i+1}. {list_to_copy[i]}" for i in range(len(list_to_copy))])
                print("FIELDS: ", string_keys)
                print("COPY LIST: ", string_copy_list)
                key_to_remove = userinput.ASK_QUESTION("ENTER FIELD TO REMOVE")
                if key_to_remove in list_to_copy:
                    list_to_copy.remove(key_to_remove)
                continue
            except KeyboardInterrupt:
                continue
    return list_to_copy


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
        print(colored("You can remove any field by entering its name (= key)", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_remove(field_dictionnary)
    return field_dictionnary


def bleep_dictionnary(dic):
    for key in dic:
        dic[key] = "*"*len(dic[key])
    return dic


def copy_main_fields(list_to_copy, clear_dictionnary, field_dictionnary, delay):
    delay = int(delay)
    num = 0
    for key in list_to_copy:
        num += 1
        pyperclip.copy(clear_dictionnary[key])
        for i in range(delay, 0, -1):
            for j in range(0, 4):
                clear()
                print(field_dictionnary)
                s = f"COPY LIST: {', '.join(list_to_copy)}" + "\n"
                s += colored(f"{key} copied", userinput.MENU_COLOR) + "\n"
                s += f"[{num}] {i}{'.'*j}\n"
                print(s)
                time.sleep(0.333)
    pyperclip.copy("")
    return


def paste_main_fields(list_to_copy, clear_dictionnary, field_dictionnary, delay):
    delay = int(delay)
    time.sleep(delay)
    num = 0
    for key in list_to_copy:
        for i in range(delay, 0, -1):
            for j in range(0, 4):
                clear()
                print(field_dictionnary)
                s = f"COPY LIST: {', '.join(list_to_copy)}" + "\n"
                s += colored(f"{key} copied", userinput.MENU_COLOR) + "\n"
                s += f"[{num}] {i}{'.'*j}\n"
                print(s)
        num += 1
        pyautogui.write(clear_dictionnary[key])
        if num < len(list_to_copy):
            pyautogui.press('tab')

    pyautogui.press('enter')
    return


def ask_save_account(account_path, account_name, field_dictionnary, is_protected, encryption_tip, encryption_key, list_to_copy):
    clear()
    s = ", ".join([f"{key}: {field_dictionnary[key]}" for key in field_dictionnary])
    s += " | " if s else ""
    s += f"list_to_copy: {', '.join(list_to_copy)} | " if list_to_copy else ""
    s += "PROTECTED" if is_protected else "NOT PROTECTED"
    s += f" | {encryption_tip}" if encryption_tip else ""
    print(s)
    account_dictionnary = None
    try:
        wants_to_save = userinput.ASK_CONFIRMATION("DO YOU WANT TO SAVE?", _help=True, _exit=True)
        if not wants_to_save:
            return
        account_dictionnary = {'name': account_name, 'field_dictionnary': field_dictionnary,
                               'is_protected': is_protected, 'encryption_tip': encryption_tip, 'list_to_copy': list_to_copy, 'hash': encryption.hash_text(encryption_key)}
        mj.save_file(account_dictionnary, f"data/account/{account_path}")
    except userinput.EXCEPTION_USER_HELP:
        print(
            colored("Category will be saved under data/category/[name]. You can enter name with / to save it under a folder.", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_save_account(account_path, account_name, field_dictionnary, is_protected, encryption_tip, encryption_key, list_to_copy)
    except KeyboardInterrupt:
        return
    return account_dictionnary


if __name__ == "__main__":
    ask_create_account()
