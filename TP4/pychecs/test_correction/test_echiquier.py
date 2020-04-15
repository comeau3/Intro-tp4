# -*- coding: utf-8 -*-
import pychecs
import pytest
from pychecs.echiquier import Echiquier
from pychecs.piece import Dame, Roi, Fou, Cavalier, Tour, Pion


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
def echiquier():
    x = Echiquier()
    x.dictionnaire_pieces = {
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


def test_position_est_valide(echiquier):
    assert echiquier.position_est_valide('a1')
    assert echiquier.position_est_valide('b2')
    assert echiquier.position_est_valide('c8')
    assert echiquier.position_est_valide('d2')
    assert echiquier.position_est_valide('h1')


def test_position_est_valide_hors_bornes(echiquier):
    assert not echiquier.position_est_valide('i1')
    assert not echiquier.position_est_valide('x1')
    assert not echiquier.position_est_valide('a9')
    assert not echiquier.position_est_valide('b0')


def test_position_est_valide_mauvaise_taille(echiquier):
    assert not echiquier.position_est_valide('a11')
    assert not echiquier.position_est_valide('b12')


def test_recuperer_piece_a_position_piece_presente(echiquier):
    assert echiquier.recuperer_piece_a_position('b8') == echiquier.dictionnaire_pieces['b8']
    assert echiquier.recuperer_piece_a_position('g6') == echiquier.dictionnaire_pieces['g6']
    assert echiquier.recuperer_piece_a_position('f7') == echiquier.dictionnaire_pieces['f7']


def test_recuperer_piece_a_position_piece_absente(echiquier):
    assert echiquier.recuperer_piece_a_position('c1') is None
    assert echiquier.recuperer_piece_a_position('g1') is None


def test_couleur_piece_a_position_piece_presente(echiquier):
    assert echiquier.couleur_piece_a_position('b8') == 'noir'
    assert echiquier.couleur_piece_a_position('g6') == 'noir'
    assert echiquier.couleur_piece_a_position('b1') == 'blanc'


def test_couleur_piece_a_position_piece_absente(echiquier):
    assert echiquier.couleur_piece_a_position('c1') == ''
    assert echiquier.couleur_piece_a_position('g1') == ''


def test_colonnes_entre(echiquier):
    assert echiquier.colonnes_entre('a', 'c') == ['b']
    assert echiquier.colonnes_entre('a', 'h') == ['b', 'c', 'd', 'e', 'f', 'g']
    assert echiquier.colonnes_entre('d', 'b') == ['c']
    assert echiquier.colonnes_entre('g', 'd') == ['f', 'e']


def test_colonnes_entre_vide(echiquier):
    assert echiquier.colonnes_entre('a', 'a') == []
    assert echiquier.colonnes_entre('a', 'b') == []
    assert echiquier.colonnes_entre('c', 'b') == []


def test_rangees_entre(echiquier):
    assert echiquier.rangees_entre('1', '3') == ['2']
    assert echiquier.rangees_entre('1', '8') == ['2', '3', '4', '5', '6', '7']
    assert echiquier.rangees_entre('4', '2') == ['3']
    assert echiquier.rangees_entre('7', '4') == ['6', '5']


def test_rangees_entre_vide(echiquier):
    assert echiquier.rangees_entre('1', '1') == []
    assert echiquier.rangees_entre('1', '2') == []
    assert echiquier.rangees_entre('3', '2') == []


def test_chemin_libre_entre_positions_horizontal(echiquier):
    assert echiquier.chemin_libre_entre_positions('d6', 'g6')
    assert echiquier.chemin_libre_entre_positions('g6', 'd6')
    assert echiquier.chemin_libre_entre_positions('g6', 'h6')
    assert echiquier.chemin_libre_entre_positions('h6', 'g6')
    assert not echiquier.chemin_libre_entre_positions('d6', 'h6')
    assert not echiquier.chemin_libre_entre_positions('h6', 'd6')


def test_chemin_libre_entre_positions_vertical(echiquier):
    assert echiquier.chemin_libre_entre_positions('e3', 'e8')
    assert echiquier.chemin_libre_entre_positions('e8', 'e3')
    assert echiquier.chemin_libre_entre_positions('a7', 'a6')
    assert echiquier.chemin_libre_entre_positions('a6', 'a7')
    assert not echiquier.chemin_libre_entre_positions('e2', 'e8')
    assert not echiquier.chemin_libre_entre_positions('e8', 'e2')


def test_chemin_libre_entre_positions_diagonal(echiquier):
    assert echiquier.chemin_libre_entre_positions('c2', 'd3')
    assert echiquier.chemin_libre_entre_positions('d3', 'c2')
    assert echiquier.chemin_libre_entre_positions('c2', 'e4')
    assert echiquier.chemin_libre_entre_positions('e4', 'c2')
    assert echiquier.chemin_libre_entre_positions('c2', 'f5')
    assert echiquier.chemin_libre_entre_positions('f5', 'c2')
    assert echiquier.chemin_libre_entre_positions('e3', 'c5')
    assert echiquier.chemin_libre_entre_positions('c5', 'e3')
    assert not echiquier.chemin_libre_entre_positions('b4', 'e7')
    assert not echiquier.chemin_libre_entre_positions('e7', 'b4')
    assert not echiquier.chemin_libre_entre_positions('e5', 'c7')
    assert not echiquier.chemin_libre_entre_positions('c7', 'e5')


def test_chemin_libre_entre_positions_invalide(echiquier):
    assert not echiquier.chemin_libre_entre_positions('a1', 'b7')


def test_deplacement_est_valide_standard(echiquier):
    assert echiquier.deplacement_est_valide('g2', 'g5')
    assert echiquier.deplacement_est_valide('e3', 'f5')
    assert echiquier.deplacement_est_valide('b2', 'b3')
    assert echiquier.deplacement_est_valide('d6', 'd4')


def test_deplacement_est_valide_prise(echiquier):
    assert echiquier.deplacement_est_valide('g2', 'g6')
    assert echiquier.deplacement_est_valide('d6', 'd1')
    assert echiquier.deplacement_est_valide('h8', 'h2')


def test_deplacement_valide_cavalier_saute(echiquier):
    assert echiquier.deplacement_est_valide('g6', 'e7')


def test_deplacement_invalide_chemin_pas_libre(echiquier):
    assert not echiquier.deplacement_est_valide('d1', 'd7')
    assert not echiquier.deplacement_est_valide('d1', 'g1')
    assert not echiquier.deplacement_est_valide('f1', 'f3')


def test_deplacement_invalide_prise_meme_couleur(echiquier):
    assert not echiquier.deplacement_est_valide('e3', 'd1')
    assert not echiquier.deplacement_est_valide('d6', 'g6')


def test_deplacement_invalide_pas_de_piece(echiquier):
    assert not echiquier.deplacement_est_valide('g1', 'g2')


def test_deplacement_invalide_hors_plateau(echiquier):
    assert not echiquier.deplacement_est_valide('h8', 'h9')


def test_deplacement_bouge_piece(echiquier):
    piece = echiquier.dictionnaire_pieces['g2']
    echiquier.deplacer('g2', 'g3')
    assert echiquier.dictionnaire_pieces['g3'] == piece
    assert 'g2' not in echiquier.dictionnaire_pieces


def test_deplacement_bouge_pas_piece_si_invalide(echiquier):
    piece = echiquier.dictionnaire_pieces['e3']
    echiquier.deplacer('e3', 'f3')
    assert echiquier.dictionnaire_pieces['e3'] == piece
    assert 'f3' not in echiquier.dictionnaire_pieces


def test_deplacement_retourne_true_si_ok(echiquier):
    resultat = echiquier.deplacer('g2', 'g3')
    assert isinstance(resultat, bool)
    assert resultat


def test_deplacement_retourne_false_si_pas_ok(echiquier):
    resultat = echiquier.deplacer('e3', 'f3')
    assert isinstance(resultat, bool)
    assert not resultat


def test_roi_est_dans_echiquier(echiquier):
    assert echiquier.roi_de_couleur_est_dans_echiquier('blanc')
    assert echiquier.roi_de_couleur_est_dans_echiquier('noir')


def test_roi_est_pas_dans_echiquier_noir(echiquier):
    del echiquier.dictionnaire_pieces['a8']
    assert echiquier.roi_de_couleur_est_dans_echiquier('blanc')
    assert not echiquier.roi_de_couleur_est_dans_echiquier('noir')


def test_roi_est_pas_dans_echiquier_blanc(echiquier):
    del echiquier.dictionnaire_pieces['a1']
    assert echiquier.roi_de_couleur_est_dans_echiquier('noir')
    assert not echiquier.roi_de_couleur_est_dans_echiquier('blanc')


def test_sortie_ascii(echiquier):
    pychecs.piece.UTILISER_UNICODE = False
    assert repr(echiquier) is not None


def test_sortie_unicode(echiquier):
    pychecs.piece.UTILISER_UNICODE = True
    assert repr(echiquier) is not None
