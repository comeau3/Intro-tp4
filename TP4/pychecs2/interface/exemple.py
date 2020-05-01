"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.
"""
from pickle import UnpicklingError
from tkinter import NSEW, Canvas, Label, Tk, Menu, CENTER, LEFT, font, RIGHT, E, messagebox, \
    filedialog, Text, END, Button
from pychecs2.echecs.partie import (Partie)
from pychecs2.echecs.echiquier import (Echiquier)

import webbrowser
# Exemple d'importation de la classe Partie.
from pychecs2.echecs.exception import (AucunePieceAPosition, MauvaiseCouleurPiece, ErreurDeplacement)
import pickle
import time



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
        self.parent = parent
        self.tutoriel = True

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.position_selectionnee = None
        self.position_tutoriel = None

        self.afficher_liste_deplacements = False


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
        # self.bind('<Button-1>', self.obtenir_position_a_partir_de_coordonnees)

    def obtenir_position_a_partir_de_coordonnees(self, i, j):
        position = "{}{}".format(self.partie.echiquier.lettres_colonnes[j],
                                 int(self.partie.echiquier.chiffres_rangees[self.n_lignes - i - 1]))

        return position




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
                if self.obtenir_position_a_partir_de_coordonnees(i, j) == self.position_selectionnee:
                    couleur = "cyan"




                elif (i + j) % 2 == 0:
                    couleur = self.couleur1

                else:
                    couleur = self.couleur2

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')


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


class Fenetre(Tk):
    def __init__(self):
        super().__init__()
        self.estTermine = False
        self.estSauvegarde = False
        self.listemovements = []
        self.listepiecesnoirs = []
        self.listepiecesblanches = []
        self.chrono_actif = False




        # On redéfinie ce qui se passe lors de la fermeture du  fichier.
        self.protocol("WM_DELETE_WINDOW", self.demandesauvegarde)

        # Nom de la fenêtre.
        self.title("Échiquier")

        self.partie = Partie()

        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 60, self.partie)
        self.canvas_echiquier.grid(row=0, column=0, sticky=NSEW)

        # Création du menu
        self.menubar = BarreMenu(self, self.canvas_echiquier)
        self.config(menu=self.menubar)

        # Ajout d'une étiquette d'information.
        self.lblMessages = Label(self)
        self.lblMessages.config(font=("Courier", 18))
        self.lblMessages.grid()

        self.lblMessagejoueuractif = Label(self)
        self.lblMessagejoueuractif['text'] = 'Tour du joueur blanc'
        self.lblMessagejoueuractif.config(font=("Courier", 18))
        self.lblMessagejoueuractif.grid()

        # Listes des pièces perdues par chaque joueurs
        self.lblpiecesblanches = Label(self, anchor='w')
        self.lblpiecesblanches.grid(row=4, column=0)
        self.lblpiecesblanches.config(font=("Courier", 14))
        self.lblpiecesblanches['text'] = 'Pièces noires perdues: '

        self.lblpiecesnoires = Label(self, anchor='w')
        self.lblpiecesnoires.config(font=("Courier", 14))
        self.lblpiecesnoires.grid(row=4, column =1)
        self.lblpiecesnoires['text'] = 'Pièces blanches perdues: '

        # Création d'une zone de texte pour l'affichage des déplacements.
        self.afficher_deplacement = False

        self.txtListe = Text(self)
        self.txtListe.grid(row=0, column=1, sticky=NSEW)

        self.lblListe = Label(self)
        self.lblListe['text'] = 'La liste des mouvements'
        self.lblListe.grid(row=1, column=1, sticky=NSEW)

        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-1>', self.selectionner)

        # chrono
        self.chrono = Label(text="")
        self.chrono.grid(row=5, column=0, sticky=NSEW)
        self.minute = 0
        self.second = 0
        self.color_chrono = "blue"

    def update_clock(self):
        if self.chrono_actif:
            self.second += 1
            if self.second == 60:
                self.second = 0
                self.minute += 1
            elif self.minute == 1 and self.second == 30:
                self.color_chrono = "red"
            elif self.minute == 2:
                    self.second = 0
                    self.minute = 0
                    self.partie.joueur_suivant()

        now = f'Chrono: {self.minute} m : {self.second} s'
        self.chrono.configure(text=now, fg=self.color_chrono)
        self.canvas_echiquier.after(1000, self.update_clock)

    def stop_clock(self):
        self.canvas_echiquier.after_cancel(self.update_clock)
        self.second = 0
        self.chrono_actif = False

    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case
        position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne],
                                 int(self.canvas_echiquier.chiffres_rangees[
                                         self.canvas_echiquier.n_lignes - ligne - 1]))



        # print(event.x)               # Pour des fins de débug'
        # print(event.y)               # Pour des fins de débug

        if not self.partie.partie_terminee():
            try:
                if self.canvas_echiquier.position_selectionnee is None:
                    if self.partie.echiquier.recuperer_piece_a_position(position):
                        if self.partie.joueur_actif == self.partie.echiquier.couleur_piece_a_position(position):
                            # print('1er clic')  # Pour tester les positions sélectionnées


                            self.canvas_echiquier.position_selectionnee = position
                            self.lblMessages['text'] = ""
                        else:
                            messagebox.showwarning('Mauvaise couleur','Mauvaise couleur de pièce sélectionnée')

                else:
                    # print('second clic') # Pour tester les positions sélectionnées
                    # print(self.canvas_echiquier.position_selectionnee, position)
                    piecesource = self.partie.echiquier.recuperer_piece_a_position(
                        self.canvas_echiquier.position_selectionnee)

                    piececible = self.partie.echiquier.recuperer_piece_a_position(position)

                    # Si une prise est faite, affiche la pièce. Sinon affiche seulement le déplacement.
                    if piececible is not None:
                        mouvement = "Le joueur {} a joué la pièce {} de {} à {} et a prit la pièce {}".format(
                            self.partie.joueur_actif, piecesource,
                            self.canvas_echiquier.position_selectionnee,
                            position, piececible)

                    else:
                        mouvement = "Le joueur {} a joué la pièce {} de {} à {} ". \
                            format(self.partie.joueur_actif, piecesource, self.canvas_echiquier.position_selectionnee,
                                   position)
                    self.partie.deplacer(self.canvas_echiquier.position_selectionnee, position)
                    self.minute = 0
                    self.second = 0

                    if piececible is not None:
                        self.piecesprises(piececible)
                    self.listemovements.append(mouvement)
                    self.canvas_echiquier.position_selectionnee = None
                    self.estSauvegarde = False

                    self.rafraichirtexte()

            except (ErreurDeplacement, AucunePieceAPosition, MauvaiseCouleurPiece) as e:
                self.canvas_echiquier.position_selectionnee = None
                messagebox.showwarning("Erreur", e)
                self.canvas_echiquier.position_selectionne = None
            finally:
                self.canvas_echiquier.raffraichir()

            if self.partie.joueur_actif == 'blanc':
                self.lblMessagejoueuractif['foreground'] = 'black'
                self.lblMessagejoueuractif['text'] = 'Tour du joueur blanc'

            else:
                self.lblMessagejoueuractif['foreground'] = "black"
                self.lblMessagejoueuractif['text'] = 'Tour du joueur noir'

        if self.partie.partie_terminee():
            if messagebox.askyesno( "Partie terminée", "La partie est terminée, le joueur " +
                                    self.partie.determiner_gagnant() + ' a gagné! =)' + '\n' +
                                    'Voulez-vous rejouer de nouveau?'):
                self.menubar.nouvelle_partie()

    def piecesprises(self, piece):
        if self.partie.joueur_actif == "blanc":
            self.listepiecesnoirs.append(piece)

        elif self.partie.joueur_actif == "noir":
            self.listepiecesblanches.append(piece)



    def demandesauvegarde(self):
        if not self.estSauvegarde:
            if not messagebox.askyesno("Quitter", "Voulez vous sauvegarder avant de quitter?"):
                self.destroy()
            else:
                self.menubar.sauvegarder()
                self.destroy()
        else:
            self.destroy()

    def rafraichirtexte(self):

        self.txtListe['foreground'] = "purple"
        self.txtListe.delete("1.0", END)
        for x in self.listemovements:
            self.txtListe.insert(END, x + "\n")

        if self.partie.partie_terminee():
            self.txtListe.insert(END, "La partie est terminée. Le joueur  " + self.partie.determiner_gagnant()
                                 + ' a gagné! =)')

        self.lblpiecesblanches.config(text='Pièces noires perdues: ' + (" ".join(map(str, self.listepiecesblanches))))
        self.lblpiecesnoires.config(text='Pièces blanches perdues: ' + (" ".join(map(str, self.listepiecesnoirs))))


class BarreMenu(Menu):
    def __init__(self, parent, canvas_echiquier):
        Menu.__init__(self, parent)

        self.canvas_echiquier = canvas_echiquier
        self.parent = parent  # le parent est la fenetre

        menufichier = Menu(self, tearoff=0)
        menufichier.add_command(label='Nouvelle partie', command=self.nouvelle_partie)
        menufichier.add_command(label="Ouvrir", command=self.charger)
        menufichier.add_command(label="Sauvegarder", command=self.sauvegarder)
        menufichier.add_separator()
        menufichier.add_command(label="Quitter", command=self.quitter)
        self.add_cascade(label="Fichier", menu=menufichier)

        # Ajout d'un menu pour les options
        menuoptions = Menu(self, tearoff=0)
        menuoptions.add_command(label="Couleur", command=self.changertheme)
        menuoptions.add_command(label="Partir le chrono", command=self.partir_chrono)
        menuoptions.add_command(label="Arrêter le chrono", command=self.arreter_chrono)
        self.add_cascade(label="Options", menu=menuoptions)

        menuaide = Menu(self, tearoff=0)
        menuaide.add_command(label="Règles des échecs", command=self.ouvreRegles)
        self.add_cascade(label="Aide", menu=menuaide)

    def partir_chrono(self):
        if not self.parent.chrono_actif:
            self.parent.chrono_actif = True
            self.parent.update_clock()

    def arreter_chrono(self):
        self.parent.stop_clock()

    def sauvegarder(self):

        nom_fichier = filedialog.asksaveasfilename(defaultextension='.pickle')
        try:
            if nom_fichier is not None:
                sauvegarde = open(nom_fichier, 'wb')

                pickle.dump(self.canvas_echiquier.partie.echiquier.dictionnaire_pieces, sauvegarde)
                pickle.dump(self.parent.listemovements, sauvegarde)
                pickle.dump(self.parent.listepiecesblanches, sauvegarde)
                pickle.dump(self.parent.listepiecesnoirs, sauvegarde)
                pickle.dump(self.canvas_echiquier.partie.joueur_actif, sauvegarde)
                self.parent.estSauvegarde = True
                messagebox.showinfo("Sauvegarde", "Sauvegarde Completée")

        except FileNotFoundError:
            messagebox.showinfo("Sauvegarde", "Sauvegarde Annulée")

    def charger(self):
        nom_fichier = filedialog.askopenfilename()
        try:
            if nom_fichier is not None:
                charger = open(nom_fichier, 'rb')

                self.canvas_echiquier.partie.echiquier.dictionnaire_pieces = pickle.load(charger)
                self.parent.listemovements = pickle.load(charger)
                self.parent.listepiecesblanches = pickle.load(charger)
                self.parent.listepiecesnoirs = pickle.load(charger)
                self.canvas_echiquier.partie.joueur_actif = pickle.load(charger)
                self.canvas_echiquier.raffraichir()
                messagebox.showinfo("Chargement", "Chargement Completé")

                self.parent.rafraichirtexte()
        except FileNotFoundError:
            messagebox.showinfo("Chargement", "Chargement Annulé")
        except UnpicklingError:
            messagebox.showerror("Chargement", "Erreur lors du chargement. Mauvais fichier?")

    def nouvelle_partie(self):
        self.canvas_echiquier.partie.echiquier.initialiser_echiquier_depart()
        self.canvas_echiquier.partie.joueur_actif = 'blanc'
        self.parent.listemovements = []
        self.parent.txtListe.delete('1.0', END)
        self.canvas_echiquier.raffraichir()
        self.parent.lblMessages['text'] = " "
        self.parent.lblMessagejoueuractif['text'] = " "
        self.parent.listepiecesnoirs = []
        self.parent.listepiecesblanches = []
        self.parent.lblpiecesblanches['text'] = 'Pièces noires perdues: '
        self.parent.lblpiecesnoires['text'] = 'Pièces blanches perdues: '
        self.parent.minute = 0
        self.parent.second = 0

    def afficher_tutoriel(self):
        if self.canvas_echiquier.tutoriel == True:
            self.canvas_echiquier.tutoriel = False
        else:
            self.canvas_echiquier.tutoriel = True

    def quitter(self):
        Fenetre.demandesauvegarde(self.parent)

    def changertheme(self):
        if self.canvas_echiquier.couleur1 == "white":
            self.canvas_echiquier.couleur1 = "green"
            self.canvas_echiquier.couleur2 = "red"

        elif self.canvas_echiquier.couleur1 == "green":
            self.canvas_echiquier.couleur1 = "yellow"
            self.canvas_echiquier.couleur2 = "purple"
        else:
            self.canvas_echiquier.couleur1 = "white"
            self.canvas_echiquier.couleur2 = "gray"
        self.canvas_echiquier.raffraichir()

    def ouvreRegles(self):
        webbrowser.open("https://fr.wikipedia.org/wiki/R%C3%A8gles_du_jeu_d%27%C3%A9checs")


f_accueil = Tk()
f_accueil.title("Fenêtre d'acceuil")
f_accueil.geometry("650x650")

f_accueil_label1 = Label(f_accueil, text="Bienvenue dans notre jeu d'échec à interface graphique!", font="Times 20",
                         justify=CENTER)
f_accueil_label1.grid(row=0)

texte1 = Label(f_accueil,
               text="Dans cet interface graphique, vous trouverez différentes options"
                    " \n permettant de jouer aux échecs!",
               font="Times 16")
texte1.grid(row=1, pady=100)

texte2 = Label(f_accueil, text="Ce jeu d'échec représente un prototype de base. Les mouvements de type 'roque',\n "
                               "la prise 'en passant' ainsi que la promotion du pion de sont pas supportés. "
                               "\n De plus, les détections des mises en échecs ne sont pas programmées, \n"
                               "ainsi il vous sera possible d'effectuer un mouvement qui vous mettera en échec. \n"
                               "La partie se terminera quand un des rois ne sera plus sur l'échiquier, les parties \n"
                               "nulles sont donc par le fait même, impossibles. Les règles complètes sont disponibles \n"
                               "dans l'onglet 'aide'."
               , justify=LEFT, font="Times 14")

texte2.grid(row=2, pady=0)

texte3 = Label(f_accueil, text="Fermez cette fenêtre pour débuter la partie!")
texte3.grid(row=3, pady=50)
f = font.Font(texte3, texte3.cget("font"))
f.configure(underline=True)
texte3.configure(font=f)




name1 = Label(f_accueil, text="Réalisé par:\nJean-Christophe Comeau\nColin Routhier-Legault", justify=RIGHT)
name1.grid(row=4, sticky=E)



f_accueil.mainloop()
