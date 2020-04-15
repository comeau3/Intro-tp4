# -*- coding: utf-8 -*-
"""Module contenant la classe de base Piece, ainsi qu'une classe fille pour chacun des types de pièces du jeu d'échecs.

"""
# TODO: Si votre système n'affiche pas correctement les caractères unicodes du jeu d'échecs,
# mettez cette constante (variable globale) à False. Un tutoriel est présent sur le site Web
# du cours pour vous aider à faire fonctionner les caractères Unicoe sous Windows.
UTILISER_UNICODE = True


class Piece:
    """Une classe de base représentant une pièce du jeu d'échecs. C'est cette classe qui est héritée plus bas pour fournir
    une classe par type de pièce (Pion, Tour, etc.).

    Attributes:
        couleur (str): La couleur de la pièce, soit 'blanc' ou 'noir'.
        peut_sauter (bool): Si oui ou non la pièce peut "sauter" par dessus d'autres pièces sur un échiquier.

    Args:
        couleur (str): La couleur avec laquelle créer la pièce.
        peut_sauter (bool): La valeur avec laquelle l'attribut peut_sauter doit être initialisé.

    """
    def __init__(self, couleur, peut_sauter):
        # Validation si la couleur reçue est valide.
        assert couleur in ('blanc', 'noir')

        # Création des attributs avec les valeurs reçues.
        self.couleur = couleur
        self.peut_sauter = peut_sauter

    def est_blanc(self):
        """Retourne si oui ou non la pièce est blanche.

        Returns:
            bool: True si la pièce est blanche, et False autrement.

        """
        return self.couleur == 'blanc'

    def est_noir(self):
        """Retourne si oui ou non la pièce est noire.

        Returns:
            bool: True si la pièce est noire, et False autrement.

        """
        return self.couleur == 'noir'

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Warning:
            Comme nous sommes dans la classe de base et non dans l'une des classes filles, nous ne savons pas
            (encore) comment cette pièce se déplace. Cette méthode est donc à redéfinir dans chacune des
            classes filles.

        Warning:
            Comme la classe Piece est indépendante de l'échiquier (et donc on ne sait pas si une pièce est "dans le
            chemin"), on doit ignorer le contenu de l'échiquier : on ne se concentre que sur les règles de mouvement
            des pièces.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """
        # On lance une exception (on y reviendra) indiquant que ce code n'a pas été implémenté. Ne touchez pas
        # à cette méthode : réimplémentez-la dans les classes filles!
        raise NotImplementedError

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.
        Pour la plupart des pièces, la règle est la même, on appelle donc la méthode peut_se_deplacer_vers.

        Si ce n'est pas le cas pour une certaine pièce, on peut simplement redéfinir cette méthode pour programmer
        la règle.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """
        return self.peut_se_deplacer_vers(position_source, position_cible)


class Pion(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        colonne_source, colonne_cible = ord(position_source[0]), ord(position_cible[0])
        rangee_source, rangee_cible = int(position_source[1]), int(position_cible[1])

        # Un pion se déplace sur une même colonne.
        if colonne_cible != colonne_source:
            return False

        # Si le pion n'a jamais bougé, il peut bouger de deux cases. Sinon, seulement d'une case.
        # Notez que c'est ici le seul endroit où nous faisons référence à la taille de l'échiquier.
        # Pour rendre nos classes de pièces vraiment indépendantes de cette taille, nous pourrions
        # par exemple ajouter un attribut n_deplacements, qui sera incrémenté si la pièce se
        # déplace.
        difference = rangee_source - rangee_cible
        if self.est_blanc():
            if rangee_source == 2:
                return difference in (-1, -2)
            else:
                return difference == -1

        else:
            if rangee_source == 7:
                return difference in (1, 2)
            else:
                return difference == 1

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        colonne_source, colonne_cible = ord(position_source[0]), ord(position_cible[0])
        rangee_source, rangee_cible = int(position_source[1]), int(position_cible[1])

        # Le pion fait une prise en diagonale, d'une case seulement, et la direction dépend
        # de sa couleur.
        if colonne_cible not in (colonne_source - 1, colonne_source + 1):
            return False

        if self.est_blanc():
            return rangee_cible == rangee_source + 1

        else:
            return rangee_cible == rangee_source - 1

    def __repr__(self):
        """Redéfinit comment on affiche un pion à l'écran. Nous utilisons la constante UTILISER_UNICODE
        pour déterminer comment afficher le pion.

        Returns:
            str: La chaîne de caractères représentant le pion.

        """
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2659'
            else:
                return 'PB'
        else:
            if UTILISER_UNICODE:
                return '\u265f'
            else:
                return 'PN'


class Tour(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        colonne_source, colonne_cible = position_source[0], position_cible[0]
        rangee_source, rangee_cible = position_source[1], position_cible[1]

        # Une tour se déplace sur une même rangée ou une même ligne, peu importe la direction.
        if colonne_cible != colonne_source and rangee_source != rangee_cible:
            return False

        # Par contre, elle ne peut pas rester sur place.
        if colonne_source == colonne_cible and rangee_source == rangee_cible:
            return False

        return True

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2656'
            else:
                return 'TB'
        else:
            if UTILISER_UNICODE:
                return '\u265c'
            else:
                return 'TN'


class Cavalier(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, True)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        colonne_source, colonne_cible = ord(position_source[0]), ord(position_cible[0])
        rangee_source, rangee_cible = int(position_source[1]), int(position_cible[1])

        # Un cavalier se déplace en "L", alors l'une de ses coordonnées soit varier de 1, et l'autre de 2.
        distance_colonne = abs(colonne_source - colonne_cible)
        distance_rangee = abs(rangee_source - rangee_cible)

        if distance_colonne == 1 and distance_rangee == 2:
            return True

        if distance_colonne == 2 and distance_rangee == 1:
            return True

        return False

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2658'
            else:
                return 'CB'
        else:
            if UTILISER_UNICODE:
                return '\u265e'
            else:
                return 'CN'


class Fou(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        # Un fou se déplace en diagonale, c'est à dire, la distance entre les rangées et colonnes doit être la même.
        colonne_source, colonne_cible = ord(position_source[0]), ord(position_cible[0])
        rangee_source, rangee_cible = int(position_source[1]), int(position_cible[1])

        if abs(colonne_source - colonne_cible) != abs(rangee_source - rangee_cible):
            return False

        # Par contre, il ne peut pas faire de sur-place.
        if colonne_source == colonne_cible and rangee_source == rangee_cible:
            return False

        return True

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2657'
            else:
                return 'FB'
        else:
            if UTILISER_UNICODE:
                return '\u265d'
            else:
                return 'FN'


class Roi(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        # Un roi peut se déplacer d'une case, sur une ligne, rangée ou colonne.
        colonne_source, colonne_cible = ord(position_source[0]), ord(position_cible[0])
        rangee_source, rangee_cible = int(position_source[1]), int(position_cible[1])

        distance_colonne = abs(colonne_source - colonne_cible)
        distance_rangee = abs(rangee_source - rangee_cible)

        if distance_rangee != 1 and distance_colonne != 1:
            return False

        return True

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2654'
            else:
                return 'RB'
        else:
            if UTILISER_UNICODE:
                return '\u265a'
            else:
                return 'RN'


class Dame(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        # Une mouvement pour une dame est valide si elle se déplace sur une rangée, colonne ou en diagonale.
        # Notez que nous utilisons directement les méthodes à partir d'une classe, en passant comme premier
        # argument l'objet courant (self). Il aurait été plus "propre" de se créer des nouvelles fonctions
        # communes aux classes Tour, Fou et Dame pour éviter de faire ces appels à partir de la classe.
        return Tour.peut_se_deplacer_vers(self, position_source, position_cible) or \
            Fou.peut_se_deplacer_vers(self, position_source, position_cible)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2655'
            else:
                return 'DB'
        else:
            if UTILISER_UNICODE:
                return '\u265b'
            else:
                return 'DN'
