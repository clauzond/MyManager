# coding: utf-8
import json
import os


def load_file(filedir):
    """
    Renvoie le contenu du ficher
    """
    with open(filedir, 'r', encoding='utf-8-sig') as filein:
        data = json.load(filein)
        filein.close()
        return data


def save_file(data, filedir):
    """
    Sauvegarde le contenu du ficher et ne renvoie rien
    """
    directory = "/".join(filedir.split('/')[:-1])
    if not os.path.exists(directory):
        os.mkdir(directory)
    with open(filedir, 'w+', encoding='utf-8-sig') as fileout:
        json.dump(data, fileout, ensure_ascii=False)
        fileout.close()
