import manipulate_json as mj
from userinput import ASK_USER, USER_QUIT, USER_REMOVE
from terminal import clear

def create_account():
    account_dictionnary = {}
    while True:
        try:
            clear()
            wrote_yet = ", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary])
            if wrote_yet:
                print(wrote_yet)
            key = ASK_USER("NAME?")
            value = ASK_USER("VALUE?")
            account_dictionnary[key] = value
            print(", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary]))
        except (USER_QUIT, KeyboardInterrupt):
            print("")
            break
        except USER_REMOVE:
            try:
                clear()
                wrote_yet = ", ".join([f"{key}: {account_dictionnary[key]}" for key in account_dictionnary])
                if wrote_yet:
                    print(wrote_yet)
                key_to_remove = ASK_USER("WHICH KEY TO REMOVE?")
                account_dictionnary.pop(key_to_remove, None)
                continue
            except (USER_QUIT, KeyboardInterrupt):
                print("")
                break
            except:
                continue
    return account_dictionnary

if __name__ == "__main__":
    print(create_account())