import manipulate_json as mj
import userinput
from terminal import clear
from manipulate_file import get_all_files_from
from termcolor import colored
import os


def ask_create_category():
    """ Ask the user to complete a category by:
    1) Ask category path
    2) Ask category name
    3) Ask file path of the account
    4) Repeat until done
    5) Ask to save
    """
    category_path = ask_category_path()
    if not category_path:
        return
    category_name = ask_category_name()
    if not category_name:
        return
    account_path_list = ask_account_path_list(category_path=category_path)
    if not account_path_list:
        return
    return ask_save_category(category_path, category_name, account_path_list)


LIST_FILES_COMMAND = userinput.GET_FILES_LIST
def ask_category_path(do_clear=True):
    if do_clear:
        clear()
    try:
        question = "ENTER PATH FOR YOUR CATEGORY"
        category_path = userinput.ASK_QUESTION(question, _help=True, _exit=True)
        if category_path in LIST_FILES_COMMAND:
            print(", ".join(get_all_files_from("data/category")))
            userinput.ASK_CONTINUE()
            return ask_category_path(do_clear=False)
        if not (len(category_path) > 5 and category_path[-5:] == ".json"):
            category_path += ".json"
        full_path = "data/category/" + category_path
        if os.path.isfile(full_path):
            question = "ARE YOU SURE YOU WANT TO MODIFY THIS CATEGORY?"
            try:
                wants_modify = userinput.ASK_CONFIRMATION(question)
            except KeyboardInterrupt:
                return ask_category_path(do_clear=True)
            if wants_modify:
                return category_path
            else:
                return ask_category_path(do_clear=True)
        else:
            return category_path
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        return
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter the path name of your category", userinput.HELP_COLOR))
        print(colored(f"LIST ALL CATEGORIES: {', '.join(LIST_FILES_COMMAND)}", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_category_path(do_clear=True)


def ask_category_name():
    try:
        clear()
        category_name = userinput.ASK_QUESTION("ENTER CATEGORY NAME", _exit=True, _help=True)
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter a name for your category", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_category_name()
    except KeyboardInterrupt:
        category_name = ""
    return category_name


LIST_ACCOUNT_COMMAND = userinput.GET_FILES_LIST
def ask_account_path_list(category_path):
    if os.path.isfile(f"data/category/{category_path}"):
        account_path_list = mj.load_file(f"data/category/{category_path}")
    else:
        account_path_list = []
    do_clear = True
    while True:
        try:
            if do_clear:
                clear()
                if account_path_list:
                    s = ", ".join([f"{i+1}. {account_path_list[i]}" for i in range(len(account_path_list))])
                    print(s)
            file_path = userinput.ASK_QUESTION("ADD ACCOUNT TO CATEGORY", _exit=True, _help=True, _remove=True)
            if file_path in LIST_ACCOUNT_COMMAND:
                print(", ".join(get_all_files_from("data/account")))
                userinput.ASK_CONTINUE()
                do_clear = False
                continue
            if not (len(file_path) > 5 and file_path[-5:] == ".json"):
                file_path += ".json"
            full_path = "data/account/" + file_path
            if os.path.isfile(full_path):
                do_clear = True
                if file_path not in account_path_list:
                    account_path_list.append(file_path)
                else:
                    continue
            else:
                print(colored("INVALID PATH", userinput.EXCEPTION_COLOR))
                do_clear = False
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            account_path_list = ask_remove(account_path_list)
            continue
        except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
            try:
                wants_to_quit = userinput.ASK_CONFIRMATION("ARE YOU FINISHED?", _repeat=True, _default_answer=True)
                if wants_to_quit:
                    break
                else:
                    do_clear = True
                    continue
            except KeyboardInterrupt:
                break
        except userinput.EXCEPTION_USER_HELP:
            print(colored("Enter a file path containing an account", userinput.HELP_COLOR))
            print(colored(f"LIST ALL ACCOUNTS: {', '.join(LIST_ACCOUNT_COMMAND)}", userinput.HELP_COLOR))
            userinput.PRINT_REMOVE()
            userinput.PRINT_HELP()
            userinput.PRINT_EXIT()
            userinput.ASK_CONTINUE()
            do_clear = True
            continue
    return account_path_list


def ask_remove(account_path_list):
    try:
        clear()
        print(", ".join(account_path_list))
        path_to_remove = userinput.ASK_QUESTION("WHICH FILE TO REMOVE?", _help=True, _exit=True)
        if not (len(path_to_remove) > 5 and path_to_remove[-5:] == ".json"):
            path_to_remove += ".json"
        if path_to_remove in account_path_list:
            account_path_list.remove(path_to_remove)
    except (KeyError, KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print(colored("You can remove any account by entering its path", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_remove(account_path_list)
    return account_path_list


def ask_save_category(category_path, category_name, account_path_list):
    category_dictionnary = None
    try:
        clear()
        s = category_name
        s += " | " + ", ".join(account_path_list) if account_path_list else ""
        print(s)
        wants_to_save = userinput.ASK_CONFIRMATION("DO YOU WANT TO SAVE?", _help=True, _exit=True)
        if not wants_to_save:
            return
        file_path_list = list(account_path_list)
        category_dictionnary = {'name': category_name, 'account_path_list': file_path_list}
        mj.save_file(category_dictionnary, f"data/category/{category_path}")
    except userinput.EXCEPTION_USER_HELP:
        print(
            colored("Category will be saved under data/category/[name]. You can enter name with / to save it under a folder.", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_save_category(category_path, category_name, account_path_list)
    except KeyboardInterrupt:
        pass
    return category_dictionnary


if __name__ == "__main__":
    ask_create_category()
