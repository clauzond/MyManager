# coding: utf-8
import json
import os


def load_file(filedir):
    """ Renvoie le contenu du ficher
    """
    with open(filedir, 'r', encoding='utf-8-sig') as filein:
        data = json.load(filein)
        filein.close()
        return data


def save_file(data, filedir):
    """ Sauvegarde le contenu du ficher et ne renvoie rien
    """
    create_directory(filedir)
    with open(filedir, 'w+', encoding='utf-8-sig') as fileout:
        json.dump(data, fileout, ensure_ascii=False, sort_keys=True, indent=4)
        fileout.close()


def create_directory(filedir):
    """ Créer le répertoire qui contient le fichier
    """
    directory_list = filedir.split('/')[:-1]

    current_list = []
    for directory in directory_list:
        current_list.append(directory)
        dir_to_create = "/".join(current_list)
        if not os.path.exists(dir_to_create):
            os.mkdir(dir_to_create)
