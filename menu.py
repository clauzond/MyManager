import userinput
import account
import category
import favorite
import encryption
import manipulate_json as mj
from manipulate_file import get_all_files_from
from terminal import clear
from termcolor import colored
import os


# back button -> s0, f0
# always last -> userinput.MENU_PRINT(s1, s2, ..., s0)
#             -> userinput.MENU_ASK(f1, f2, ..., f0)
#             then menu function call itself
#             in case of userinput.EXCEPTION_MENU_BACK, return

s0 = "0. Back"
def f0(*args):
    raise userinput.EXCEPTION_MENU_BACK


MAIN_JSON_PATH = "data/menu/main.json"


def main_menu():
    s1 = "1. Show main accounts"
    def f1(): return show_main_something("category")
    s2 = "2. Show main categories"
    def f2(): return show_main_something("favorite")
    s3 = "3. Show all favorites"
    def f3(): return show_all_something("favorite")
    s4 = "4. Show all categories"
    def f4(): return show_all_something("category")
    s5 = "5. Show all accounts"
    def f5(): return show_all_something("account")
    s6 = "6. Create/Modify something"
    f6 = create_something
    s7 = "7. Settings"
    f7 = show_settings
    try:
        clear()
        userinput.MENU_PRINT(s1, s2, s3, s4, s5, s6, s7, s0)
        userinput.MENU_ASK(f1, f2, f3, f4, f5, f6, f7, f0)
        main_menu()
    except userinput.EXCEPTION_MENU_BACK:
        return


def show_settings():
    s1 = "1. Change main category (account list)"
    def f1(): return change_main_something("category")
    s2 = "2. Change main favorite (category list)"
    def f2(): return change_main_something("favorite")
    s3 = "3. Change colors"
    f3 = change_colors
    s4 = "4. Change copy delay"
    f4 = change_copy_delay
    try:
        clear()
        userinput.MENU_PRINT(s1, s2, s3, s4, s0)
        userinput.MENU_ASK(f1, f2, f3, f4, f0)
        show_settings()
    except userinput.EXCEPTION_MENU_BACK:
        return

def change_colors():
    s1 = colored("1. Change help color", userinput.HELP_COLOR)
    def f1(): change_single_color("help")
    s2 = colored("2. Change question color", userinput.QUESTION_COLOR)
    def f2(): change_single_color("question")
    s3 = colored("3. Change confirmation color", userinput.CONFIRMATION_COLOR)
    def f3(): change_single_color("confirmation")
    s4 = colored("4. Change exception color", userinput.EXCEPTION_COLOR)
    def f4(): change_single_color("exception")
    s5 = colored("5. Change menu color", userinput.MENU_COLOR)
    def f5(): change_single_color("menu")
    s_0 = colored(s0, userinput.MENU_COLOR)
    try:
        clear()
        userinput.MENU_PRINT_WITHOUT_COLOR(s1, s2, s3, s4, s5, s_0)
        userinput.MENU_ASK(f1, f2, f3, f4, f5, f0)
        change_colors()
    except userinput.EXCEPTION_MENU_BACK:
        return

def change_single_color(something):
    """
    <something> may be "help", "question", "confirmation", "exception", "menu"
    """
    menu_color_dic = mj.load_file(userinput.MENU_COLOR_JSON_PATH)
    def f(new_color):
        menu_color_dic[f"{something}_color"] = new_color
        mj.save_file(menu_color_dic, userinput.MENU_COLOR_JSON_PATH)
        userinput.LOAD_COLORS()

    s1 = colored("1. Red", "red")
    f1 = lambda:f("red")
    s2 = colored("2. Green", "green")
    f2 = lambda:f("green")
    s3 = colored("3. Yellow", "yellow")
    f3 = lambda:f("yellow")
    s4 = colored("4. Blue", "blue")
    f4 = lambda:f("blue")
    s5 = colored("5. Magenta", "magenta")
    f5 = lambda:f("magenta")
    s6 = colored("6. Cyan", "cyan")
    f6 = lambda:f("cyan")
    s7 = colored("7. Grey", "grey")
    f7 = lambda:f("grey")
    s8 = colored("8. White", "white")
    f8 = lambda:f("white")
    s_0 = colored(s0, userinput.MENU_COLOR)

    s = f"This is the current {something} color."
    sentence = colored(s, userinput.MENU_COLOR)
    try:
        clear()
        print(sentence)
        userinput.MENU_PRINT_WITHOUT_COLOR(s1, s2, s3, s4, s5, s6, s7, s8, s_0)
        userinput.MENU_ASK(f1, f2, f3, f4, f5, f6, f7, f8, f0)
        change_single_color(something)
    except userinput.EXCEPTION_MENU_BACK:
        return


def change_copy_delay():
    main_json = mj.load_file(MAIN_JSON_PATH)
    cur_delay = int(main_json['delay'])
    s = f"Current delay: {cur_delay}s"
    sentence = colored(s, userinput.MENU_COLOR)
    try:
        clear()
        print(sentence)
        question = "ENTER DELAY (in seconds)"
        delay_input = userinput.ASK_QUESTION(question, _help=True, _exit=True)
        if delay_input.isnumeric() and int(delay_input)>0 and int(delay_input) != cur_delay:
            main_json['delay'] = int(delay_input)
            mj.save_file(main_json, MAIN_JSON_PATH)
            print(colored(f"Delay changed to {int(delay_input)}s", userinput.MENU_COLOR))
            userinput.ASK_CONTINUE()
            return
        elif delay_input.isnumeric() and int(delay_input) == cur_delay:
            print(colored("Delay unchanged", userinput.MENU_COLOR))
            userinput.ASK_CONTINUE()
            return
        else:
            return
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        return
    except userinput.EXCEPTION_USER_HELP:
        print(colored("Delay (in second) between each copy of account's main fields", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return change_copy_delay()


def show_main_something(something):
    """
    <something> may be "category", "favorite"
    """
    something_path = mj.load_file(MAIN_JSON_PATH)[something]
    if not something_path:
        return
    something_dic = mj.load_file(f"data/{something}/{something_path}")
    if something == "category":
        show_category(something_dic)
    elif something == "favorite":
        show_favorite(something_dic)
    else:
        return


def create_something():
    s1 = "1. Create/Modify account"
    f1 = account.ask_create_account
    s2 = "2. Create/Modify category"
    f2 = category.ask_create_category
    s3 = "3. Create/Modify favorite"
    f3 = favorite.ask_create_favorite
    try:
        clear()
        userinput.MENU_PRINT(s1, s2, s3, s0)
        userinput.MENU_ASK(f1, f2, f3, f0)
        create_something()
    except userinput.EXCEPTION_MENU_BACK:
        return


def show_all_something(something):
    """
    Show all <something> available in data folder (<something> may be "account", "category" or "favorite")
    User may choose any of them to show its details
    """
    if something == "account":
        def show_something(dic): return show_account(dic)
    elif something == "category":
        def show_something(dic): return show_category(dic)
    elif something == "favorite":
        def show_something(dic): return show_favorite(dic)
    i = 0
    s_list = []
    f_list = []
    something_list = []
    path_list = get_all_files_from(f"data/{something}")
    for rel_path in path_list:
        path = f"data/{something}/{rel_path}"
        something_dic = mj.load_file(path)
        something_list.append(something_dic)
        s_i = f"{i+1}. {something_dic['name']} ({rel_path})"
        if something == "account":
            s_i += " (PROTECTED)" if something_dic['is_protected'] else ""
        s_list.append(s_i)
        def f_i(k): return show_something(something_list[k])
        f_list.append(f_i)
        i += 1

    s_list.append(s0)
    f_list.append(f0)
    try:
        clear()
        userinput.MENU_PRINT(*s_list)
        userinput.MENU_ASK_WITH_PARAMETERS(*f_list)
        show_all_something(something)
    except userinput.EXCEPTION_MENU_BACK:
        return


def show_account(account_dic, encryption_key=None, show_values=False):
    if account_dic['is_protected']:
        if encryption_key is None:
            try:
                encryption_key = userinput.ASK_QUESTION("ENTER PASSWORD")
                if not encryption.verify_hash(encryption_key, account_dic['hash']):
                    raise ValueError
                show_values = userinput.ASK_CONFIRMATION("SHOW FIELD VALUES?")
            except (ValueError, KeyboardInterrupt):
                return
        clear_dictionnary = encryption.decrypt_dictionnary(dict(account_dic['field_dictionnary']), encryption_key)
        if not show_values:
            field_dictionnary = account.bleep_dictionnary(dict(clear_dictionnary))
        else:
            field_dictionnary = clear_dictionnary
    else:
        field_dictionnary = account_dic['field_dictionnary']
        clear_dictionnary = field_dictionnary

    s = colored(account_dic['name'], userinput.HELP_COLOR) + "\n"
    for key in field_dictionnary:
        s += f"{key}: {field_dictionnary[key]}"
        if key in account_dic['list_to_copy']:
            s += " [COPY]"
        s += "\n"

    delay = int(mj.load_file(MAIN_JSON_PATH)['delay'])
    s1 = f"1. Copy main fields ({delay}s delay)"
    def f1(): return account.copy_main_fields(account_dic['list_to_copy'], clear_dictionnary, delay)

    try:
        clear()
        print(s, end="")
        userinput.MENU_PRINT(s1, s0)
        userinput.MENU_ASK(f1, f0)
        show_account(account_dic, encryption_key, show_values)
    except userinput.EXCEPTION_MENU_BACK:
        return


def show_category(category_dic):
    s = colored(category_dic['name'], userinput.HELP_COLOR) + "\n"
    s_list = []
    f_list = []
    account_list = []
    i = 0
    for rel_path in category_dic['account_path_list']:
        account_dic = mj.load_file(f"data/account/{rel_path}")
        account_list.append(account_dic)
        s_i = f"{i+1}. {account_dic['name']} ({rel_path})"
        s_i += " (PROTECTED)" if account_dic['is_protected'] else ""
        s_list.append(s_i)
        def f_i(k): return show_account(account_list[k])
        f_list.append(f_i)
        i += 1
    s_list.append(s0)
    f_list.append(f0)

    try:
        clear()
        print(s, end="")
        userinput.MENU_PRINT(*s_list)
        userinput.MENU_ASK_WITH_PARAMETERS(*f_list)
        show_category(category_dic)
    except userinput.EXCEPTION_MENU_BACK:
        return


def show_favorite(favorite_dic):
    s = colored(favorite_dic['name'], userinput.HELP_COLOR) + "\n"
    s_list = []
    f_list = []
    category_list = []
    i = 0
    for rel_path in favorite_dic['category_path_list']:
        category_dic = mj.load_file(f"data/category/{rel_path}")
        category_list.append(category_dic)
        s_i = f"{i+1}. {category_dic['name']} ({rel_path})"
        s_i += " (PROTECTED)" if category_dic['is_protected'] else ""
        s_list.append(s_i)
        def f_i(k): return show_category(category_list[k])
        f_list.append(f_i)
        i += 1
    s_list.append(s0)
    f_list.append(f0)

    try:
        clear()
        print(s, end="")
        userinput.MENU_PRINT(*s_list)
        userinput.MENU_ASK_WITH_PARAMETERS(*f_list)
        show_category(favorite_dic)
    except userinput.EXCEPTION_MENU_BACK:
        return


LIST_FILES_COMMAND = userinput.GET_FILES_LIST


def change_main_something(something, do_clear=True):
    """
    <something> may be "category", "favorite"
    """
    if do_clear:
        clear()
    try:
        main_json = mj.load_file(MAIN_JSON_PATH)
        cur_main = main_json[something]
        s = f"Current main {something} is: {cur_main}"
        print(s)
        question = f"ENTER PATH FOR YOUR {something.upper()}"
        something_path = userinput.ASK_QUESTION(question, _help=True, _exit=True)
        if something_path in LIST_FILES_COMMAND:
            print(", ".join(get_all_files_from(f"data/{something}")))
            userinput.ASK_CONTINUE()
            return change_main_something(something, do_clear=False)
        if not (len(something_path) > 5 and something_path[-5:] == ".json"):
            something_path += ".json"
        full_path = f"data/{something}/{something_path}"
        if os.path.isfile(full_path):
            question = "ARE YOU SURE TO SET THIS TO MAIN?"
            try:
                wants_main = userinput.ASK_CONFIRMATION(question)
            except KeyboardInterrupt:
                return
            if wants_main:
                main_json[something] = something_path
                mj.save_file(main_json, MAIN_JSON_PATH)
                return
            else:
                return
    except (KeyboardInterrupt, userinput.EXCEPTION_USER_EXIT):
        return
    except userinput.EXCEPTION_USER_HELP:
        print(colored(f"Enter the path name of your {something} list", userinput.HELP_COLOR))
        print(colored(f"LIST ALL {something.upper()}: {', '.join(LIST_FILES_COMMAND)}", userinput.HELP_COLOR))
        userinput.PRINT_HELP()
        userinput.PRINT_EXIT()
        userinput.ASK_CONTINUE()
        return change_main_something(something, do_clear=False)

if __name__=="__main__":
    main_menu()