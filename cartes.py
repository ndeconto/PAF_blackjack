# -*- coding: utf-8 -*-

import random
from warnings import warn


#definition des constantes bien pratiques 


VALET   = 11
DAME    = 12
ROI     = 13
AS      = 1

COEUR   =   14
PIQUE   =   15
CARREAU =   16
TREFLE  =   17


REPR = ["undefined", "as", "deux", "trois", "quatre", "cinq", "six", "sept",
        "huit", "neuf", "dix", "valet", "dame", "roi",
        "coeur", "pique", "carreau", "trefle"
        ]


class Carte:
    """
        classe representant une carte de jeu (ex 3 de carreau)
    """

    def __init__(self, hauteur, couleur):
        """
            exemples d'utilisation :
            valet_de_coeur = Carte(VALET, COEUR)
            trois_de_pique = Carte(3, PIQUE)
        """


        #hauteur de la carte : as, deux, trois, ... dame, roi
        self.hauteur = hauteur
        self.couleur = couleur

        #valeur de la carte : 1, 2, ... 10, 11.
        self.valeur = self.get_valeur()

    def get_card_object(self,indice):
        return (self.contenu[indice])
    
    def get_valeur(self):
        """
            renvoie la valeur de la carte au blackjack
            plus precisement, cette methode renvoie : 
                2 -> 10 : valeur nominale de la carte
                valet, dame, roi : 10
                as : [1, 11]

            NB : POUR UN AS, CETTE METHODE RENVOIE UNE LISTE !!
        """

        if 1 < self.hauteur <= 13: return min(self.hauteur,10)

        if self.hauteur == AS: return [1, 11]
        #if self.hauteur == ASONZE: return(11)
        return 10
        
    def __str__(self):
        return  REPR[self.hauteur] + " de " + REPR[self.couleur]

    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        """
            reecriture de la methode d'egalite de sorte qu'ecrire :
            
                ma_carte == AS      signifie "ma_carte est un as"
                ma_carte == COEUR   signifie "ma_carte est un coeur"
        """

        if isinstance(other, int):
            return (other == self.hauteur) or (other == self.couleur)

        if isinstance(other, Carte):
            return other.hauteur == self.hauteur and other.couleur == self.couleur


        if other == None:
            return False

        raise (TypeError("L'operation de type Carte == " + str(type(other))
                         + " n'est pas definie"))

    def __ne__(self, other):
        """ operateur != """
        return not (self == other)
        


class Main:
    """
        classe representant une main, c'est a dire un ensemble de cartes
    """

    def __init__(self, contenu):
        """
            Main([Carte(AS, COEUR), Carte(2, TREFLE)]) cree une main contenant
            un as de coeur et un deux de trefle
            Main([]) cree une main vide

        """

        #liste des cartes dans la main
        self.contenu = contenu

        #valeur optimale de la main
        self.valeur = 0
        self.calcul_valeur()

    def get_card_at(self,indice):
        if (isinstance(self.contenu[indice].valeur,int)): 
            return(self.contenu[indice].valeur)
        else: 
            return(1)
    
    def get_card_at_high(self,indice):
        return(self.contenu[indice].hauteur)
        
    def ajouter(self, nouvelle_carte):
        """
            rajoute 'carte' a la main
            la valeur de la main est mise a jour automatiquement
        """

        self.contenu.append(nouvelle_carte)

        self.calcul_valeur()

        

    def calcul_valeur(self):
        """
            calcule en place la liste des valeurs possibles de la main
            NON --> calcul la meilleur main possible 
        """

        v = 0
        b = False   #on regarde si on a un as
        for c in self.contenu:
            if c != AS :
            	v += c.valeur
            else: 
            	v += 1
            	b = True
        if (v<12 and b) : v+=10
        self.valeur = v

    def get_m_valeur(self):
    	return self.valeur

    def __str__(self):
        return "[" + "; ".join(map(str, self.contenu)) + "]"

    def __repr__(self):
        return str(self)
    
    def __len__(self):
        return(len(self.contenu))

    def __getitem__(self, i):
        return self.contenu[i]


class Deck:
    """
        represente un jeu (initalement) de 52 cartes
        Au blackjack : cartes melangees entre chaque tours ? (Est-ce qu'on peut compter les cartes)
    """
    
    def __init__(self):
        self.pile = [Carte(i, j) for i in range(AS, ROI + 1)
                     for j in [COEUR, PIQUE, CARREAU, TREFLE]]

        random.shuffle(self.pile)

    def piocher(self):
        return self.pile.pop()
    
    
class DeckTruque (Deck):
    """
    Permet de creer un deck ou il manque des cartes pour l'apprentissage spÃ©cifique    
    """
    
    def __init__(self,liste_carte):
        self.pile = [Carte(i, j) for i in range(AS, ROI + 1)
                     for j in [COEUR, PIQUE, CARREAU, TREFLE]
                     if not (Carte(i,j) in liste_carte)]
        random.shuffle(self.pile)



class Sabot(Deck):
    """
        dans les casinos, NB_PAQUET de 52 cartes sont melanges ensemble, cela
        forme un sabot. Ensuite, le croupier joue plusieurs manches en utilisant
        ces NB_PAQUET * 52 cartes, sans remelanger.
        On peut donc avoir 3 dame de coeur, c'est normal, car il y a plusieurs
        jeux de cartes
        Au fil des manches, le sabot s'epuise. Apres avoir pioche
        TAUX_PENETRATION pourcents des cartes du sabots, le croupier remelange
        le sabot, en laissant bien sur sur la table les cartes utilisees pour
        la manche en cours. Un taux de penetration eleve avantage les joueurs
        qui comptent les cartes.

        cette classe s'utilise de la maniere suivante :
            - creer le sabot : mon_sabot = Sabot()
            - quand une nouvelle manche commence, ne pas creer de nouveau sabot
                mais simplement faire : mon_sabot.nouvelle_manche()
            - quand on veut tirer une carte, faire : mon_sabot.piocher()
            - quand on veut connaitre la valeur du compteur (pour le comptage
                des cartes), faire : mon_sabot.get_counter()
            - et c'est tout ! la classe s'occupe toute seule de remelanger quand
                il le faut. Les cartes de la manche en cours ne sont pas
                remelangees. (c'est pour pouvoir faire ca qu'il y a une methode
                nouvelle_manche() a appeler)

        NB : avec un sabot, il y aura beaucoup plus d'erreur du style
        "pop from empty list", erreur que l'on peut avoir avec un Deck.
        Cette erreur arrivera si la fonction nouvelle_manche n'est pas appelee
        Cependant, si la classe s'apercoit que plus de NB_MAX_CARTE_PAR_MANCHE
        cartes ont ete piochees dans une meme manche, un warning sera lance
        Donc la console sera inondee de warning avec d'avoir le pop from empty
        list

    """

    #valable en europe et aux US, au canada c'est 8...
    NB_PAQUET           =   6
    TAUX_PENETRATION    =   75  #pourcents

    NB_MAX_CARTE_PAR_MANCHE = 52


    def __init__(self, counter_bound=5, warning_enable=True):
        """
            le parametre warning_enable permet d'activer/desactiver les warnings
            quand il y a "trop" de cartes utilisees dans une main pour etre
            honnete
            le compteur renvoye par get_counter est borne par coutner_bound
        """
        self.pile = [Carte(i, j) for i in range(AS, ROI + 1)
                     for j in [COEUR, PIQUE, CARREAU, TREFLE]
                     for k in range(self.NB_PAQUET)]

        self.trash = []
        self.on_table = []
        self.counter = 0
        self.counter_bound = counter_bound
        self.warning_enable = warning_enable
        self.carte_min = int(len(self.pile) * (1 - self.TAUX_PENETRATION / 100.))
        assert(self.carte_min >= 0)

        random.shuffle(self.pile)

    def nouvelle_manche(self):
        """
            quand le sabot est remelange, on ne remelange pas les cartes qui
            sont sur la table et utilisees dans la manche en cours
            il faut donc que le sabot sache quand les manches commencent pour
            savoir quelles cartes il peut remelanger.
            La fonction nouvelle_manche doit donc etre appelee au debut de
            chaque manche (cf ci-dessus)
            NB : il ne faut pas creer un nouveau sabot a chaque debut de manche,
            sinon on ne peut pas compter les cartes !
        """

        self.trash.extend(self.on_table)
        self.on_table = []
        
            

    def piocher(self):

        #s'il faut remelange
        if len(self.pile) <= self.carte_min:
            #et bien on remelange, dingue n'est ce pas ?
            self.pile.extend(self.trash)
            self.trash = []
            random.shuffle(self.pile)

            #et on met a jour le compte
            self.counter = 0
            for c in self.on_table:
                self.counter += self.delta_counter(c)
            
        carte = self.pile.pop()
        self.on_table.append(carte)
        self.counter += self.delta_counter(carte)

        if self.warning_enable == len(self.on_table) > self.NB_MAX_CARTE_PAR_MANCHE:
            warn(UserWarning("Il y a actuellement " + str(len(self.on_table))
                             + " cartes utilisees dans cette manche ; est ce "
                             + "bien normal ?"))

        return carte

    def get_counter(self):
        """
            on compte les cartes selon la technique HI-LOW
            on renvoie le compteur en cours, pas le vrai compteur
            (vrai compteur = compteur en cours / nb de deck utilises)
            cela permet d'avoir des entiers, ce qui est pratique pour indexer
            directement avec le compteur en cours
            RAPPEL : en python, on peut indexer des tableaux avec des entiers
            negatifs
        """

        if self.counter >= self.counter_bound:
            return self.counter_bound
        if self.counter <= self.counter_bound:
            return - self.couunter_bound
        
        return self.counter
    

    def delta_counter(self, carte):
        """
            renvoie la variation du compteur obtenue quand on tire la carte
            'carte' (technique HI-LOW)
        """

        if (2 <= carte.hauteur <= 6):
            return 1

        if (7 <= carte.hauteur <= 9):
            return 0

        #cas 10, J, Q, K, A
        return -1


class SabotDistant(Sabot):


    def __init__(self, ip, port):

        self.client = Client(port, ip)

    def piocher(self):
        
        r = c.has_drawn()

        

        

    
