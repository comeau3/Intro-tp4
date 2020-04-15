# -*- coding: utf-8 -*-
import pychecs
import pytest
from pychecs.piece import Piece, Dame, Roi, Fou, Cavalier, Tour, Pion


def test_couleur():
    piece = Piece('noir', True)
    assert piece.est_noir()

    piece = Piece('blanc', False)
    assert piece.est_blanc()


def test_mouvement_piece():
    piece = Piece('blanc', True)
    with pytest.raises(NotImplementedError):
        piece.peut_se_deplacer_vers('a2', 'c3')


def test_mouvements_pion():
    pion = Pion('blanc')
    assert pion.peut_se_deplacer_vers('b2', 'b3')
    assert not pion.peut_se_deplacer_vers('b2', 'c3')
    assert not pion.peut_se_deplacer_vers('c2', 'c1')

    pion = Pion('noir')
    assert not pion.peut_se_deplacer_vers('b2', 'b3')
    assert not pion.peut_se_deplacer_vers('b3', 'c2')
    assert pion.peut_se_deplacer_vers('c2', 'c1')


def test_mouvements_pion_deplacement_depart():
    pion = Pion('blanc')
    assert pion.peut_se_deplacer_vers('b2', 'b4')
    assert pion.peut_se_deplacer_vers('g2', 'g4')
    assert not pion.peut_se_deplacer_vers('b2', 'b5')
    assert not pion.peut_se_deplacer_vers('c3', 'c5')

    pion = Pion('noir')
    assert not pion.peut_se_deplacer_vers('b2', 'b4')
    assert pion.peut_se_deplacer_vers('b7', 'b5')
    assert pion.peut_se_deplacer_vers('h7', 'h5')
    assert not pion.peut_se_deplacer_vers('d7', 'd4')
    assert not pion.peut_se_deplacer_vers('d8', 'd6')


def test_prises_pion():
    pion = Pion('blanc')
    assert pion.peut_faire_une_prise_vers('b2', 'c3')
    assert pion.peut_faire_une_prise_vers('b2', 'a3')
    assert not pion.peut_faire_une_prise_vers('b2', 'b3')
    assert not pion.peut_faire_une_prise_vers('c2', 'c1')

    pion = Pion('noir')
    assert not pion.peut_faire_une_prise_vers('b2', 'c3')
    assert not pion.peut_faire_une_prise_vers('b2', 'a3')
    assert pion.peut_faire_une_prise_vers('b3', 'c2')
    assert not pion.peut_faire_une_prise_vers('c2', 'c1')


def test_mouvements_tour():
    tour = Tour('blanc')
    assert tour.peut_se_deplacer_vers('c4', 'd4')
    assert tour.peut_se_deplacer_vers('c4', 'h4')
    assert tour.peut_se_deplacer_vers('h4', 'c4')
    assert tour.peut_se_deplacer_vers('h4', 'h7')
    assert tour.peut_se_deplacer_vers('h7', 'h4')
    assert not tour.peut_se_deplacer_vers('c4', 'd5')
    assert not tour.peut_se_deplacer_vers('c4', 'd6')


def test_prises_tour():
    tour = Tour('blanc')
    assert tour.peut_faire_une_prise_vers('c4', 'd4')
    assert tour.peut_faire_une_prise_vers('c4', 'h4')
    assert tour.peut_faire_une_prise_vers('h4', 'c4')
    assert tour.peut_faire_une_prise_vers('h4', 'h7')
    assert tour.peut_faire_une_prise_vers('h7', 'h4')
    assert not tour.peut_faire_une_prise_vers('c4', 'd5')
    assert not tour.peut_faire_une_prise_vers('c4', 'd6')


def test_mouvements_fou():
    fou = Fou('blanc')
    assert fou.peut_se_deplacer_vers('c1', 'd2')
    assert fou.peut_se_deplacer_vers('d2', 'c1')
    assert fou.peut_se_deplacer_vers('c1', 'e3')
    assert fou.peut_se_deplacer_vers('e3', 'c1')
    assert fou.peut_se_deplacer_vers('c1', 'h6')
    assert fou.peut_se_deplacer_vers('h6', 'c1')
    assert fou.peut_se_deplacer_vers('c1', 'a3')
    assert fou.peut_se_deplacer_vers('a3', 'c1')

    assert not fou.peut_se_deplacer_vers('a1', 'a2')
    assert not fou.peut_se_deplacer_vers('a1', 'a5')
    assert not fou.peut_se_deplacer_vers('a1', 'h1')


def test_prises_fou():
    fou = Fou('blanc')
    assert fou.peut_faire_une_prise_vers('c1', 'd2')
    assert fou.peut_faire_une_prise_vers('d2', 'c1')
    assert fou.peut_faire_une_prise_vers('c1', 'e3')
    assert fou.peut_faire_une_prise_vers('e3', 'c1')
    assert fou.peut_faire_une_prise_vers('c1', 'h6')
    assert fou.peut_faire_une_prise_vers('h6', 'c1')
    assert fou.peut_faire_une_prise_vers('c1', 'a3')
    assert fou.peut_faire_une_prise_vers('a3', 'c1')

    assert not fou.peut_faire_une_prise_vers('a1', 'a2')
    assert not fou.peut_faire_une_prise_vers('a1', 'a5')
    assert not fou.peut_faire_une_prise_vers('a1', 'h1')


def test_mouvements_dame():
    dame = Dame('blanc')
    assert dame.peut_se_deplacer_vers('c4', 'd4')
    assert dame.peut_se_deplacer_vers('c4', 'h4')
    assert dame.peut_se_deplacer_vers('h4', 'c4')
    assert dame.peut_se_deplacer_vers('h4', 'h7')
    assert dame.peut_se_deplacer_vers('h7', 'h4')
    assert dame.peut_se_deplacer_vers('c1', 'd2')
    assert dame.peut_se_deplacer_vers('d2', 'c1')
    assert dame.peut_se_deplacer_vers('c1', 'e3')
    assert dame.peut_se_deplacer_vers('e3', 'c1')
    assert dame.peut_se_deplacer_vers('c1', 'h6')
    assert dame.peut_se_deplacer_vers('h6', 'c1')
    assert dame.peut_se_deplacer_vers('c1', 'a3')
    assert dame.peut_se_deplacer_vers('a3', 'c1')
    assert not dame.peut_se_deplacer_vers('d4', 'f5')
    assert not dame.peut_se_deplacer_vers('d4', 'a3')


def test_prises_dame():
    dame = Dame('blanc')
    assert dame.peut_faire_une_prise_vers('c4', 'd4')
    assert dame.peut_faire_une_prise_vers('c4', 'h4')
    assert dame.peut_faire_une_prise_vers('h4', 'c4')
    assert dame.peut_faire_une_prise_vers('h4', 'h7')
    assert dame.peut_faire_une_prise_vers('h7', 'h4')
    assert dame.peut_faire_une_prise_vers('c1', 'd2')
    assert dame.peut_faire_une_prise_vers('d2', 'c1')
    assert dame.peut_faire_une_prise_vers('c1', 'e3')
    assert dame.peut_faire_une_prise_vers('e3', 'c1')
    assert dame.peut_faire_une_prise_vers('c1', 'h6')
    assert dame.peut_faire_une_prise_vers('h6', 'c1')
    assert dame.peut_faire_une_prise_vers('c1', 'a3')
    assert dame.peut_faire_une_prise_vers('a3', 'c1')
    assert not dame.peut_faire_une_prise_vers('d4', 'f5')
    assert not dame.peut_faire_une_prise_vers('d4', 'a3')


def test_mouvements_roi():
    roi = Roi('blanc')
    assert roi.peut_se_deplacer_vers('d3', 'c2')
    assert roi.peut_se_deplacer_vers('d3', 'c3')
    assert roi.peut_se_deplacer_vers('d3', 'c4')
    assert roi.peut_se_deplacer_vers('d3', 'd4')
    assert roi.peut_se_deplacer_vers('d3', 'd2')
    assert roi.peut_se_deplacer_vers('d3', 'e2')
    assert roi.peut_se_deplacer_vers('d3', 'e3')
    assert roi.peut_se_deplacer_vers('d3', 'e4')
    assert not roi.peut_se_deplacer_vers('d3', 'd5')
    assert not roi.peut_se_deplacer_vers('d3', 'f3')


def test_prises_roi():
    roi = Roi('blanc')
    assert roi.peut_faire_une_prise_vers('d3', 'c2')
    assert roi.peut_faire_une_prise_vers('d3', 'c3')
    assert roi.peut_faire_une_prise_vers('d3', 'c4')
    assert roi.peut_faire_une_prise_vers('d3', 'd4')
    assert roi.peut_faire_une_prise_vers('d3', 'd2')
    assert roi.peut_faire_une_prise_vers('d3', 'e2')
    assert roi.peut_faire_une_prise_vers('d3', 'e3')
    assert roi.peut_faire_une_prise_vers('d3', 'e4')
    assert not roi.peut_faire_une_prise_vers('d3', 'd5')
    assert not roi.peut_faire_une_prise_vers('d3', 'f3')


def test_mouvements_cavalier():
    cavalier = Cavalier('blanc')
    assert cavalier.peut_se_deplacer_vers('e4', 'c3')
    assert cavalier.peut_se_deplacer_vers('e4', 'c5')
    assert cavalier.peut_se_deplacer_vers('e4', 'd2')
    assert cavalier.peut_se_deplacer_vers('e4', 'd6')
    assert cavalier.peut_se_deplacer_vers('e4', 'f2')
    assert cavalier.peut_se_deplacer_vers('e4', 'f6')
    assert cavalier.peut_se_deplacer_vers('e4', 'g3')
    assert cavalier.peut_se_deplacer_vers('e4', 'g5')

    assert not cavalier.peut_se_deplacer_vers('e4', 'c4')
    assert not cavalier.peut_se_deplacer_vers('e4', 'd5')
    assert not cavalier.peut_se_deplacer_vers('e4', 'a5')


def test_prises_cavalier():
    cavalier = Cavalier('blanc')
    assert cavalier.peut_faire_une_prise_vers('e4', 'c3')
    assert cavalier.peut_faire_une_prise_vers('e4', 'c5')
    assert cavalier.peut_faire_une_prise_vers('e4', 'd2')
    assert cavalier.peut_faire_une_prise_vers('e4', 'd6')
    assert cavalier.peut_faire_une_prise_vers('e4', 'f2')
    assert cavalier.peut_faire_une_prise_vers('e4', 'f6')
    assert cavalier.peut_faire_une_prise_vers('e4', 'g3')
    assert cavalier.peut_faire_une_prise_vers('e4', 'g5')

    assert not cavalier.peut_faire_une_prise_vers('e4', 'e4')
    assert not cavalier.peut_faire_une_prise_vers('e4', 'c4')
    assert not cavalier.peut_faire_une_prise_vers('e4', 'd5')
    assert not cavalier.peut_faire_une_prise_vers('e4', 'a5')


def test_deplacements_sur_place_interdits():
    pion = Pion('blanc')
    tour = Tour('noir')
    fou = Fou('blanc')
    dame = Dame('blanc')
    roi = Roi('noir')
    cavalier = Cavalier('blanc')
    assert not pion.peut_se_deplacer_vers('d3', 'd3')
    assert not pion.peut_faire_une_prise_vers('c2', 'c2')
    assert not tour.peut_se_deplacer_vers('c4', 'c4')
    assert not tour.peut_faire_une_prise_vers('d5', 'd5')
    assert not fou.peut_se_deplacer_vers('c5', 'c5')
    assert not fou.peut_faire_une_prise_vers('a1', 'a1')
    assert not dame.peut_se_deplacer_vers('d2', 'd2')
    assert not dame.peut_faire_une_prise_vers('d4', 'd4')
    assert not roi.peut_se_deplacer_vers('d3', 'd3')
    assert not roi.peut_faire_une_prise_vers('d3', 'd3')
    assert not cavalier.peut_se_deplacer_vers('e4', 'e4')
    assert not cavalier.peut_faire_une_prise_vers('f4', 'f4')


def test_representations_differentes_ascii():
    pychecs.piece.UTILISER_UNICODE = False
    pieces = [Pion('blanc'), Pion('noir'), Tour('blanc'), Tour('noir'), Cavalier('blanc'), Cavalier('noir'),
              Fou('blanc'), Fou('noir'), Dame('blanc'), Dame('noir'), Roi('blanc'), Roi('noir')]

    representations = [str(piece) for piece in pieces]
    assert len(representations) == len(set(representations))


def test_representations_differentes_unicode():
    pychecs.piece.UTILISER_UNICODE = True
    pieces = [Pion('blanc'), Pion('noir'), Tour('blanc'), Tour('noir'), Cavalier('blanc'), Cavalier('noir'),
              Fou('blanc'), Fou('noir'), Dame('blanc'), Dame('noir'), Roi('blanc'), Roi('noir')]

    representations = [str(piece) for piece in pieces]
    assert len(representations) == len(set(representations))
