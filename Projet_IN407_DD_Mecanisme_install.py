# Mécanisme d'installation du Projet IN407

from setuptools import setup, find_packages

setup(
    name='Projet_IN407_DD',
    version='1.0',
    packages=find_packages(),
    scripts=['Projet_IN407_Desmares_Desfontaines.py'],
    install_requires=[
        'time', 'random', 'threading', 'os', 'platform', 'subprocess'
    ],
    entry_points={
        'console_scripts': [
            'nom_de_commande = Projet_IN407_Desmares_Desfontaines:fonction_principale',
        ]
    },
    author='Loïc Desmares - Alexia Desfontaines',
    author_email='',
    description="Projet_IN407_DD est une application permettant de comparer des stratégies de gestion de flux de données au sein d'un réseau.",
    url='https://github.com/LugolBis/Projet-IN407/tree/main',
)