import os

def get_all_files_from(folder="data/account"):
    """ Folder should be a string like "data/category" or "data/account"
    """
    l = []
    for path, subdirs, files in os.walk(folder):
        for name in files:
            l.append(os.path.join(path, name)[len(folder)+1:].replace("\\", "/"))
    return l