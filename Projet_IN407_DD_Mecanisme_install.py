# Mécanisme d'installation du Projet IN407

import subprocess
import sys

# On initialise la liste des modules à installer 
liste_modules = ['customtkinter']

def install_modules(liste):
    for module in liste:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# Installation des modules nécessaires
if __name__ == '__main__':
    install_modules(liste_modules)

# Les modules 'time', 'random' et 'threading' font partis de la bibliothèque standard de python 
# Leur version est donc dépendante de l'interpréteur Python 

version_python = sys.version.split()[0] # On récupère la version de l'interpréteur python 
version_python = tuple(int(nb) for nb in version_python.split('.')) # On converti le 'str' en tuple de 'int'
assert version_python >= (3,9,10), "Votre interpréteur python étant une ancienne version peut provoquer des erreurs avec l'application."