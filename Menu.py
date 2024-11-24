import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

from Snake_final import Snake
from Final_Bot import Final_bot
from Intermediaire import BotInt
from Player import Player

import os
import io
from PIL import Image, ImageTk



class Menu():
    """
    Classe représentant le menu principal du jeu Snake. 
    """

    def __init__(self):
        """Intialisation de la fenetre principale du jeu, ainsi que des variables nécessaires au jeu."""

        #Creation fenetre principale
        self.root = tk.Tk()
        self.root.title("Menu principal")
        self.root.geometry("768x432")
        self.root.resizable(width=False, height=False)

        #Chargement des images
        self.background = tk.PhotoImage(file = 'photos/background.png' ,master=self.root)
        self.retour_image = tk.PhotoImage(file = 'photos/bouton_retour_150x150.png',master = self.root, format = 'png')
        self.menu_image = tk.PhotoImage(file = 'photos/bouton_menu_150x150.png',master = self.root, format = 'png')
        self.replay_image = tk.PhotoImage(file = 'photos/bouton_replay_150x150.png',master = self.root, format = 'png')
        self.jouer_image = tk.PhotoImage(file = 'photos/bouton_jouer_150x150.png',master = self.root, format = 'png')
        self.quitter_image = tk.PhotoImage(file = 'photos/bouton_quitter_150x150.png',master = self.root, format = 'png')
        self.rejouer_image = tk.PhotoImage(file = 'photos/bouton_rejouer_150x150.png',master = self.root, format = 'png')
        self.enregister_image = tk.PhotoImage(file = 'photos/bouton_save_150x150.png',master = self.root, format = 'png')
        self.regles_image = tk.PhotoImage(file = 'photos/bouton_regles_150x150.png',master = self.root, format = 'png')
        self.credits_image = tk.PhotoImage(file = 'photos/bouton_credit_150x150.png',master = self.root, format = 'png')
        self.background_2players = tk.PhotoImage(file = 'photos/background_2p.png' ,master=self.root)
        self.background_1player = tk.PhotoImage(file = 'photos/background_1p.png' ,master=self.root)
        self.background_regles = tk.PhotoImage(file = 'photos/background_regles.png' ,master=self.root)
        self.chemin_image = tk.PhotoImage(file = 'photos/chemin.png',master = self.root, format = 'png')
        self.logo = tk.PhotoImage(file = 'photos/logo.png' ,master=self.root)
        self.images = []
        
        #Definition des grandeurs de la fenetre
        self.width = self.background.width()
        self.height = self.background.height()


        #Creation d'une liste des widgets nous permettant de savoir quels widgets sont affichés, et de les supprimer facilement
        self.widgets_liste = []

        #Definition des variables permettant de gérer les différents serpents
        self.snake1 = False
        self.snake2 = False
        self.njoueurs = 1
        self.multi = False
        self.jeu = False

        self.chemin_display = True
        self.son_actif = True

        #Definition des variables permettant de gérer les différents bots
        self.bot_un = tk.StringVar()
        self.bot_un.set("Bot Astar")       #On initialise les bots à des modes arbitrairement choisis
        self.bot_deux = tk.StringVar()
        self.bot_deux.set("Bot Astar")

        #Variable permettant de choisir le mode de replay que nous voulons
        self.highscore = tk.BooleanVar()

        #Definition des variables permettant de gérer les couleurs des serpents
        self.couleur1 = tk.StringVar()
        self.couleur2 = tk.StringVar()
        self.couleur1.set("Vert")   
        self.couleur2.set("Noir")
        self.couleurpomme1 = tk.StringVar()
        self.couleurpomme2 = tk.StringVar()
        self.couleurpomme1.set("Rouge")
        self.couleurpomme2.set("Violet")

        #Definition de la variable permettant de gérer la vitesse du jeu
        self.speed = tk.IntVar()
        self.speed.set(7)

        #Création de dictionnaire avec les couleurs, les bots et les vitesses, permettant d'avoir un affichage plus clair
        self.couleurs = ["Rouge","Bleu","Vert","Jaune","Orange","Violet","Rose","Marron","Gris","Noir"] 
        self.colors = {"Rouge":"red","Bleu":"blue","Vert":"green","Jaune":"yellow","Orange":"orange","Violet":"purple","Rose":"pink","Marron":"brown","Gris":"grey","Noir":"black"}

        self.bots_afficher = ["Bot intermédiaire","Bot Astar","Bot Killer","Bot Smart","Joueur"]
        self.bots = {"Bot intermédiaire":'theo',"Bot Astar":'Astar',"Bot Killer":'Killer',"Joueur":'player',"Bot Smart" : 'Smart'}

        self.vitesse = {0 : 500, 1 : 450, 2 : 400, 3 : 350, 4 : 300, 5 : 250, 6 : 160, 7 : 80, 8 : 40, 9 : 20, 10 : 10}

        #Création du canvas dans lequel nous afficherons tout le menu
        self.canvas = tk.Canvas(self.root, bg = "light green", width=self.width, height=self.height) 
        self.canvas.create_image(0, 0, image=self.background, anchor= tk.NW) 
        self.canvas.pack()

        #Création de tous les widgets initiaux
        self.create_widget()
        
        
    def create_widget(self):
        """Fonction permettant de créer tous les widgets initiaux du menu :
        - Le logo
        - Le bouton quitter
        - Le bouton règles
        - Le bouton jouer
        - Le bouton replay
        """


        #Affichage du logo
        logo = self.canvas.create_image(-10, -20, image=self.logo, anchor= tk.NW)
        self.widgets_liste.append(logo)

        #Création du bouton quitter
        self.bouton_create(100, 350, self.quitter_image, self.leave)

        #Création du bouton règles
        self.bouton_create(275, 350, self.regles_image, self.menu_regles)

        #Création du bouton jouer
        self.bouton_create(275, 215, self.jouer_image, self.jouer)

        #Création du bouton replay 
        self.bouton_create(100, 215, self.replay_image, self.menu_replay)

        #Création d'un raccourci pour pouvoir fermer le jeu
        self.root.bind("<Control-q>", self.leave)

    def clear(self):

        """Fonction permettant de supprimer tous les widgets du menu, tout en laissant le fond d'écran"""

        for i in self.widgets_liste:
            self.canvas.delete(i)
        self.widgets_liste = []

    def parametre_chemin(self,event):
        """Fonction permettant de gérer l'affichage du chemin du serpent, et d'indiquer au joueur si l'option est activée ou non"""

        if self.chemin_display :
            self.chemin_display = False
            self.barre_chemin = self.canvas.create_line(self.width - 168, 93, self.width - 120, 47, fill = 'red', width = 3, state = 'disable')
            self.widgets_liste.append(self.barre_chemin)
        else : 
            self.chemin_display = True
            self.canvas.delete(self.barre_chemin)
            self.widgets_liste.remove(self.barre_chemin)

        if self.jeu :
            self.snk1.chemin = self.chemin_display
            #print(self.snk1.path_id)
            if len(self.snk1.path_id) != 0:
                for i in range(len(self.snk1.path_id)):
                    self.game_area.delete(self.snk1.path_id[i][1])

            if self.multi :
                self.snk2.chemin = self.chemin_display
                if len(self.snk2.path_id) != 0:
                    for i in range(len(self.snk2.path_id)):
                        self.game_area.delete(self.snk2.path_id[i][1])



    def leave(self, event):
        """Fonction permettant de quitter le jeu, en fermant la fenêtre"""

        self.root.destroy()

    def menu_regles(self, event):
        """Fonction permettant d'afficher les règles du jeu"""

        #On supprime tous les widgets du menu
        self.clear() 
        fond_opaque = self.canvas.create_image(0, 0, image=self.background_regles, anchor= tk.NW)
        with open('Textes/regles.txt', 'r', encoding= 'utf-8') as fichier:
            texte = fichier.read()
            self.canvas.ombre = self.canvas.create_text(self.width/2 - 50 +1, self.height/2 - 10+1, text=texte, font=("Helvetica", 10, 'bold'), fill = 'grey', justify = tk.LEFT)
            self.canvas.regles_jeu = self.canvas.create_text(self.width/2 - 50, self.height/2 - 10, text=texte, font=("Helvetica", 10, 'bold'), fill = 'black', justify = tk.LEFT)

        
        #Affichage d'un texte expliquant le fonctionnement du Snake, ainsi que les particularités de notre jeu
        
        self.widgets_liste.append(self.canvas.regles_jeu)
        self.widgets_liste.append(self.canvas.ombre)
        self.widgets_liste.append(fond_opaque)
        #Creation d'un bouton retour, allant au menu principal
        self.bouton_create(650, 350, self.retour_image, self.retour_menu)
        self.bouton_create(650, 215, self.credits_image, self.credits)

    def credits(self, event):
        """Fonction permettant d'afficher les crédits du jeu"""

        #On supprime tous les widgets du menu
        self.clear() 

        fond_opaque = self.canvas.create_image(0, 0, image=self.background_regles, anchor= tk.NW)

        #Affichage d'un texte expliquant le fonctionnement du Snake, ainsi que les particularités de notre jeu
        with open('Textes/credits.txt', 'r', encoding= 'utf-8') as fichier:
            texte = fichier.read()
            self.canvas.credits_texte = self.canvas.create_text(self.width/2 - 50, self.height/2 - 20, text=texte, font=("Helvetica", 10, 'bold'), fill = 'black', justify = tk.LEFT)

        #Creation d'un bouton retour, allant au menu principal
        self.bouton_create(650, 350, self.menu_image, self.retour_menu)
        self.bouton_create(515, 350, self.retour_image, self.menu_regles)

        self.widgets_liste.append(self.canvas.credits_texte)
        self.widgets_liste.append(fond_opaque)


    def chgt_bordure(self, event):
        """Fonction permettant de changer la couleur de la bordure d'un bouton, lorsqu'on passe la souris dessus"""

        #On regarde la couleur actuelle de la bordure du bouton
        if self.canvas.itemcget(self.bordure, 'outline') == 'white': #Si elle est blanche
            self.canvas.itemconfig(self.bordure, outline = 'black') #On la met en noir
        else :                                                          #Sinon          
            self.canvas.itemconfig(self.bordure, outline = 'white') #On la met en blanc

    def jouer(self, event):
        """Fonction permettant de choisir le nombre de joueurs, pour ensuite lancer le jeu"""

        self.clear() #On supprime tous les widgets du menu

        #Affichage de l'onglet permettant de passer à 2 joueurs
        self.deux_jou = self.canvas.create_image (self.width/2, 0, image=self.background_2players, anchor= tk.NW) #On affiche l'onglet cliquable 2 joueurs
        self.canvas.tag_bind(self.deux_jou, "<Button-1>", self.two_player) #On lui associe la fonction two_player, qui va permettre d'avoir 2 joueurs

        self.bordure = self.canvas.create_rectangle(self.width/2, 0, self.width,100, fill = '',width = 4, outline = 'black') #On crée une bordure réactive autour de l'onglet 2 joueurs
        self.canvas.tag_bind(self.bordure, "<Enter>", self.chgt_bordure) #On lui associe la fonction chgt_bordure, qui va permettre de changer la couleur de la bordure

        self.deux_jou_text = self.canvas.create_text(584, 50, text="2 joueurs", font=("Segoe Print", 20), fill="white", state = 'disabled') #On affiche le texte 2 joueurs sur le bouton à cliquer
        self.un_jou_text = self.canvas.create_text(self.width/4, 50, text=" • 1 joueur", font=("Segoe Print", 20, "bold"), fill="black", state = 'disabled') #On affiche le texte •1 joueur pour savoir quel mode est sélectionné

        #On ajoute tous les widgets dans la liste des widgets
        self.widgets_liste.append(self.un_jou_text)
        self.widgets_liste.append(self.deux_jou_text)
        self.widgets_liste.append(self.bordure)
        self.widgets_liste.append(self.deux_jou)        
        
        #On crée un bouton jouer, qui va permettre de lancer la partie
        self.bouton_create(650, 350, self.jouer_image, self.start)

        #On crée un bouton retour, qui va permettre de revenir au menu principal
        self.bouton_create(100, 350, self.retour_image, self.retour_menu)

        #On crée un menu déroulant, qui va permettre de choisir le bot
        self.choix_bot_un = tk.OptionMenu(self.root, self.bot_un, *self.bots_afficher) #On utilise la classe OptionMenu de tkinter
        self.menu_place_un = self.canvas.create_window(400, 250, window=self.choix_bot_un) #On place le menu déroulant sur le canvas

        #On crée une échelle qui va permettre de choisir la vitesse du bot
        self.speed_scale = tk.Scale(self.root, from_=0, to=10, orient=tk.HORIZONTAL, variable = self.speed, length=200, background = 'light grey', troughcolor = 'grey') #On utilise la classe Scale de tkinter
        self.speed_scale_place = self.canvas.create_window(self.width/2, 400, window=self.speed_scale)  #On place l'échelle sur le canvas
        self.speed_text = self.canvas.create_text(self.width/2, 360, text="Vitesse du jeu :", font=("Segoe Print", 14), fill="white") #On écrit ce que fait l'échelle

        #On ajoute tous les widgets dans la liste des widgets   
        self.widgets_liste.append(self.speed_scale_place)
        self.widgets_liste.append(self.menu_place_un)
        self.widgets_liste.append(self.speed_text)


    def two_player(self, event):
        """Fonction permettant de passer à 2 joueurs, en changeant les variables et les widgets affichés"""

        #On efface les widgets qui ne nous intéressent plus
        self.widgets_liste.remove(self.deux_jou)
        self.canvas.delete(self.deux_jou)
        self.widgets_liste.remove(self.deux_jou_text)
        self.canvas.delete(self.deux_jou_text)
        self.widgets_liste.remove(self.bordure)
        self.canvas.delete(self.bordure)
        self.widgets_liste.remove(self.menu_place_un)
        self.canvas.delete(self.menu_place_un)

        #On crée un bouton pour choisir le nombre de joueurs
        self.un_jou = self.canvas.create_image (0, 0, image=self.background_1player, anchor= tk.NW) #On affiche l'onglet cliquable 1 joueur
        self.canvas.tag_bind(self.un_jou, "<Button-1>", self.one_player) #On lui associe la fonction one_player, qui va permettre d'avoir 1 joueur
        self.bordure = self.canvas.create_rectangle(0, 0, self.width/2,100, fill = '',width = 4, outline = 'black') #On crée une bordure réactive autour de l'onglet 1 joueur
        self.canvas.tag_bind(self.bordure, "<Enter>", self.chgt_bordure) #On lui associe la fonction chgt_bordure, qui va permettre de changer la couleur de la bordure

        self.un_jou_text = self.canvas.create_text(self.width/4, 50, text="1 joueur", font=("Segoe Print", 20), fill="white", state = 'disabled') #On affiche le texte 1 joueur sur le bouton à cliquer
        self.deux_jou_text = self.canvas.create_text(3*self.width/4, 50, text=" • 2 joueurs", font=("Segoe Print", 20, "bold"), fill="black", state = 'disabled') #On affiche le texte •2 joueurs pour savoir quel mode est sélectionné
        
        #On crée deux menus déroulants, qui vont permettre de choisir les bots
        self.choix_bot_un = tk.OptionMenu(self.root, self.bot_un, *self.bots_afficher) #On utilise la classe OptionMenu de tkinter
        self.menu_place_un = self.canvas.create_window(300, 250, window=self.choix_bot_un) #On place le menu déroulant sur le canvas
        
        self.choix_bot_deux = tk.OptionMenu(self.root, self.bot_deux, *self.bots_afficher) #On utilise la classe OptionMenu de tkinter
        self.menu_place_deux = self.canvas.create_window(500, 250, window=self.choix_bot_deux) #On place le menu déroulant sur le canvas
        
        #On ajoute tous les nouveaux widgets dans la liste des widgets
        self.widgets_liste.append(self.un_jou_text)
        self.widgets_liste.append(self.deux_jou_text)
        self.widgets_liste.append(self.bordure)
        self.widgets_liste.append(self.un_jou)
        self.widgets_liste.append(self.menu_place_un)
        self.widgets_liste.append(self.menu_place_deux)

        #On change la variable multi, qui va permettre de savoir que l'on est en mode 2 joueurs
        self.multi = True 

    def one_player(self, event):
        """Fonction permettant de passer à 1 joueur, en changeant les variables et les widgets affichés, en retournant comme au début"""

        #On efface les widgets qui ne nous intéressent plus
        self.widgets_liste.remove(self.un_jou)
        self.canvas.delete(self.un_jou)
        self.widgets_liste.remove(self.un_jou_text)
        self.canvas.delete(self.un_jou_text)
        self.widgets_liste.remove(self.bordure)
        self.canvas.delete(self.bordure)
        self.widgets_liste.remove(self.menu_place_un)
        self.canvas.delete(self.menu_place_un)
        self.widgets_liste.remove(self.menu_place_deux)
        self.canvas.delete(self.menu_place_deux)

        #On crée un bouton pour choisir le nombre de joueurs
        self.deux_jou = self.canvas.create_image (self.width/2, 0, image=self.background_2players, anchor= tk.NW) #On affiche l'onglet cliquable 2 joueurs
        self.canvas.tag_bind(self.deux_jou, "<Button-1>", self.two_player) #On lui associe la fonction two_player, qui va permettre d'avoir 2 joueurs
        self.bordure = self.canvas.create_rectangle(self.width/2, 0, self.width,100, fill = '',width = 4, outline = 'black') #On crée une bordure réactive autour de l'onglet 2 joueurs
        self.canvas.tag_bind(self.bordure, "<Enter>", self.chgt_bordure) #On lui associe la fonction chgt_bordure, qui va permettre de changer la couleur de la bordure

        self.deux_jou_text = self.canvas.create_text(584, 50, text="2 joueurs", font=("Segoe Print", 20), fill="white", state = 'disabled') #On affiche le texte 2 joueurs sur le bouton à cliquer

        #On crée un menu déroulant, qui va permettre de choisir le bot
        self.choix_bot_un = tk.OptionMenu(self.root, self.bot_un, *self.bots_afficher)
        self.menu_place_un = self.canvas.create_window(400, 250, window=self.choix_bot_un)

        #On ajoute tous les nouveaux widgets dans la liste des widgets
        self.widgets_liste.append(self.deux_jou)
        self.widgets_liste.append(self.deux_jou_text)
        self.widgets_liste.append(self.bordure)
        self.widgets_liste.append(self.menu_place_un)

        #On change la variable multi, qui va permettre de savoir que l'on est en mode 1 joueur
        self.multi = False


    def retour_menu(self, event):
        """Fonction permettant de retourner au menu principal"""

        self.clear() #On efface tous les widgets
        self.create_widget() #On crée tous les widgets du menu principal

    def main_menu(self, event):
        """Fonction permettant de retourner au menu principal, alors qu'une partie est en cours"""
        self.compte = False #On arrête le compte à rebours, s'il est en cours
        self.clear() #On efface tous les widgets
        if self.njoueurs >= 1 : #On reset les serpents s'ils existent
            self.snk1.reset() 
        if self.njoueurs == 2 : 
            self.snk2.reset() 
        self.njoueurs = 1 #On remet le nombre de joueurs à 1, comme il est au début
        self.multi = False #On remet la variable multi à False, comme elle est au début
        self.create_widget() #On crée tous les widgets du menu principal

    def fin(self):
        """Fonction permettant de gérer la fin de la partie, quand tous les serpents sont arrêtés, en permettant au joueur de relancer une partie ou d'enregistrer sa partie'"""

        if not (self.snake1) and not (self.snake2): #Si les deux serpents sont déclarés comme arrêtés
            self.boutons_fin() #On crée les boutons de fin de partie : rejouer et enregistrer

    def boutons_fin(self): 
        """Fonction permettant de créer les boutons de fin de partie : rejouer et enregistrer"""

        self.bouton_create(675, 200, self.rejouer_image, self.start) #On crée le bouton pour rejouer, qui relance la même partie directement
        self.bouton_create(88,340,self.enregister_image,self.saisir_titre) #On crée le bouton pour enregistrer la partie, en saisissant un titre
        self.njoueurs = 1 #On remet le nombre de joueurs à 1, comme il est au début

    def save(self,event = ''):
        """Fonction permettant de sauvegarder la partie, en appelant la fonction save_moves de la classe Snake, en nommant le fichier avec le titre saisi par le joueur"""

        titre = self.champ_saisie.get() #On récupère le titre saisi par le joueur
        if titre.strip() == "": #Si le titre est vide
            messagebox.showerror("Erreur", "Le titre ne peut pas être vide.") #On affiche une erreur
            self.fen_titre.destroy() #On détruit la fenêtre de saisie du titre
            self.saisir_titre() #On rappelle la fonction saisir_titre, pour que le joueur puisse saisir un titre valable

        else: #Si le titre n'est pas vide
            messagebox.showinfo("Confirmation", "le titre de votre sauvegarde est : " + titre) #On affiche une confirmation
            self.fen_titre.destroy() #On détruit la fenêtre de saisie du titre

            if len(self.commande) == 1: #Si le serpent 1 uniquement est en jeu
                self.snk1.save_moves(titre) #On appelle la fonction save_moves de la classe Snake, pour sauvegarder les mouvements du serpent 1 
            if len(self.commande) == 2: #Si le serpent 2 est en jeu 
                if self.snk1.lose_time > self.snk2.lose_time: #On regarde quel serpent est le plus long, et donc a duré plus longtemps, et on enregistre son fichier, contenant également l'autre serpent en entier
                    self.snk1.save_moves(titre)
                else:
                    self.snk2.save_moves(titre) #On appelle la fonction save_moves de la classe Snake, pour sauvegarder les mouvements du serpent 2 dans le même fichier

    def saisir_titre(self,event = ""):
        """Fonction permettant de créer une fenêtre de saisie du titre, pour que le joueur puisse nommer sa sauvegarde"""

        self.fen_titre = tk.Tk() #On crée une fenêtre 
        self.fen_titre.title("Saisir un titre") #On indique à quoi sert la fenêtre
    
        self.label_choix_titre = tk.Label(self.fen_titre, text="Entrez un titre:") #On crée un texte pour indiquer au joueur ce qu'il doit faire
        self.label_choix_titre.pack() #On affiche le texte
        
        self.champ_saisie = tk.Entry(self.fen_titre) #On crée un champ de saisie
        self.champ_saisie.pack() #On affiche le champ de saisie
        
        bouton_valider = tk.Button(self.fen_titre, text="Valider", command=self.save) #On crée un bouton pour valider le titre
        bouton_valider.pack() #On affiche le bouton

        self.fen_titre.bind('<Return>',self.save) #On lie la touche entrée à la fonction save, pour que le joueur puisse valider son titre avec la touche entrée
        
        self.fen_titre.mainloop() #On lance la fenêtre
        return 'test' 
    

    def menu_replay(self, event):
        """Fonction permettant de créer le menu de replay, pour que le joueur puisse visionner une partie sauvegardée"""

        self.clear()  # On efface tous les widgets
        
        self.bouton_create(100, 350, self.retour_image, self.retour_menu) #On crée le bouton pour retourner au menu principal

        self.label_replay = self.canvas.create_text(400,80,text='Choisissez la sauvegarde que vous souhaitez visionner',font= "Helvetica 18 bold" ) #On crée un texte pour indiquer au joueur comment marche le replay

        self.replay_dir = 'saves' #On indique le dossier où sont stockées les sauvegardes

        #On crée ici l'emplacement où nous pourrons choisir le fichier à visionner
        self.listbox_replay = tk.Listbox(self.root, width=40) #On crée l'emplacement où afficher ces fichiers, avec le widget listbox de tkinter
        #On va remplir cette liste avec les fichiers présents dans le dossier de sauvegarde
        for filename in os.listdir(self.replay_dir): #On parcourt tous les fichiers présents dans le dossier de sauvegarde
            self.listbox_replay.insert(tk.END, filename) #On ajoute le nom du fichier à la liste
        window_listbox_replay = self.canvas.create_window(320,200,window = self.listbox_replay) #On affiche la liste dans le canvas


        self.button_replay = tk.Button(self.root, text="Sélectionner le fichier", command=self.select_file) #On crée un bouton pour sélectionner le fichier à visionner
        window_button_replay = self.canvas.create_window(365,300,window = self.button_replay) #On affiche le bouton dans le canvas

        self.button_effacer = tk.Button(self.root, text="Effacer", command=self.efface) #On crée un bouton pour effacer le fichier sélectionné
        window_button_effacer = self.canvas.create_window(270,300,window = self.button_effacer) #On affiche le bouton dans le canvas

        #On ajoute tous les widgets à la liste des widgets
        self.widgets_liste.append(self.label_replay)
        self.widgets_liste.append(window_listbox_replay)
        self.widgets_liste.append(window_button_replay)    
        self.widgets_liste.append(window_button_effacer)

    def efface(self):
        """Fonction permettant d'effacer le fichier sélectionné"""

        selected_index = self.listbox_replay.curselection() #On récupère l'index du fichier sélectionné dans la liste
        file_path = "saves/"+self.listbox_replay.get(tk.ACTIVE) #On récupère le chemin du fichier sélectionné

        try: #On essaie de supprimer le fichier
            os.remove(file_path) #On supprime le fichier
            print(f"Fichier supprimé : {file_path}") #On affiche un message de confirmation
            self.listbox_replay.delete(selected_index) #On supprime le fichier de la liste d'affichage

        except FileNotFoundError: #Si le fichier n'existe pas 
            self.message(f"Le fichier {file_path} n'existe pas.") #On affiche un message d'erreur
        except PermissionError: #Si on n'a pas la permission de supprimer le fichier
            self.message(f"Impossible de supprimer le fichier {file_path}. Permission refusée.") #On affiche un message d'erreur
        except Exception as e: #Si une autre erreur survient
            self.message(f"Une erreur est survenue lors de la suppression du fichier {file_path}: {str(e)}") #On affiche un message d'erreur

    def message(self,message):
        """Fonction permettant d'afficher un message d'erreur"""

        messagebox.showerror('Erreur',message) #On affiche une fenêtre d'erreur avec le message passé en paramètre

    def select_file(self):
        """Fonction permettant de sélectionner le fichier à visionner"""

        selected_file = self.listbox_replay.get(tk.ACTIVE) #On récupère le nom du fichier sélectionné
        self.fichier_replay = os.path.join(self.replay_dir, selected_file) #On récupère le chemin du fichier sélectionné, et on le stocke dans une variable
        self.bouton_create(650, 350, self.jouer_image, self.replay) #On crée le bouton pour lancer le replay


    def replay (self, event):
        """Fonction permettant de lancer le replay"""

        self.clear() #On efface tous les widgets
        self.njoueurs = 1 #On indique qu'il n'y a qu'un joueur
        self.start(None, True) #On lance la partie, en indiquant le mode replay
                   
    def start(self,event, replay_mode = False):
        """Fonction permettant de lancer la partie, avec un paramètre replay_mode qui permet de passer en mode replay"""

        self.clear() #On efface tous les widgets

    
        self.compte = True #On indique que l'on peut lancer le compte à rebours
        self.jeu = True #On indique que le jeu est lancé
        size = (20, 20) #Taille du plateau, en nombre de cases
        square_size = 20 #Taille d'une case, et d'un bout de serpent
        map_size = ((size[0])*square_size, (size[1])*square_size) #Taille de la carte, qui permettra d'afficher toutes les cases


        self.game_area=tk.Canvas(self.root, width=map_size[0]+20, height=map_size[1]+20, bg="ivory") #On crée la zone de jeu, où l'on affichera le serpent, il fait la taille de la carte, avec une marge pour être sûr que tout est affiché
        self.fenetre_jeu = self.canvas.create_window(self.width/2,self.height/2, window=self.game_area) #On affiche la zone de jeu dans le canvas
        self.widgets_liste.append(self.fenetre_jeu) #On ajoute la zone de jeu à la liste des widgets
 
        self.bouton_create(675, 340, self.menu_image, self.main_menu) #On crée le bouton pour revenir au menu principal si on veut arrêter la partie

        if replay_mode: #On regarde si on est en mode replay
            Bot1 = Final_bot(size) #On crée un bot
            self.snk1 = Snake([[(2, 2), 0]],size,square_size,self,'astar',Bot1,self.njoueurs,self.vitesse[self.speed.get()], False) #On crée le serpent
            self.snk1.running = True #On indique que le serpent est en train d'être joué
            self.snk1.replay(self.fichier_replay)  #On lance le replay via la méthode replay du serpent
        else: #Si on est en mode classique
            self.chemin_bouton = self.canvas.create_image(self.width - 165, 50, image=self.chemin_image, anchor= tk.NW)
            self.canvas.tag_bind(self.chemin_bouton, '<Button-1>', self.parametre_chemin)
            self.widgets_liste.append(self.chemin_bouton)
            if not self.multi: #On regarde combien de joueurs il y a, et on crée une liste avec les bots qui seront utilisés
                self.commande = [self.bots[self.bot_un.get()]]
            else : 
                self.commande = [self.bots[self.bot_un.get()],self.bots[self.bot_deux.get()]]

            self.snake1 = True #On indique que le serpent 1 existe, et on crée le bot correspondant à la commande donnée
            if self.commande[0] == 'theo':
                Bot1 = BotInt(size)
            if self.commande[0] == 'Astar':
                Bot1 = Final_bot(size,'Astar')
            if self.commande[0] == 'Killer':
                Bot1 = Final_bot(size,'Killer')
            if self.commande[0] == 'Smart':
                Bot1 = Final_bot(size,'Smart')
            if self.commande[0] == 'player':
                Bot1 = Player(1) 
            self.snk1 = Snake([[(2, 2), 0]],size,square_size,self,self.commande[0],Bot1,self.njoueurs, self.vitesse[self.speed.get()], self.chemin_display) #On crée le serpent 1
            
            if self.commande[0] == 'player' : #Si le joueur 1 est un humain, on lui donne la main
                Bot1.bind(self)
            self.snk1.input(self.snk1) 




            if len(self.commande) == 2: #Si il y a un deuxième joueur
                self.njoueurs += 1 #On change le numéro du serpent
                self.snake2 = True #On indique que le serpent 2 existe, et on crée le bot correspondant à la commande donnée
                if self.commande[1] == 'theo':
                    Bot2 = BotInt(size)
                if self.commande[1] == 'Astar':
                    Bot2 = Final_bot(size,'Astar')
                if self.commande[1] == 'Killer':
                    Bot2 = Final_bot(size,'Killer')
                if self.commande[1] == 'Smart':
                    Bot2 = Final_bot(size,'Smart')
                if self.commande[1] == 'player':
                    Bot2 = Player(2)
                self.snk2 = Snake([[(size[0]-2, size[1]-2), 0]],size,square_size,self,self.commande[1],Bot2,self.njoueurs, self.vitesse[self.speed.get()], self.chemin_display) #On crée le serpent 2
                
                if self.commande[1] == 'player' : #Si le joueur 2 est un humain, on lui donne la main
                    Bot2.bind(self)
                self.snk2.input(self.snk2)

            self.countdown = self.game_area.create_text((map_size[0]+20)/2, (map_size[1]+20)/2, text = "3", font = ("Helvetica", 32), fill = "black") #On crée un compte à rebours
            self.countdown_debut(3)
       

        

            if len(self.commande) > 1: #Si il y a deux joueurs, on donne à chaque serpent les informations (position) de l'autre
                self.snk1.input(self.snk2)
                self.snk2.input(self.snk1)



        
    def bouton_create(self, x, y, photo, fonction):
        """Fonction permettant de créer un bouton, avec une image, à une position donnée, et une fonction à exécuter lorsqu'on clique dessus"""
        bordure = self.canvas.create_oval(x-63, y-63, x+63, y+63, fill="blue", activeoutline="white", activewidth=4) #On crée une bordure réactive pour que l'utilisateur sache qu'il faut cliquer le bouton
        bouton = self.canvas.create_image(x, y, image=photo, state = 'disabled')
        self.canvas.tag_bind(bordure, "<Button-1>", fonction)       
        self.widgets_liste.append(bordure)
        self.widgets_liste.append(bouton)

    def countdown_debut(self, chiffre):
        """Fonction permettant de lancer un compte à rebours jusqu'à 0, puis d'afficher GO !, en partant d'un chiffre donné"""
        if self.compte : #Permet de savoir s'il faut continuer le compte à rebours ou non
            if chiffre > 0 : #Si le chiffre est supérieur à 0, on affiche le chiffre, et on relance la fonction avec un chiffre inférieur en attendant 1 seconde
                self.game_area.itemconfig(self.countdown, text = str(chiffre))
                self.root.after(1000, self.countdown_debut, chiffre-1)
            if chiffre == 0 : #Si le chiffre est égal à 0, on affiche GO !, et on relance la fonction avec un chiffre inférieur, et on attend une demi-seconde
                self.game_area.itemconfig(self.countdown, text = "GO !")
                self.root.after(500, self.countdown_debut, chiffre-1)
            if chiffre == -1 : #Si on a -1, c'est que le compte à rebours est fini, on le supprime
                self.snk1.timer_debut()
                self.snk1.move() #On lance le mouvement du serpent 1
                self.game_area.delete(self.snk1.temp_head)
                if self.multi :
                    self.snk2.timer_debut()
                    self.snk2.move() #On lance le mouvement du serpent 2
                    self.game_area.delete(self.snk2.temp_head)
                self.game_area.delete(self.countdown)






menu = Menu()
menu.root.mainloop()