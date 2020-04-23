# -*- coding: utf-8 -*-
"""Module principal du package pychecs2. C'est ce module que nous allons exécuter pour démarrer votre jeu.
Importez les modules nécessaires et démarrez votre programme à partir d'ici. Le code fourni n'est qu'à titre d'exemple.

"""
from pychecs2.echecs.partie import Partie
from pychecs2.interface.exemple import Fenetre

if __name__ == '__main__':
    # Création d'une instance de Partie.
    p = Partie()

    # Affichage de l'échiquier dans cette partie.
    print(p.echiquier)

    # Création et affichage d'une fenêtre (aucun lien avec la partie ci-haut).
    Fenetre().mainloop()

    #effacercetteligneapreslecommitsvp
    #pourquoicacommitpas
