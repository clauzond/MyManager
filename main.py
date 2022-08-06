import pip


def import_necessary():
    __import__("Crypto.Cipher")
    __import__("hashlib")
    __import__("pyperclip")
    __import__("termcolor")
    __import__("pyautogui")


if __name__ == "__main__":
    try:
        import menu
        import_necessary()
    except (ImportError, ModuleNotFoundError):
        pip.main(["install", "-r", "requirements.txt"])

    import menu
    menu.main_menu()
