# -*- coding: utf-8 -*-
"""Module principal du package pychecs. C'est ce module que nous allons exécuter pour démarrer votre jeu.

"""
from pychecs.partie import Partie

if __name__ == '__main__':
    # Création d'une instance de Partie.
    p = Partie()

    # Exemple de modification du dictionnaire de pièces, afin de débuter une partie simplifiée pour faire
    # vos tests. Vous devez importer les pièces appropriés pour que ce code fonctionne.
    # p.echiquier.dictionnaire_pieces = {
    #     'b1': Roi('noir'),
    #     'c4': Fou('noir'),
    #     'b8': Tour('blanc'),
    #     'g7': Roi('blanc')
    # }

    # Démarrage de cette partie.
    p.jouer()
