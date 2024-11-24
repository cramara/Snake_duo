from queue import PriorityQueue
from random import randint


'''La classe `Bot` représente un robot capable de trouver le chemin le plus court pour atteindre une pomme sur une carte donnée.
Voici une brève description de chaque fonction :

- `__init__(self, taillemap)` : Initialise un objet `Smart_bot` avec la taille de la carte.
- `adjacences(self)` : Crée la liste d'adjacence des cases sur la carte en fonction de la position de la queue.
- `distance(self, point1, point2)` : Calcule la distance euclidienne entre deux points en dimension 2.
- `astar(self, goal)` : Implémente l'algorithme A* pour trouver le plus court chemin vers une pomme.
- `esquive(self)` : Gère l'esquive lorsque le robot est bloqué.
- `new_apple_fake(self)` : Génère une nouvelle pomme qui ne se trouve pas sur le serpent.
- `try_path(self, apple)` : Vérifie s'il existe un chemin vers une pomme donnée.
- `moove(self)` : Détermine le déplacement que le serpent doit effectuer pour atteindre la pomme.
- `actualisation(self, queue, pomme, queue2, pomme2)` : Met à jour les attributs du robot en fonction des nouvelles informations.
'''


class Final_bot:
    '''Classe qui crée un robot'''
    
    def __init__(self, taillemap, type = ""):
        '''
        Initialise un objet de la classe Smart_bot.
        
        Paramètres :
        - taillemap : liste [largeur, hauteur] de la taille de la carte
        '''
        self.adj = {}  # Dictionnaire pour stocker les adjacences des cases
        self.stop = ''  # Variable pour le statut d'arrêt du robot
        self.map = taillemap  # Taille de la carte
        self.bloque = False  # Indicateur de blocage du robot
        self.compteur = 0  # Compteur pour le blocage du robot
        self.type = type #définie le type de robot utilisé parmis (Astar, Killer et Smart)

        
    def adjacences(self):
        '''
        Crée la liste d'adjacence des cases sur la carte en fonction de la position de la queue.
        '''
        
        for x in range(self.map[0]):
            for y in range(self.map[1]):
                self.adj[(x, y)] = []                 
                if (x + 1, y) not in self.new_queue  and x + 1 < self.map[0]:
                    self.adj[(x, y)].append((x + 1, y))
                if (x - 1, y) not in self.new_queue  and x - 1 >= 0:
                    self.adj[(x, y)].append((x - 1, y))
                if (x, y + 1) not in self.new_queue  and y + 1 < self.map[1]:
                    self.adj[(x, y)].append((x, y + 1))
                if (x, y - 1) not in self.new_queue  and y - 1 >= 0:
                    self.adj[(x, y)].append((x, y - 1))
        if self.type == "Killer": #utile que pour le bot Killer
            self.good = [] #liste contenant les cases accessibles 
            for i in self.adj.values(): #ajout des cases accessibles dans self.good
                for y in i:
                    self.good.append(y)
        
    def distance(self, point1, point2):
        '''
        Calcule la distance euclidienne entre deux points en dimension 2.
        
        Paramètres :
        - point1 : tuple (x1, y1) du premier point
        - point2 : tuple (x2, y2) du deuxième point
        
        Retourne :
        - La distance entre les deux points
        '''
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    def front(self,case):
        '''
        Attribue un poids faible à chaque case devant le snake adverse

        Paramètres : 
        - position de la tete du snake adverse
        
        Retourne :
        - poids que doit avoir la case en fonction de sa position par rapport au snake adverse
        '''
        if self.type == 'Killer': #uniquement utile pour le snake de type Killer
            direct = self.other_direction #direction de l'autre snake
            n = 30 #limite qui détermine si une case est devant le snake adverse ou pas
            if case in self.good and len(self.other_tail) > 0: #si la case fait partie des cases accéssibles
                #en fonction de la direction du snake, si la case est devant l'autre snake, sont poids est diminué
                if direct == 'right':#chaque direction à une condition différentes pour trouver les cases devant
                    if self.other_tail[0][0] < case[0] and self.other_tail[0][0]+n > case[0]:#on se limite aux n case devant l'autre snake
                        return -9
                    else:
                        return 0
                elif direct == 'left':
                    if self.other_tail[0][0] > case[0] and self.other_tail[0][0]+n < case[0]:
                        return -9
                    else:
                        return 0
                elif direct == 'up':
                    if self.other_tail[0][1] > case[1] and self.other_tail[0][1]+n < case[0]:
                        return -9
                    else:
                        return 0
                elif direct == 'down':
                    if self.other_tail[0][1] < case[1] and self.other_tail[0][0]+n > case[0]:
                        return -9
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0


    def astar(self,goal):
        '''
        Algorithme A* qui trouve le plus court chemin en orientant la recherche vers la position de la pomme. 
        En utilisant la fonction distance. 
        
        Paramètres :
        - goal : position de la pomme
        
        Retourne :
        - Le chemin que le serpent doit parcourir pour atteindre la pomme
        '''
        if self.in_map(self.queue[0]): #vérifie que la tête est bien dans la carte pour éviter de demander une clé qui n'est pas dans la liste d'adjacence
            frontier = PriorityQueue()  #crée un objet de type Priorityqueue qui donne un priorité à chaque valeur qu'on lui donne (équivalent à une liste de liste)
            frontier.put(self.queue[0], 0) #on ajoute les cordonnées de la queue au debut de la liste avec une priorité de 0 (maximale)
            came_from = {} #initialisation d'un dico qui récupère le chemin pour aller à un point du graphe
            cost_so_far = {} #initialisation de la liste qui gère les poids/priorités à donner 
            came_from[tuple(self.queue[0])] = None #le chemin pour aller à la tête est None car pas de chemin à faire
            cost_so_far[tuple(self.queue[0])] = 0 #Idem pour la cout de la tête qui est nul car la tete est toujours à la tete 
            current = None #initialise la varianle currant (pour pouvoir l'utilisant dans le while)
            while not frontier.empty() and current != goal: #tant qu'on n'est pas arrivé à l'objectif ou que la PriorityQueue n'est pas vide
                current = frontier.get() #on s'interesse maintenant à l'élément ayant la priorité la plus faible
                for next in self.adj[tuple(current)]: #regarde tout les points adjacents à la case dont on s'interesse
                    new_cost = cost_so_far[tuple(current)] + 10*self.distance(current, next) + self.front(next) #ajuste la valeur du poids en fonction de la distance et de l'autre snake dans le cas du snake Killer
                    if next not in cost_so_far or new_cost < cost_so_far[next]: #si la case dont on s'interesse n'est pas dans le chemin (éviter de répasser par une case) ou que le cout est plus faible (donc plus interessant)
                        cost_so_far[next] = new_cost #on met a jour la valeur du cout du chemin en ajoutant le point actuel
                        priority = new_cost + 10*self.distance(goal, next) + self.front(next) #on met le poids de cette nouvelle case 
                        frontier.put(next, priority) #on ajoute cette nouvelle case et son poids dans la PriorityQueue
                        came_from[next] = current #on ajoute au chemin la case actuelle

            # Récupération du chemin utilisé
            path = [goal] #commence le chemin à parcourir par l'objectif (nécessite donc la présence d'un objectif)
            compteur_path = 0 #compte pour éviter que la boucle soit infini quand il n'y a plus de chemin
            while (path[-1] != self.queue[0]) and compteur_path < 401: #si le chemin est vide, sort de la boucle au bout de 500 itération (carte en 20*20 donc chemin max = 400)
                compteur_path += 1
                if came_from is not None : #vérifie que came_from n'est pas vide ce qui équivaut à None
                    if tuple(path[-1]) in came_from : #vérifie que la fin du chemin est bien dans came_from (évite des erreurs pour l'étape d'après)
                        path.append(came_from[tuple(path[-1])]) #ajoute au chemin le dernier élément du chemin du parcours de graphe
                    else: #si rien dans le path = pas de chemin vers la pomme possbiel
                        if self.type == 'Astar' or self.type == 'Killer': #si c'est pas le snake Smart, on laisse le snake mourir
                            self.stop = 'pas de chemin'
                        else:  #sinon on gère le problème en appellant la fonction esquive
                            if not self.bloque: 
                                self.stop = 'pas de chemin'
                                self.esquive()
                                return None
                            else: 
                                return None
            path.reverse() #on inverse le chemin que l'on vient de créer (pour rapelle l'arrivé était en premier et le chemin était prit à l'envers)
            return path #on finit par renvoyer le chemin à suivre (vaut None si pas de chemin possible)
        else :
            return None #renvoi un chemin null pour que le snake meurt sans causer de bug


    def in_map(self, point):
        '''
        Fonction qui dit si un point est dans la carte
        
        Argument:
            -point : liste de 2 coordonnées [x,y]
        Retourne:
            - Booléen : True ou False qui indique si le point est dans la carte
        '''
        if 0<= point[0] <= self.map[0]-1 and 0<= point[1] <= self.map[1]-1:
            return True
        else:
            return False

    def esquive(self):
        '''
        Gère l'esquive lorsque le robot est bloqué.
        '''
        if not self.bloque: #si n'est pas considéré comme bloqué
            self.bloque = True #on le passe comme bloqué car si cette fonction se lance c'est parce qu'il l'est
            self.fake_apple = self.new_apple_fake() #on crée un nouvelle fausse pomme atteignable par le snake
        if self.bloque: #si il est deja considéré comme bloqué
            if self.queue[0] ==  self.fake_apple: #si le serpent arrive sur la fausse pomme
                self.compteur = 0 #on remet ce compteur à zéro (évite la boucle infinie)
                self.fake_apple = self.new_apple_fake() #on remplace l'ancienne fausse pomme par un nouvelle fausse pomme
                


    def new_apple_fake(self):
        '''
        Génère une nouvelle pomme qui ne se trouve pas sur le serpent. 
        Cette fonction n'est utile que pour le snake Smart car elle sert à continuer de faire bouger le snake vers une fasse pomme lorsque celui ci
        n'a plus de chemin vers la vraie pomme
        
        Retourne :
        - Les coordonnées de la nouvelle pomme
        '''
        self.compteur += 1 #utilité du compteur explicité après
        apple = (randint(1, self.map[0]-1), randint(1, self.map[1]-1)) #génère une pomme à une position aléatoire
        if apple in self.new_queue or apple == self.other_apple or not self.try_path(apple): #si cette pomme est dans la queue, sur l'autre pomme ou inaccessible, on en genère une nouvelle
            if self.compteur < 100: #pour eviter de générer en boucle des pommes car le snake est mort donc forcément aucune ne sera accéssible 
                return self.new_apple_fake()
            else : 
                return apple
        else :
            return apple #renvoi les coordonnées de la fausse pomme lorsque toutes les conditions sont rempli
        
    def try_path(self,apple):
        '''
        Vérifie s'il existe un chemin vers la pomme. Script également utile uniquement pour le bot Smart
        
        Paramètres :
        - apple : position de la pomme
        
        Retourne :
        - True s'il existe un chemin, False sinon
        '''
        if self.astar(apple) is not None: 
            return True
        else:
            return False
        
    def moove(self):
        '''
        Trouve le déplacement que le serpent doit effectuer. En fonction du chemin donné par la lecture de graphe
    
        Retourne :
        - Un string indiquant la direction que le serpent doit prendre
        '''
        if self.path != [] and self.path is not None: #lorsque le snake n'a plus de chemin, le path est de type None donc on ne peut pas l'utiliser comme un liste
            if self.path[0][0] > self.queue[0][0]:
                return "right"
            elif self.path[0][0] < self.queue[0][0]:
                return "left"
            elif self.path[0][1] > self.queue[0][1]:
                return "down"
            elif self.path[0][1] < self.queue[0][1]:
                return "up"
            else:
                self.path.pop(0)
                return self.moove()
        else:
            return "up" #lorsque le snake meurt, au lieu de faire planter le script il va dans un direction au pif pour mourir correctement et finir la partie

    def actualisation(self,queue,pomme,queue2,pomme2,other_queue,other_direction):
        '''
        Met à jour les attributs du robot en fonction des nouvelles informations.
    
        Paramètres :
        - queue : liste des coordonnées de la queue du serpent
        - pomme : liste des coordonnées de la pomme
        - queue2: liste des coordonnées de la queue du 2e serpent (si il existe)
        - pommme2 : liste des coordonnées de la pomme du 2e serpent (si il existe)
        - other_queue : liste des coordonnées de la queue du 2e serpent
        - other_direction : string de la direction du 2e serpent
        '''
        self.queue = [i[0] for i in queue] #prend uniquement les coordonnées de la queue et pas les éléments utilisés pour la sauvegarde de la partie
        self.new_queue = queue2 #prend la queue des 2 snakes qui correspondent à des obstacles
        self.other_apple = list(pomme2) #pomme du 2e snake (à aussi éviter)
        self.pomme = [pomme[0][0],pomme[0][1]] #position de la pomme 
        self.adjacences() #actualise la liste d'adjacence
        self.other_tail = other_queue 
        self.other_direction = other_direction
        if self.type == 'Smart': #fait uniquement par le bot Smart
            if self.try_path(self.pomme): #essaye de voir si un chemin existe entre la pomme et le snake
                self.bloque = False #si oui, on change la valeur de la variable bloqué
                self.compteur = 0 # et on remet ce compteur qui évite un boucle infini à 0
            if not self.bloque: #si le snake n'est pas bloqué
                self.path = self.astar(self.pomme) #on utilise le chemin pour aller à la vraie pomme
            else:
                self.esquive() #sinon on lance la fonction esquive qui va créer une fausse pomme (self.fake_apple)
                print('Pomme fantome : ',self.fake_apple) #pour que l'utilisateur puisse voir quand le snake n'as plus de chemin
                self.path = self.astar(self.fake_apple) #puis on utilise le chemin pour aller à la fausse pomme

        
        else: #dans le cas ou le bot n'est pas le "Smart"
            self.path = self.astar(self.pomme) #il prendra toujours le chemin pour aller à la vraie pomme (d'ou le fait qu'il fonce dans le mur lorsque le chemin n'existe pas)

            




