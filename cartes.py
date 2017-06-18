import random
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


    def get_valeur(self):
        """
            renvoie la valeur de la carte au blackjack
            plus precisement, cette methode renvoie : 
                2 -> 10 : valeur nominale de la carte
                valet, dame, roi : 10
                as : [1, 11]

            NB : POUR UN AS, CETTE METHODE RENVOIE UNE LISTE !!
        """

        if 2 <= self.hauteur <= 10: return self.hauteur

        if self.hauteur == AS: return [1, 11]

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

        #liste des valeurs possibles de la  main
        self.valeur = [0]
        self.calcul_valeur()


    def ajouter(self, nouvelle_carte):
        """
            rajoute 'carte' a la main
            la valeur de la main est mise a jour automatiquement
        """

        self.contenu.append(nouvelle_carte)

        self.maj_valeur(nouvelle_carte)

        

    def maj_valeur(self, nouvelle_carte):
        """
            met a jour la valeur de la main quand on rajoute une nouvelle carte
        """

        if nouvelle_carte != AS:
            self.valeur = [x + nouvelle_carte.valeur for x in self.valeur]

        else:
            #NB : s'il y a deux as, le deuxieme as est forcement compte comme
            #un 1 (et le premier reste au choix 1 ou 11)
            # NB 2 : ne pas se faire avoir pas le cas d'initialisation !
            # (self.valeur == [0])
            if self.valeur == [0] or (not (AS in self.contenu)):
                self.valeur = ([x + 1 for x in self.valeur]
                               + [x + 11 for x in self.valeur])

            else :
                self.valeur = [x + 1 for x in self.valeur]


        

    def calcul_valeur(self):
        """
            calcule en place la liste des valeurs possibles de la main
        """

        self.valeur = [0]

        for c in self.contenu:
            self.maj_valeur(c)


    def __str__(self):
        return "[" + "; ".join(map(str, self.contenu)) + "]"

    def __repr__(self):
        return str(self)


class Deck:
    """
        represente un jeu (initalement) de 52 cartes
        Au blackjack : cartes melangées entre chaque tours ? (Est-ce qu'on peut compter les cartes)
    """
    
    def __init__(self):
        self.pile = [Carte(i, j) for i in range(AS, ROI + 1)
                     for j in [COEUR, PIQUE, CARREAU, TREFLE]]

        random.shuffle(self.pile)

    def piocher(self):
        return self.pile.pop()
    
    
        

        
