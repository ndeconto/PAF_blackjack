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

        if 1 <= self.hauteur <= 13: return min(self.hauteur,10)

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

        #valeur optimale de la main
        self.valeur = 0
        self.calcul_valeur()


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


class Deck:
    """
        represente un jeu (initalement) de 52 cartes
    """

    def __init__(self):
        self.pile = [Carte(i, j) for i in range(AS, ROI + 1)
                     for j in [COEUR, PIQUE, CARREAU, TREFLE]]

        random.shuffle(self.pile)

    def piocher(self):
        return self.pile.pop()
        

        
