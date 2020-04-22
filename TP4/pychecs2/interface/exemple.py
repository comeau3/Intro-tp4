"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.
"""
from tkinter import NSEW, Canvas, Label, Tk, Menu, colorchooser
from pychecs2.echecs.partie import (Partie)
import webbrowser
# Exemple d'importation de la classe Partie.
from pychecs2.echecs.exception import (AucunePieceAPosition, MauvaiseCouleurPiece, ErreurDeplacement)



class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.
    """

    def __init__(self, parent, n_pixels_par_case, partie):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        self.couleur1 = "white"
        self.couleur2 = "gray"

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.position_selectionnee = None

        self.partie = partie

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces. Vous devinerez, si vous réutilisez cette classe dans votre TP4,
        # qu'il fandra adapter ce code pour plutôt utiliser la classe Echiquier.
        self.pieces = {
            'a1': 'TB', 'b1': 'CB', 'c1': 'FB', 'd1': 'DB', 'e1': 'RB', 'f1': 'FB', 'g1': 'CB', 'h1': 'TB',
            'a2': 'PB', 'b2': 'PB', 'c2': 'PB', 'd2': 'PB', 'e2': 'PB', 'f2': 'PB', 'g2': 'PB', 'h2': 'PB',
            'a7': 'PN', 'b7': 'PN', 'c7': 'PN', 'd7': 'PN', 'e7': 'PN', 'f7': 'PN', 'g7': 'PN', 'h7': 'PN',
            'a8': 'TN', 'b8': 'CN', 'c8': 'FN', 'd8': 'DN', 'e8': 'RN', 'f8': 'FN', 'g8': 'CN', 'h8': 'TN',
        }

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)


    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.
        """


        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case


                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = self.couleur1

                else:
                    couleur = self.couleur2

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')

        #



    #permet de trouver le carré sélectionné
    #def carre_selectionne(self, event):
        # y1 = event.y // self.canvas_echiquier.n_pixels_par_case
        # y2 = y1 + n_pixels_par_case
        # x1 = event.x // self.canvas_echiquier.n_pixels_par_case
        # x2 = x1 + n_pixels_par_case
        # return x1, y1, x2, y2


    def dessiner_pieces(self):
        # Caractères unicode représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        caracteres_pieces = {'PB': '\u2659',
                             'PN': '\u265f',
                             'TB': '\u2656',
                             'TN': '\u265c',
                             'CB': '\u2658',
                             'CN': '\u265e',
                             'FB': '\u2657',
                             'FN': '\u265d',
                             'RB': '\u2654',
                             'RN': '\u265a',
                             'DB': '\u2655',
                             'DN': '\u265b'
                             }

        # Pour tout paire position, pièce:
        for position, piece in self.partie.echiquier.dictionnaire_pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(
                position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(
                position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text=piece,
                             font=('Deja Vu', self.n_pixels_par_case // 2), tags='piece')



    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes
        self.raffraichir()

    def raffraichir(self):
         # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()


        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()
        #self.square.clear()



class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Échiquier")

        self.partie = Partie()

        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du menu
        menubar = BarreMenu(self)
        self.config(menu=menubar)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie)
        if self.position_selectionnee is not None:
            CanvasEchiquier.dessiner_cases()

        self.canvas_echiquier.grid(sticky=NSEW)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()
        self.messagejoueuractif = Label(self)
        self.messagejoueuractif['text'] = 'Tour du joueur blanc'
        self.messagejoueuractif.grid()



        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)






    def selectionner(self, event):


        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))
        print(event.x)
        print(event.y)

        try:
            if self.canvas_echiquier.position_selectionnee is None:
                print('1er clic')
                self.canvas_echiquier.position_selectionnee = position
            else:
                print('second clic')
                print(self.canvas_echiquier.position_selectionnee, position)
                self.partie.deplacer(self.canvas_echiquier.position_selectionnee, position)
                self.canvas_echiquier.position_selectionnee = None

                if self.partie.partie_terminee():
                    self.messages['foreground'] = "black"
                    self.messages['text'] = "La partie est terminée, le joueur" + self.partie.determiner_gagnant() + 'a gagné! =)'

        except (ErreurDeplacement, AucunePieceAPosition, MauvaiseCouleurPiece) as e:
            self.canvas_echiquier.position_selectionnee = None
            self.messages['foreground'] = "red"
            self.messages['text'] = e
            self.canvas_echiquier.position_selectionne= None
        finally:
            self.canvas_echiquier.raffraichir()

        if self.partie.joueur_actif == 'blanc':
            self.messagejoueuractif['foreground'] = 'black'
            self.messagejoueuractif['text'] = 'Tour du joueur blanc'
        else:
            self.messagejoueuractif['foreground'] = "black"
            self.messagejoueuractif['text'] = 'Tour du joueur noir'




def sauvegarder():
    print("sauvegarder")


def charger():
    print("charger")

def nouvelle_partie():
    pass

def changertheme():
    CanvasEchiquier.couleur1 = "purple"
    CanvasEchiquier.couleur2 = "yellow"
    print("theme")
    CanvasEchiquier.raffraichir()

def ouvreRegles():
    webbrowser.open("https://fr.wikipedia.org/wiki/R%C3%A8gles_du_jeu_d%27%C3%A9checs")


class BarreMenu(Menu):
    def __init__(self,parent):
        Menu.__init__(self,parent)

        menufichier = Menu(self, tearoff=0)
        menufichier.add_command(label='Nouvelle partie', command=nouvelle_partie)
        menufichier.add_command(label="Ouvrir", command=charger)
        menufichier.add_command(label="Sauvegarder", command=sauvegarder)
        menufichier.add_separator()
        menufichier.add_command(label="Quitter", command=self.quit)
        self.add_cascade(label="Fichier", menu=menufichier)

        # Ajout d'un menu pour les options
        menuoptions = Menu(self, tearoff=0)
        menuoptions.add_command(label="Couleur", command=changertheme)
        self.add_cascade(label="Options", menu=menuoptions)

        menuaide = Menu(self, tearoff=0)
        menuaide.add_command(label="Règles des échecs", command=ouvreRegles)
        self.add_cascade(label="Aide", menu=menuaide)
