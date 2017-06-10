# ce fichier permet de faire la conversion entre les objets Carte, Main formels
#en images affichables par l'interface graphique

from pygame import *


import sys
#cartes etant dans le dossier parent, il faut bricoler pour pouvoir importer
sys.path.append("..")
from cartes import *


#taille des cartes en pixels
TX = 192
TY = 279

#constantes pour parametrer l'affichage
HORIZONTAL  =   0
VERTICAL    =   1

#decalage des cartes lorsqu'on en affiche plusieurs
DECALAGE_RELATIF_X = .2
DECALAGE_RELATIF_Y = .3


#matrice 4 * 13 contenant les images
img_cartes = [[None] * 13 for i in range(4)]


def charger_img():
    """
        fonction d'initialisation
        doit etre appelee avant le premier appel a get_img !!!
    """
    
    all_cards = image.load("img/img_cartes_2.png").convert_alpha()

    

    for couleur in range(4):
        for hauteur in range(13):
            img_cartes[couleur][hauteur] = all_cards.subsurface(hauteur  * TX,
                                                                couleur * TY,
                                                                TX, TY)



def get_img(c, sens=VERTICAL):
    """
        prend en parametre une Carte ou une Main
        renvoie une image representant cet objet

        dans le cas ou c est une Main, sens permet de choisir l'orientation
        de l'affichage : sens = HORIZONTAL ou sens = VERTICAL.
    """

    if isinstance(c, Carte):
        if c.couleur == COEUR:
            return img_cartes[2][c.hauteur - 1]
        elif c.couleur == PIQUE:
            return img_cartes[3][c.hauteur - 1]
        elif c.couleur == TREFLE:
            return img_cartes[0][c.hauteur - 1]
        elif c.couleur == CARREAU:
            return img_cartes[1][c.hauteur - 1]
        else:
            raise(ValueError("la couleur " + str(c.couleur) + " n'est pas reconnue"))


    elif isinstance(c, Main):
        l_img = [get_img(carte) for carte in c.contenu]
        n = len(l_img)

        if sens == VERTICAL:
            s = Surface((TX, TY * (1 + (n - 1) * DECALAGE_RELATIF_Y)))

            dx = 0
            dy = TY * DECALAGE_RELATIF_Y
            

        elif sens == HORIZONTAL:
            s = Surface((TX * (1 + (n - 1) * DECALAGE_RELATIF_X), TY))

            dx = TX * DECALAGE_RELATIF_X
            dy = 0

        else:
            raise(ValueError("la valeur de sens = " + str(sens) + 
                             " n'est pas reconnue"))

        r = Rect(0, 0, TX, TY)
        for img in l_img:
            s.blit(img, r)
            r.move_ip(dx, dy)

        return s


    else:
        raise(TypeError("c n'est ni une Carte ni une Main"))
        

    

            

    
