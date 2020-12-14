import manipulate_json as mj
import userinput
from terminal import clear
import os


def ask_create_category():
    """ Ask the user to complete a category by:
    1) Ask category name
    2) Ask file path of the account
    3) Repeat until done
    4) Ask to save
    """
    category_name = ask_category_name()
    if not category_name:
        return
    file_path_set = ask_file_path()
    ask_save_category(category_name, file_path_set)
    return category_name, file_path_set


def ask_category_name():
    try:
        clear()
        category_name = userinput.ASK_QUESTION("ENTER CATEGORY NAME", _exit=True, _help=True)
    except userinput.EXCEPTION_USER_HELP:
        print("Enter a name for your category")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_category_name()
    except KeyboardInterrupt:
        category_name = ""
    return category_name


def ask_file_path(do_clear=True):
    file_path_set = set()
    while True:
        try:
            if do_clear:
                clear()
                if file_path_set:
                    print(", ".join(file_path_set))
            file_path = userinput.ASK_QUESTION("ENTER FILE PATH", _exit=True, _help=True, _remove=True)
            if not (len(file_path) > 5 and file_path[-5:] == ".json"):
                file_path += ".json"
            full_path = "data/account/" + file_path
            if os.path.isfile(full_path):
                file_path_set.add(file_path)
                do_clear = True
            else:
                print("INVALID PATH")
                return ask_file_path(False)
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            file_path_set = ask_remove(file_path_set)
            continue
        except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
            try:
                wants_to_quit = userinput.ASK_CONFIRMATION("ARE YOU FINISHED?", _repeat=True, _default_answer=True)
                if wants_to_quit:
                    break
                else:
                    continue
            except KeyboardInterrupt:
                break
        except userinput.EXCEPTION_USER_HELP:
            print("Enter a file path containing an account")
            userinput.PRINT_REMOVE()
            userinput.PRINT_HELP()
            userinput.PRINT_EXIT()
            userinput.ASK_CONTINUE()
            do_clear = True
            continue
    return file_path_set


def ask_remove(file_path_set):
    try:
        clear()
        print(", ".join(file_path_set))
        path_to_remove = userinput.ASK_QUESTION("WHICH FILE TO REMOVE?", _help=True, _exit=True)
        if not (len(path_to_remove) > 5 and path_to_remove[-5:] == ".json"):
                path_to_remove += ".json"
        file_path_set.remove(path_to_remove)
    except (KeyError, KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print("You can remove any account by entering its path")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_remove(file_path_set)
    return file_path_set



def ask_save_category(category_name, file_path_set):
    try:
        clear()
        print(category_name, "|", "".join(file_path_set))
        file_name = userinput.ASK_QUESTION("FILE NAME FOR CATEGORY?", _help=True, _exit=True)
        file_name = file_name.replace('.json', '')
        file_path_list = ["data/category/" + path for path in file_path_set]
        category_dictionnary = {'category_name': category_name, 'file_path_list': file_path_list}
        mj.save_file(category_dictionnary, f"data/category/{file_name}.json")
    except userinput.EXCEPTION_USER_HELP:
        print("Category will be saved under data/category/[name]. You can enter name with / to save it under a folder.")
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_save_category(category_name, file_path_set)
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    ask_create_category()
