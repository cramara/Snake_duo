from random import randint
from tkinter import*
from tkinter import filedialog
from tkinter import messagebox
import time
import datetime
import csv	
import math as m
import os
from PIL import ImageTk, Image


class Snake :
    """Objet Snake"""
    def __init__(self, posdepart, size, square_size, menu, commande,bot, njoueur, speed, chemin) :
        """Initialise un nouvel objet Snake.

        Arguments:
            posdepart (tuple): Les coordonnées de départ du serpent.
            size (int): La taille de la carte de jeu.
            square_size (int): La taille d'une case sur la carte.
            menu (object): L'objet représentant la fenêtre du jeu.
            commande (object): L'objet de commande pour le serpent.
            bot (bool): Indique si le serpent est contrôlé par l'ordinateur ou un joueur.
            njoueur (int): Le numéro du joueur.
            speed (int): La vitesse du serpent.
            chemin (bool): Indique si le chemin doit être affiché."""
        

        self.menu = menu #Fenetre tkinter, permet de relier le snake avec le menu et ainsi d'échanger des infos
        self.chemin = chemin #Dit si le chemin doit être affiché

        #import des différentes images
        self.image_green_tail = PhotoImage(file="photos/Green_tail.png", master=self.menu.root)
        self.image_orange_tail = PhotoImage(file="photos/Orange_tail.png", master=self.menu.root)
        self.image_red_apple = PhotoImage(file="photos/Red_apple.png", master=self.menu.root)
        self.image_golden_apple = PhotoImage(file="photos/Golden_apple.png", master=self.menu.root)
        self.image_orange_head = Image.open("photos/orange_head.png")
        self.image_green_head = Image.open("photos/green_head.png")


        #Création d'un dictionnaire pour stocker les images de la tête tournées
        self.head_green = {}
        for angle in range(0, 360, 90):
            rotated_img = self.image_green_head.rotate(angle)
            self.head_green[angle] = ImageTk.PhotoImage(rotated_img)

        #Fait de même pour les têtes oranges
        self.head_orange = {}
        for angle in range(0, 360, 90):
            rotated_img = self.image_orange_head.rotate(angle)
            self.head_orange[angle] = ImageTk.PhotoImage(rotated_img)

        self.img = [self.head_green, self.head_orange] #Liste contenant les dictionnaires des têtes

        self.njoueur = njoueur #Numéro du joueur (1 ou 2)
        self.open = False #vaut true lorsque le lien entre les 2 snake est créé, cette variable sert à éviter que certaines fonctionnalitées qui ont besoin du lien ne bug
        self.old_apple = (0,0) #ancienne position de la pomme (mis à zéro au départ mais n'a pas d'importance)
        self.size = size #Taille de la map
        self.square_size = square_size #Taille d'une case
        self.running = True #si True alors le jeu est en cours, lorsque le snake s'arrête passe en False
        self.start = posdepart #Position de départ
        self.tail = posdepart #Queue sous la forme [[(x,y), id], [(x,y), id]...]
        self.length = 1 #longueur de la queue
        if njoueur == 1:
            self.direction = 'right' #direction du serpent si joueur 1
        else:
            self.direction = 'left' #direction du serpent si joueur 2 
        self.apple = [(3,5), 0] #Pomme sous la forme [(x,y), id]
        self.apple = [(randint(5, 10), randint(5, 10)), 0] #(position, id), au départ la pomme apparait au centre pour faciliter le début (mise en place des doigts sur les touches etc...)
        self.apple[1] = self.disp_oval(self.apple[0][0], self.apple[0][1], self.njoueur) #dessin de la première pomme
        self.has_eaten = False #initialisation (vaut True lorsque le serpent mange une pomme)
        self.moves_history = [] #initialise la liste qui récupère les mouvements
        self.path_id = [] 
        self.distance = [-1,m.sqrt((self.tail[0][0][0]-self.apple[0][0])**2+(self.tail[0][0][1]-self.apple[0][1])**2)] #initialise la valeur de distance
        self.commande = commande #permet de savoir qui joue (Intermédiaire, Astar, Killer, Smart, Joueur)
        self.bot = bot #l'objet bot ou joueur qui est relié au serpent
        self.other_tail = [] #initialise la queue de l'autre snake
        self.other_apple = self.apple #initialise la queue de l'autre snake (on a mit la valeur de l'autre pomme mais pas d'importance)
        self.tailes = [self.tail[0][0]] #initialise tailes qui est un liste de l'ensemble des queue / obstacles
        self.speed = speed #vitesse du jeu = vitesse d'actualisation
        self.lose_time = 0 #temps au moment de la défaite
        self.temps_debut = 0 #temps au moment du début de la partie
        self.debut_affich() 
        self.disp_margin()



    def debut_affich(self):
        '''
        Méthode pour créer l'affichage nécessaire au début du jeu.
        '''
        self.img = [self.head_green, self.head_orange]
        self.score = self.menu.canvas.create_text(35, 80+25*self.njoueur, text = 'Score : '+str(self.length-1), anchor = 'nw', font = ('Arial', 12), fill = 'white')
        self.menu.widgets_liste.append(self.score)
        self.tick = self.menu.canvas.create_image(10, 80+25*self.njoueur, anchor="nw", image=self.img[self.njoueur-1][270])
        self.menu.widgets_liste.append(self.tick)

        if self.njoueur == 1 :
            self.menu.timer = self.menu.canvas.create_text(10, 30, text = 'Temps : 0', anchor = 'nw', font = ('Arial', 12), fill = 'white')
            self.menu.widgets_liste.append(self.menu.timer)

            
            self.temp_head = self.disp_head(self.start[0][0][0], self.start[0][0][1], self.head_green, self.direction)
        
        else :
            self.temp_head = self.disp_head(self.start[0][0][0], self.start[0][0][1], self.head_orange, self.direction)  

                                                  
        
    def colision(self,x1,x2,y1,y2):
        '''
        Fonction qui détermine si deux objets entrent en collision.

        Paramètres:
            x1 (int): Coordonnée x du premier objet.
            x2 (int): Coordonnée x du deuxième objet.
            y1 (int): Coordonnée y du premier objet.
            y2 (int): Coordonnée y du deuxième objet.

        Retourne:
            bool: True si les objets entrent en collision, False sinon.
    '''
        if x1 == x2 and y1 == y2:
            return True
        else:
            return False
        
    def colision_die(self):
        '''
        Fonction qui indique si le snake entre en collision avec sa queue ou un mur (doit mourir).

        Retourne:
        bool: True si le snake entre en collision, False sinon.
        '''
        if self.tail[0][0][0] < 0 or self.tail[0][0][0] >= self.size[0] or self.tail[0][0][1] < 0 or self.tail[0][0][1] >= self.size[1] :
            return True
        if self.tail[0][0] in [self.tail[i][0] for i in range(2, self.length)] :
            return True
        if self.tailes[0] in self.tailes[1:] :
            return True
        return False    

    def bbot(self):
        '''
        Méthode pour effectuer le déplacement du snake contrôlé par le bot.
        '''
        self.bot.actualisation(self.tail, self.apple,self.tailes,self.other_tail,self.dir_other,self.other_apple)
        self.change_direction(self.bot.moove())
        self.disp_path()

    def theo(self):
        '''
        Méthode pour effectuer le déplacement du snake contrôlé par le bot (stratégie "theo").
        '''
        self.bot.actualisation(self.tail, self.apple, self.tailes, self.other_apple)
        self.change_direction(self.bot.moove())


    def player(self):
        '''
        Méthode pour effectuer le déplacement du snake contrôlé par le joueur.
        '''
        self.direction = self.bot.get_direction()

    def input(self, other):
        '''
        Méthode pour récupérer les informations de l'autre joueur et mettre à jour les variables.

        Arguments:
        other (SnakeGame): Instance du jeu de l'autre joueur.
        '''
        if other == self:
            self.tailes = [i[0] for i in self.tail]
            self.other = other #dans ce cas c'est le même vu que le joueur est seul
            self.dir_other = other.direction #meme chose, juste pour ne pas avoir de problème avec les variables
        else:
            self.other = other
            self.dir_other = other.direction
            self.other_tail = [i[0] for i in other.tail]
            self.mini_tail = [i[0] for i in self.tail]
            self.other_apple = other.apple[0]
            for i in self.other_tail:
                self.mini_tail.append(i)
            self.tailes = self.mini_tail
        self.open = True #permet de savoir si on a déjà fait la fonction input ou pas


    def timer_debut(self):
        self.temps_debut = time.time() #debut du jeu


    def timer_refresh(self):
        '''
        Méthode pour rafraîchir le timer affiché.

        Calcul le temps écoulé depuis le début du jeu et met à jour le texte du timer.
        '''
        if self.menu.timer in self.menu.widgets_liste:
            self.menu.widgets_liste.remove(self.menu.timer)
            self.menu.canvas.delete(self.menu.timer)
            self.menu.timer = self.menu.canvas.create_text(10, 30, text = 'Temps : '+str(round(time.time() - self.temps_debut, 2)), anchor = 'nw', font = ('Arial', 12), fill = 'white')
            self.menu.widgets_liste.append(self.menu.timer)

    def move(self) :
        """
        Fonctionnement du serpent : déplacement,  manger, perdre, c'est la fonction principale du snake, elle est appellée en boucle jusqu'à la mort du serpent
            
        """
        
        if self.running : #s'execute tant que le snake est en vie 
            
            if self.colision_die(): #vérifie que le snake n'est pas dans un mur ou dans un corps
                self.lose() #si oui, lance la fonction lose 

            if self.open:# si un échange à déjà était fait, open = True pour le reste de la partie
                self.input(self.other) #prend les valeurs de leurs snake (queue, pomme et direction)
            if not self.has_eaten : #si le serpent n'est pas entrain de manger
                                    #alors on le fait avancer normalement
                self.menu.game_area.delete(self.tail[-1][1]) #on enlève le dernier élément de sa queue
                if self.length > 1 :
                    for i in range(self.length-1, 0, -1) :
                        self.tail[i] = self.tail[i-1].copy()
            else :  #si le serpent à mangé, il faut le faire grandir donc on se déplace mais sans supprimer la fin
                self.tail.append(self.tail[-1].copy())
                self.length += 1
                if self.length > 2 :
                    for i in range(self.length-2, 0, -1) :
                        self.tail[i] = self.tail[i-1].copy()
                self.has_eaten = False #on remet la valeur de "a mangé" à False
            if 'Killer' in self.commande or 'Astar' in self.commande or 'Smart' in self.commande :
                self.bbot() #si le controle du serpent est prit par un bot du type lecture de graphe
            if 'theo' in self.commande:
                self.theo() #si le controle du serpent est prit par un bot du type lecture basique
            if 'player' in self.commande:
                self.player() #si le controle du serpent est prit par un joueur

            
            #modifie la position de la tête et du dernier bout de queue en fonction de la direction
            if self.direction == 'up' :
                self.tail[0][0] = (self.tail[0][0][0], self.tail[0][0][1]-1)
            elif self.direction == 'down' :
                self.tail[0][0] = (self.tail[0][0][0], self.tail[0][0][1]+1)
            elif self.direction == 'left' :
                self.tail[0][0] = (self.tail[0][0][0]-1, self.tail[0][0][1])
            elif self.direction == 'right' :
                self.tail[0][0] = (self.tail[0][0][0]+1, self.tail[0][0][1])
            elif self.direction == None :#si jamais le bot renvoi None (n'est pas sensé arriver)
                print('Mort par bug')
                self.lose()

            if self.colision(self.apple[0][0],self.tail[0][0][0],self.apple[0][1],self.tail[0][0][1]): #condition qui permet de faire manger le serpent lorsqu'il est sur un pomme
                self.eat()
                self.has_eaten = True #la valeur de "a mangé" est mise à True

            if self.colision(self.other_apple[0],self.tail[0][0][0],self.other_apple[1],self.tail[0][0][1]): #condtion qui permet de savoir si le serpent a mangé la pomme adverse
                self.eat_other() 

        
            if self.njoueur == 2: #si c'est le joueur 2 qui maîtrise ce snake
                self.tail[0][1] = self.disp_head(self.tail[0][0][0], self.tail[0][0][1],self.head_orange, self.direction) #met une image de tête au début du serpent
                if len(self.tail) > 1:
                    self.menu.game_area.delete(self.tail[1][1])
                    self.tail[1][1] = self.disp_tail(self.tail[1][0][0], self.tail[1][0][1], self.image_orange_tail) #met une image de queue en deuxième position
            else: #si c'est le joueur 1 qui maîtrise ce snake
                self.tail[0][1] = self.disp_head(self.tail[0][0][0], self.tail[0][0][1],self.head_green, self.direction) #met une image de tête au début du serpent
                if len(self.tail) > 1:
                    self.menu.game_area.delete(self.tail[1][1])
                    self.tail[1][1] = self.disp_tail(self.tail[1][0][0], self.tail[1][0][1], self.image_green_tail) #met une image de queue en deuxième position

            #gère la sauvegarde de la postion de la queue du snake
            self.moves_history.append(self.append_move())

            #gere affichage score
            self.disp_score()

            #gere affichage timer
            if self.menu.snk1.running and self.njoueur == 1:
                self.timer_refresh()
            elif not (self.menu.snk1.running) and self.njoueur == 2:
                self.timer_refresh()

            self.menu.root.after(self.speed, self.move) #rappelle en boucle la fonction move, delais d'attente variable en fonction de la vitesse
                

    def change_direction(self, direction_target) :
        """
        Cette fonction empêche la snake d'aller derière lui

            Paramètre : 
                - direction cible
            """
        
        if self.direction == 'up' and direction_target != 'down' :
            self.direction = direction_target
        elif self.direction == 'down' and direction_target != 'up' :
            self.direction = direction_target
        elif self.direction == 'left' and direction_target != 'right' :
            self.direction = direction_target
        elif self.direction == 'right' and direction_target != 'left' :
            self.direction = direction_target
        elif self.direction == '' :
            self.direction = direction_target


    def eat(self) :
        """
        Cette fonction fait manger la pomme 
        """
        
        self.menu.game_area.delete(self.apple[1])
        self.apple[0] = self.new_apple() 
        self.apple[1] = self.disp_oval(self.apple[0][0], self.apple[0][1], self.njoueur)


    def eat_other(self):
        """
        Fonction qui est appelé si la pomme du serpent adverse est mangée
            Dans ce cas le serpent ne gagne pas de point
        """
        
        self.menu.game_area.delete(self.other.apple[1])
        self.other.apple[0] = self.new_apple()
        self.other.apple[1] = self.disp_oval(self.other.apple[0][0], self.other.apple[0][1], self.other.njoueur)


    def new_apple(self):
        """
        Gérnération d'une nouvelle pomme avec vérification qu'on est ni sur un serpent, ni sur une pomme, ni sur l'ancienne pomme

        Input : coordonnées du serpent, taille de la map
        Output : nouvelle pomme
        """
    
        apple = (randint(1, self.size[0]-2), randint(1, self.size[1]-2))
        if self.open:

            if apple in [self.tail[i][0] for i in range(1, self.length)] or apple in self.start or apple in [self.other.tail[i][0] for i in range(1, self.other.length)] or apple == self.other_apple  or apple == self.old_apple:
                

                return self.new_apple()
            else :
                self.old_apple = apple
                return apple
        else: 
            if apple in [self.tail[i][0] for i in range(1, self.length)] or apple in self.start  or apple == self.old_apple:
                return self.new_apple()
            else :
                self.old_apple = apple
                return apple
            

    def disp_path(self) :
        """
        Affichage graphique du chemin prévu par le bot
        """
        if (self.commande == 'Astar' or self.commande == 'Killer' or self.commande == 'Smart') and self.chemin and self.bot.path != None :
            for i in range(len(self.path_id)):
                self.menu.game_area.delete(self.path_id[i][1])
            
            path = self.bot.path
            self.path_id = []
            for i in range(len(path)):
                if (path[i][0], path[i][1]) != (self.apple[0][0], self.apple[0][1]) and self.chemin:
                    self.path_id.append([(path[i][0], path[i][1]), self.disp_rect(path[i][0], path[i][1], 'lightblue', 2)]) #affichage sous forme de carrés bleus       


    def append_move(self) :
        """
        Renvoie la liste des queues et des pommes du tour actuel pour être ajoutée à l'historique des moves
            Chaque joueur est sous la forme : [nom, direction, pomme, queue1, queue2, ...]
        """

        #Joueur
        to_append_snk1 = [self.direction, self.apple[0][0], self.apple[0][1]]
        for i in self.tail :
            to_append_snk1.append(i[0][0])
            to_append_snk1.append(i[0][1])

        #Adversaire
        to_append_snk2 = []
        if self.dir_other == '':
            to_append_snk2.append(self.direction)
        else :
            to_append_snk2.append(self.dir_other)
        to_append_snk2.append(self.other.apple[0][0])
        to_append_snk2.append(self.other.apple[0][1])
        for i in self.other.tail :
            to_append_snk2.append(i[0][0])
            to_append_snk2.append(i[0][1])

        #On réunit les deux, toujours avec le joueur 1 en premier
        to_append = ["snk1"]
        if self.njoueur == 1 :
            to_append += to_append_snk1
            to_append.append("snk2")
            to_append += to_append_snk2
        else :
            to_append += to_append_snk2
            to_append.append("snk2")
            to_append += to_append_snk1

        return to_append


    def save_moves(self, titre) :
        """
        Sauvegarde des mouvements dans un fichier csv
            Chaque ligne correspond à un tour sous la forme décris dans append_move

        Input : nom du fichier à créer, historique des moves
        Output : création du fichier csv associé à la partie
        """

        #Sauvegarde du replay
        now = datetime.datetime.now()
        print('again',os.path.exists('saves/'+titre+'.csv'))
        if os.path.exists('saves/'+titre+'.csv'):
            file_name = titre +'_'+ str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '-' + str(now.hour) + ';' + str(now.minute) + ';'+ str(now.second) + '-' + str(self.length) + '.csv'
            messagebox.showerror("Erreur", "Le titre exitant déjà le nom du fichier à été mofifier en rajoutant la date à la suite du titre. Le nouveau nom de la sauvegarde est : "+file_name)
        else:
            file_name = titre+'.csv'
        with open('saves/'+file_name, 'w', newline="", encoding='UTF8') as file :
            file.truncate()
            writer = csv.writer(file)
            writer.writerows(self.moves_history)
        print("Moves saved !")

    def create_rectangle(self,x,y,a,b,**options): 
        """
        Permet de créer un rectangle de (x,y) à (a,b) avec des options telles que l'opacité
        """
        if 'alpha' in options:
            self.image = []
            # Calculate the alpha transparency for every color(RGB)
            alpha = int(options.pop('alpha') * 255)
            # Use the fill variable to fill the shape with transparent color
            fill = options.pop('fill')
            fill = self.menu.root.winfo_rgb(fill) + (alpha,)
            self.image_opaque = Image.new('RGBA', (a-x, b-y), fill)
            self.image_affich = ImageTk.PhotoImage(self.image_opaque)

            self.menu.widgets_liste.append(self.menu.game_area.create_image(x, y, image=self.image_affich, anchor='nw', state = 'disable'))


    def lose(self) :
        """
        Défaite

        Input : coordonnées du serpent, longueur du serpent, coordonnées de la pomme
        Output : affichage du score et du gagnant, arrêt du jeu (suppression sur le canevas)
        """

        self.chemin = False
        self.lose_time = time.time()-self.temps_debut
        self.running = False

        #On dit que le serpent est mort
        if self.njoueur == 1 :
            self.menu.snake1 = False
        if self.njoueur == 2 :
            self.menu.snake2 = False

        if not self.menu.snake1 and not self.menu.snake2: #Si les deux serpents sont morts
            self.create_rectangle(0, 0, self.size[0]*self.square_size+25, self.size[1]*self.square_size+25, fill='white', alpha=0.5) #Fond blanc transparent
            #On associe chaque serpent à sa couleur
            if self.njoueur == 1 :
                self.vert = self.length
                self.orange = self.other.length
            else :
                self.vert = self.other.length
                self.orange = self.length

            #On regarde qui a gagné et on l'affiche
            if self.vert == self.orange and self != self.other: #Si les deux serpents sont de même taille, mais différents
                self.egalite = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 -20, text='Egalité ! \nRien ne sert de courir, \nil faut partir à point.', font=("Helvetica", 22), fill='black', justify='center')
                self.score_affich = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 +50, text=f'Score : {self.length-1}', font=("Helvetica", 22), fill='black')
            elif self.vert == self.orange and self == self.other: #Si on a un seul serpent
                self.lose_affich = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 -20, text=f'Tu as perdu !', font=("Helvetica", 22), fill='black')
                self.score_affich = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 +20, text=f'Score : {self.length-1}', font=("Helvetica", 22), fill='black')
           
           
            elif self.vert > self.orange: #Si le serpent vert est plus grand
                self.loser = ImageTk.PhotoImage(((Image.open("photos/orange_head.png")).resize((15, 15), Image.ANTIALIAS)).rotate(270))
                self.message_vict = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 -20, text='Le serpent vert gagne !', font=("Helvetica", 22), fill='black')
                self.win_tick = self.menu.game_area.create_image((self.size[0]*self.square_size+20)/2-90, (self.size[1]*self.square_size+20)/2+21, image=self.head_green[270])
                self.win_score = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2+20, text=f'Score : {self.vert-1}', font=("Helvetica", 22), fill='black')
                self.lose_tick = self.menu.game_area.create_image((self.size[0]*self.square_size+20)/2-70, (self.size[1]*self.square_size+20)/2+51, image=self.loser)           
                self.lose_score = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2+50, text=f'Score : {self.orange-1}', font=("Helvetica", 14), fill='black')
            
            elif self.orange > self.vert: #Si le serpent orange est plus grand
                self.loser = ImageTk.PhotoImage(((Image.open("photos/green_head.png")).resize((15, 15), Image.ANTIALIAS)).rotate(270))
                self.message_vict = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2 -20, text='Le serpent orange gagne !', font=("Helvetica", 22), fill='black')
                self.win_tick = self.menu.game_area.create_image((self.size[0]*self.square_size+20)/2-90, (self.size[1]*self.square_size+20)/2+21, image=self.head_orange[270])
                self.win_score = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2+20, text=f'Score : {self.orange-1}', font=("Helvetica", 22), fill='black')
                self.lose_tick = self.menu.game_area.create_image((self.size[0]*self.square_size+20)/2-70, (self.size[1]*self.square_size+20)/2+51, image=self.loser)           
                self.lose_score = self.menu.game_area.create_text((self.size[0]*self.square_size+20)/2, (self.size[1]*self.square_size+20)/2+50, text=f'Score : {self.vert-1}', font=("Helvetica", 14), fill='black')


        self.menu.fin()
        

    def reset(self) :
        """
        Réinitialisation du serpent
        """

        for coord, ident in self.tail :
            self.menu.game_area.delete(ident)
        self.tail = []
        self.length = 0
        self.running = False


    def replay(self, file_name) :
        """
        Mode replay
            Affichage d'une partie sauvegardée par lecture du fichier csv correspondant
            Forme décrite dans append_move()

        Input : nom du fichier à lire
        Output : affichage graphique
        """
        self.timer_debut()
        with open(file_name, 'r', encoding='UTF8') as file :
                #Initialisation score
                self.menu.widgets_liste.remove(self.score)
                self.menu.canvas.delete(self.score)
                self.tick1 = self.menu.canvas.create_image(10, 105, anchor="nw", image=self.img[self.njoueur-1][270])
                self.menu.widgets_liste.append(self.tick1)
                self.score1 = self.menu.canvas.create_text(35, 105, text = 'Score : 0', anchor = 'nw', font = ('Arial', 12), fill = 'white')
                self.menu.widgets_liste.append(self.score1)
                self.tick2 = self.menu.canvas.create_image(10, 130, anchor="nw", image=self.img[self.njoueur-1][270])
                self.menu.widgets_liste.append(self.tick2)
                self.score2 = self.menu.canvas.create_text(35, 130, text = 'Score : 0', anchor = 'nw', font = ('Arial', 12), fill = 'white')
                self.menu.widgets_liste.append(self.score2)

                same_snakes = False #Affectée à True si les deux serpents sont les mêmes

                #Lecture du fichier
                reader = csv.reader(file)
                for row in reader :
                    if self.running :
                        snk1 = []
                        snk2 = []
                        #Séparation des deux serpents
                        for i in range(1, len(row)) :
                            if row[i] == "snk2" :
                                snk1 = row[1:i]
                                snk2 = row[i+1:]
                                break
                        
                        same_snakes = (snk1[1:] == snk2[1:])

                        #Affichage du serpent 1
                        self.menu.game_area.delete("all") #suppression des éléments du canvas
                        self.disp_margin()
                        dir_snk1 = snk1[0]
                        self.disp_oval(int(snk1[1]), int(snk1[2]), 1)
                        self.disp_head(int(snk1[3]), int(snk1[4]), self.head_green, dir_snk1)
                        for i in range(5, len(snk1), 2) :
                            self.disp_tail(int(snk1[i]), int(snk1[i+1]), self.image_green_tail)

                        if self.score1 in self.menu.widgets_liste:
                            self.menu.widgets_liste.remove(self.score1)
                            self.menu.canvas.delete(self.score1)
                            self.menu.widgets_liste.remove(self.tick1)
                            self.menu.canvas.delete(self.tick1)
                            self.tick1 = self.menu.canvas.create_image(10, 105, anchor="nw", image=self.img[self.njoueur-1][270])
                            self.menu.widgets_liste.append(self.tick1)
                            self.score1 = self.menu.canvas.create_text(35, 105, text = 'Score : '+str(len(snk1)//2-1), anchor = 'nw', font = ('Arial', 12), fill = 'white')
                            self.menu.widgets_liste.append(self.score1)


                        #Affichage du serpent 2 (si différent du 1)
                        if not same_snakes :
                            if self.score2 in self.menu.widgets_liste:
                                self.menu.widgets_liste.remove(self.score2)
                                self.menu.canvas.delete(self.score2)
                                self.menu.widgets_liste.remove(self.tick2)
                                self.menu.canvas.delete(self.tick2)
                            self.tick2 = self.menu.canvas.create_image(10, 130, anchor="nw", image=self.img[1][270])
                            self.menu.widgets_liste.append(self.tick2)
                            self.score2 = self.menu.canvas.create_text(35, 130, text = 'Score : '+str(len(snk2)//2-1), anchor = 'nw', font = ('Arial', 12), fill = 'white')
                            self.menu.widgets_liste.append(self.score2)

                            dir_snk2 = snk2[0]
                            self.disp_oval(int(snk2[1]), int(snk2[2]), 2)
                            self.disp_head(int(snk2[3]), int(snk2[4]), self.head_orange, dir_snk2)
                            for i in range(5, len(snk2), 2) :
                                self.disp_tail(int(snk2[i]), int(snk2[i+1]), self.image_orange_tail)
                        elif self.score2 in self.menu.widgets_liste : 
                            self.menu.widgets_liste.remove(self.score2)
                            self.menu.canvas.delete(self.score2)
                            self.menu.widgets_liste.remove(self.tick2)
                            self.menu.canvas.delete(self.tick2)

                        self.timer_refresh()
                        self.menu.root.after(self.speed, self.menu.root.update()) #rafraichissement à la vitesse choisie


    def disp_rect(self, x, y, color, radius) :
        """
        Affichage d'un rectangle de couleur color et de rayon radius à la position (x, y)
        """

        return self.menu.game_area.create_rectangle(x*self.square_size-radius+20, y*self.square_size-radius+20, x*self.square_size+radius+20, y*self.square_size+radius+20, outline= color, fill=color)


    def disp_tail(self, x, y,image_path) :
        """
        Affichage d'un morceau de queue à la position (x, y) avec l'image image_path
        """

        return self.menu.game_area.create_image(x*self.square_size+11, y*self.square_size+11, anchor="nw", image=image_path)

        
    def disp_oval(self, x, y, numjoueur) :
        """
        Affichage de la pomme à la position (x, y) pour le joueur numjoueur
        """

        if numjoueur == 1 :
            return self.menu.game_area.create_image(x*self.square_size+11, y*self.square_size+11, anchor="nw", image=self.image_red_apple)
        else :
            return self.menu.game_area.create_image(x*self.square_size+11, y*self.square_size+11, anchor="nw", image=self.image_golden_apple)


    def disp_head(self, x, y, img, direction):
        """
        Affiche la tête du serpent à la position (x, y) avec l'orientation définie par direction
        """

        if direction == 'right':
            angle = 0
        elif direction == 'left':
            angle = 180
        elif direction == 'up':
            angle = 90
        else:
            angle = 270
        return self.menu.game_area.create_image(x*self.square_size+11, y*self.square_size+11, anchor="nw", image=img[angle])
    

    def disp_margin(self) :
        """
        Affiche des marges de largeur 10 sur les bords du canvas
        """

        self.menu.game_area.create_rectangle(0, 0, 10, self.size[0]*self.square_size+20, fill='grey', outline='grey')
        self.menu.game_area.create_rectangle(0, 0, self.size[0]*self.square_size+20, 10, fill='grey', outline='grey')
        self.menu.game_area.create_rectangle(self.size[0]*self.square_size+11, 0, self.size[0]*self.square_size+21, self.size[0]*self.square_size+20, fill='grey', outline='grey')
        self.menu.game_area.create_rectangle(0, self.size[0]*self.square_size+11, self.size[0]*self.square_size+20, self.size[0]*self.square_size+21, fill='grey', outline='grey')

    def disp_score(self):
        """Affiche le score du serpent, à côté d'une image de sa tête pour savoir à quel joueur il correspond"""
        self.menu.widgets_liste.remove(self.score)
        self.menu.canvas.delete(self.score)
        self.menu.widgets_liste.remove(self.tick)
        self.menu.canvas.delete(self.tick)

        self.score = self.menu.canvas.create_text(35, 80+25*self.njoueur, text = 'Score : '+str(self.length-1), anchor = 'nw', font = ('Arial', 12), fill = 'white')
        self.menu.widgets_liste.append(self.score)
        self.tick = self.menu.canvas.create_image(10, 80+25*self.njoueur, anchor="nw", image=self.img[self.njoueur-1][270])
        self.menu.widgets_liste.append(self.tick)