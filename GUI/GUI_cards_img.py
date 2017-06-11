# ce fichier permet de faire la conversion entre les objets Carte, Main formels
#en images affichables par l'interface graphique

from pygame import *
from GUI_component import *


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


def init_lib_cartes():
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
        

    
class MainGraphique(GUIComponent, Main):
    """
        objet graphique qui represente une Main de cartes
    """

    def __init__(self, contenu, position, sens=VERTICAL, identifier=""):
        """
            contenu = contenu de la Main
            position = position a l'ecran
            sens = cf get_img
        """

        Main.__init__(self, contenu)
        img = get_img(self, sens)
        self.sens = sens
        GUIComponent.__init__(self, 1, position, img.get_size(), [], [], img,
                              identifier)


        #pour deplacer les cartes
        self.drag = False

    def ajouter(self, nouvelle_carte): #redefinition de la methode
        
        Main.rajouter(self, nouvelle_carte)
        self.background = get_img(self, self.sens)


    def manage_event(self, event_list):

        GUIComponent.manage_event(self, event_list)

        for ev in event_list:

            if (self.drag or
                Rect(self.position, self.size).collidepoint(mouse.get_pos())) :

                if ev.type == MOUSEBUTTONDOWN:
                    x1, y1 = mouse.get_pos()
                    x2, y2 = self.position
                    self.offset = (x1 - x2, y1 - y2)
                    self.drag = True

                if ev.type == MOUSEMOTION and mouse.get_pressed()[0]:
                    x, y = mouse.get_pos()
                    self.position = (x - self.offset[0], y - self.offset[1])

                if ev.type == MOUSEBUTTONUP:
                    self.drag = False
        
            
            

    
