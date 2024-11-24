from math import inf

class BotInt:

    def __init__(self,map) -> None:
        self.map = map

        self.direc = ""



    def adjacences(self):
    
        '''
        Fonction qui crée la liste d'adjacence des cases autour de la tête du serpent uniquement.
        Vérifie dans les 4 directions ce qu'il y a et le rentre dans une liste.
       
        '''
        
        self.adj = {}
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Les 4 directions possibles
        for direction in directions:
            row = self.queue[0][0] + direction[0]
            col = self.queue[0][1] + direction[1]
            if 0 <= row < self.map[0] and 0 <= col < self.map[1]:  # Vérifie que la case est dans les limites de la carte
                if (row, col) not in self.new_queue:  # Vérifie que la case n'est pas occupée par le corps du serpent
                    if (row, col) == tuple(self.pomme) and (row,col) != self.other_apple:  # Vérifie si la case contient une pomme et pas la pomme adverse
                        self.adj[(row, col)] = 0
                    else:
                        self.adj[(row, col)] = 0
                else:
                    self.adj[(row, col)] = float('inf')
            else:
                self.adj[(row, col)] = float('inf')


    

    def actualisation(self,queue,pomme,queue2,pomme2):
        '''
        Fonction qu actualise les valerus du snake

        Arguments : 
        - queue : liste qui contient la position de la queue du serpent (et un chiffre utile pour la sauvegarde)
        - pomme : liste qui contient les coordonnées de la pomme (et un chiffre utile pour la sauvegarde)
        - queue2 : liste qui contient l'ensemble des 2 queues, si il y a 2 joueurs, sinon 2 fois la même queue
        - pomme2 : liste qui contient les coordonnées de la pomme adverse 
        '''
        self.queue = [i[0] for i in queue] #on fait ça pour ne pas prendre les chiffres de sauvegardes ajoutés à chaque coordonnées
        self.new_queue = queue2
        self.other_apple = pomme2
        self.pomme = pomme[0] #on ne prend pas le chiffre de sauvegarde

        self.adjacences() #crée la liste d'adjacence
    
    def distance_euclidienne(self,case):
        '''
        Fonction qui calcule la distance entre la case et la pomme

        Argument :
            - case : liste contenant les coordonnés de la case
        Retourne :
            - la distance de Manhattan (pas de racine et de carré) entre la case en argument et la pomme

        '''
        return abs(case[0]-self.pomme[0]) + abs(case[1]-self.pomme[1])
    
    def find_mini(self,dico):
        '''
        Fonction qui trouve la case avec la plus petite distance avec la pomme

        Argument : 
            - dico : dictionnaire contenant les quatres cases à coté de la tête avec la distance entre la pomme et la case en question

        Retourne : 
            - case : la case ayant la plus petite distance
            - False : si le dico est vide

        '''
        #fonction basique qui trouve le minimum dans les valeurs du dico
        case = None
        mini = inf
        if len(dico.keys()) > 0:
            for i in dico.keys():
                if dico[i] < mini:
                    mini = dico[i]
                    case = i
            return case
        else:
            return False

    def moove(self):
        '''
        Fonction qui essaye au maximum de se rapprocher de la pomme, en fonction de sa distance avec la pomme
        et qui évite les obstacles

        Retourne : 
            - self.direc : la direction dans laquelle le serpent doit aller
        '''
        #phase de test
        try:
            len(self.adj) != 4
        except ValueError as l:
            print('Pas tous les adjacents')
            print(l)  
        #création du dictionnaire avec les directions comme clé et la distance entre la case dans cette direction et la pomme comme valeur
        self.distance = {'right':self.distance_euclidienne([self.queue[0][0]+1,self.queue[0][1]])+self.adj[(self.queue[0][0]+1,self.queue[0][1])],
                    'left':self.distance_euclidienne([self.queue[0][0]-1,self.queue[0][1]])+self.adj[(self.queue[0][0]-1,self.queue[0][1])],
                    'up':self.distance_euclidienne([self.queue[0][0],self.queue[0][1]-1])+self.adj[(self.queue[0][0],self.queue[0][1]-1)],
                    'down':self.distance_euclidienne([self.queue[0][0]+1,self.queue[0][1]+1])+self.adj[(self.queue[0][0],self.queue[0][1]+1)]                    
                    }
        self.adjust()

        old_dir = self.direc
        self.direc = self.find_mini(self.distance) #met la direction selon le minimum trouvé dans le dico

        if old_dir == self.direc : #si la nouvelle direction est la même qui l'ancienne
            self.distance.pop(self.inverse(self.direc)) #on supprime l'élément du dico qui la direction opposé
            self.direc = self.find_mini(self.distance) #on prend alors la valeur finale de la direction que le bot va renvoyer au snake (sans la direction opposé)

        return self.direc
    

    def adjust(self):
        '''
        Fonction qui donne une distance infini à la direction opposé à laquelle le serpent se dirige, pour éviter qu'il veuille faire demi tour 
        '''
        for i in self.distance.keys():
            if i == self.inverse(self.direc):
                self.distance[i] = inf

    def inverse(self,dir):
        '''
        Fonction qui dit quelle direction est oppposée à la direction demandé

        Argument :
        - dir : str avec la direction dont on demande l'oppposé

        Retourne :
        - la direction opposée à la direction demandée en argument
        '''
        if dir == 'right':
            return 'left'
        if dir == 'left':
            return 'right'
        if dir == 'up':
            return 'down'
        if dir == 'down':
            return 'up'

        