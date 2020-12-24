import userinput
import account
import category
import favorite
from terminal import clear
import os

# back button -> s0, f0
# always last -> userinput.MENU_PRINT(s1, s2, ..., s0)
#             -> userinput.MENU_ASK(f1, f2, ..., f0)
#             then menu function call itself
#             in case of userinput.EXCEPTION_MENU_BACK, return

def create_something():
    s1 = "1. Create account"
    f1 = account.ask_create_account
    s2 = "2. Create category"
    f2 = category.ask_create_category
    s3 = "3. Create favorite"
    f3 = favorite.ask_create_favorite
    s0 = "0. Back"
    def f0():
        raise userinput.EXCEPTION_MENU_BACK
    try:
        userinput.MENU_PRINT(s1, s2, s3, s0)
        userinput.MENU_ASK(f1, f2, f3, f0)
        create_something()
    except userinput.EXCEPTION_MENU_BACK:
        return

def show_account(account_path):
    ...

def show_category(category_path):
    ...

def show_favorite(favorite_path):
    ...