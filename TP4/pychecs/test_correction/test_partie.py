# -*- coding: utf-8 -*-
from pychecs.partie import Partie
from pychecs.piece import Dame, Roi, Fou, Cavalier, Tour, Pion
import pytest


# Échiquier de test :
#
#   +----+----+----+----+----+----+----+----+
# 8 | RN | PN |    |    |    |    |    | TN |
#   +----+----+----+----+----+----+----+----+
# 7 | PN | PN |    |    |    | FN |    |    |
#   +----+----+----+----+----+----+----+----+
# 6 |    |    |    | DN |    |    | CN |    |
#   +----+----+----+----+----+----+----+----+
# 5 |    |    |    |    |    |    |    |    |
#   +----+----+----+----+----+----+----+----+
# 4 |    |    |    |    |    |    |    |    |
#   +----+----+----+----+----+----+----+----+
# 3 |    |    |    |    | CB |    |    |    |
#   +----+----+----+----+----+----+----+----+
# 2 | PB | PB |    |    |    |    | TB | PB |
#   +----+----+----+----+----+----+----+----+
# 1 | RB | PB |    | DB |    | FB |    |    |
#   +----+----+----+----+----+----+----+----+
#     a    b    c    d    e    f    g    h
#


@pytest.fixture()
def partie():
    x = Partie()
    x.echiquier.dictionnaire_pieces = {
        'a8': Roi('noir'),
        'a7': Pion('noir'),
        'b7': Pion('noir'),
        'b8': Pion('noir'),
        'a1': Roi('blanc'),
        'a2': Pion('blanc'),
        'b2': Pion('blanc'),
        'b1': Pion('blanc'),
        'd1': Dame('blanc'),
        'f1': Fou('blanc'),
        'e3': Cavalier('blanc'),
        'g2': Tour('blanc'),
        'h2': Pion('blanc'),
        'b7': Pion('noir'),
        'd6': Dame('noir'),
        'f7': Fou('noir'),
        'g6': Cavalier('noir'),
        'h8': Tour('noir'),
    }
    return x


def test_determiner_gagnant_aucun(partie):
    assert partie.determiner_gagnant() == 'aucun'


def test_determiner_gagnang_noir(partie):
    del partie.echiquier.dictionnaire_pieces['a1']
    assert partie.determiner_gagnant() == 'noir'


def test_determiner_gagnang_blanc(partie):
    del partie.echiquier.dictionnaire_pieces['a8']
    assert partie.determiner_gagnant() == 'blanc'


def test_partie_terminee_pas_terminee(partie):
    assert not partie.partie_terminee()


def test_partie_terminee_blanc(partie):
    del partie.echiquier.dictionnaire_pieces['a1']
    assert partie.partie_terminee()


def test_partie_terminee_noir(partie):
    del partie.echiquier.dictionnaire_pieces['a8']
    assert partie.partie_terminee()


def test_alterner_joueurs(partie):
    joueur_actif = partie.joueur_actif
    partie.joueur_suivant()
    assert joueur_actif != partie.joueur_actif
    partie.joueur_suivant()
    assert joueur_actif == partie.joueur_actif
