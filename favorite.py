import userinput
import manipulate_json as mj
from terminal import clear
from manipulate_file import get_all_files_from
from termcolor import colored


def ask_create_favorite():
    """
    1) Ask favorite list path
    2) Ask favorite list name
    3) Freely modify category list (add/remove)
    """
    favorite_path = ask_favorite_path()
    if not favorite_path:
        return
    favorite_name = ask_favorite_name()
    if not favorite_name:
        return
    category_path_list = ask_category_list(favorite_path)
    if not category_path_list:
        return
    return ask_save_category_path_list(favorite_path, category_path_list, favorite_name)


LIST_FILES_COMMAND = [':l', ':ls']


def ask_favorite_path(do_clear=True):
    if do_clear:
        clear()
    try:
        question = "ENTER PATH FOR YOUR FAVORITE LIST"
        favorite_path = userinput.ASK_QUESTION(question, _help=True, _exit=True)
        if favorite_path in LIST_FILES_COMMAND:
            print(", ".join(get_all_files_from("data/favorite")))
            userinput.ASK_CONTINUE()
            return ask_favorite_path(do_clear=False)
        if not (len(favorite_path) > 5 and favorite_path[-5:] == ".json"):
            favorite_path += ".json"
        full_path = "data/favorite/" + favorite_path
        if os.path.isfile(full_path):
            question = "ARE YOU SURE YOU WANT TO MODIFY THIS LIST?"
            try:
                wants_modify = userinput.ASK_CONFIRMATION(question)
            except KeyboardInterrupt:
                return ask_favorite_path(do_clear=True)
            if wants_modify:
                return favorite_path
            else:
                return ask_favorite_path(do_clear=True)
        else:
            return favorite_path
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        return
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter the path name of your favorite list", userinput.HELP_COLOR))
        print(colored(f"LIST ALL LISTS: {', '.join(LIST_FILES_COMMAND)}", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_favorite_path(do_clear=False)


def ask_favorite_name():
    try:
        clear()
        name = userinput.ASK_QUESTION("NAME YOUR FAVORITE LIST (for yourself)", _help=True, _exit=True)
        return name
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Enter the name of your favorite list, used when shown to you.", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_favorite_name()


LIST_CATEGORIES_COMMAND = LIST_FILES_COMMAND


def ask_category_list(favorite_path):
    """ Modify favorite list, whether favorite_path exists or not
    """
    do_clear = True
    if os.path.isfile(f"data/favorite/{favorite_path}"):
        category_path_list = mj.load_file(f"data/favorite/{favorite_path}")['category_path_list']
    else:
        category_path_list = []
    while True:
        try:
            if do_clear:
                clear()
                s = ", ".join([f"{i+1}. {category_path_list[i]}" for i in range(len(category_path_list))])
                if category_path_list:
                    print(s)
            user_path = userinput.ASK_QUESTION("ADD CATEGORY TO FAVORITE LIST", _remove=True, _help=True, _exit=True)
            if user_path in LIST_CATEGORIES_COMMAND:
                print(", ".join(get_all_files_from("data/category")))
                userinput.ASK_CONTINUE()
                do_clear = False
                continue
            elif user_path in category_path_list:
                do_clear = True
                continue
            if not (len(user_path) > 5 and user_path[-5:] == ".json"):
                user_path += ".json"
            full_path = "data/category/" + user_path
            if os.path.isfile(full_path):
                category_path_list.append(user_path)
                do_clear = True
            else:
                print(colored("INVALID PATH", userinput.EXCEPTION_COLOR))
                do_clear = False
            continue
        except userinput.EXCEPTION_USER_REMOVE:
            category_path_list = ask_remove(category_path_list)
            do_clear = True
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
            print(colored("Enter a file path containing a category", userinput.HELP_COLOR))
            print(colored(f"LIST ALL CATEGORIES: {', '.join(LIST_CATEGORIES_COMMAND)}", userinput.HELP_COLOR))
            userinput.PRINT_REMOVE()
            userinput.PRINT_HELP()
            userinput.PRINT_EXIT()
            userinput.ASK_CONTINUE()
            do_clear = True
            continue
    return category_path_list


def ask_remove(category_path_list):
    try:
        clear()
        print(", ".join(category_path_list))
        path_to_remove = userinput.ASK_QUESTION("WHICH FILE TO REMOVE?", _help=True, _exit=True)
        if not (len(path_to_remove) > 5 and path_to_remove[-5:] == ".json"):
            path_to_remove += ".json"
        if path_to_remove in category_path_list:
            category_path_list.remove(path_to_remove)
    except (KeyError, KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        pass
    except userinput.EXCEPTION_USER_HELP:
        print(colored("You can remove any category by entering its path", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_remove(category_path_list)
    return category_path_list


def ask_save_category_path_list(favorite_path, category_path_list, favorite_name):
    favorite_dictionnary = None
    try:
        clear()
        s = favorite_name + " | " if favorite_name else ""
        s += ", ".join([f"{i+1}. {category_path_list[i]}" for i in range(len(category_path_list))])
        print(s)
        wants_to_save = userinput.ASK_CONFIRMATION("DO YOU WANT TO SAVE?", _help=True, _exit=True)
        if not wants_to_save:
            return
        favorite_dictionnary = {'name': favorite_name, 'category_path_list': category_path_list}
        mj.save_file(favorite_dictionnary, f"data/category/{favorite_path}")
    except userinput.EXCEPTION_USER_HELP:
        print(
            colored("Favorite list will be saved under data/favorite/[name]. You can enter name with / to save it under a folder.", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return ask_save_category_path_list(favorite_path, category_path_list, favorite_name)
    except KeyboardInterrupt:
        pass
    return favorite_dictionnary
