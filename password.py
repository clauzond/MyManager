class Password:
    def __init__(self, parent_account = None, hash = None, crypted = None):
        if hash:
            self.hash = hash
        elif crypted:
            self.crypted = crypted

        if parent_account:
            self.parent_account = parent_account