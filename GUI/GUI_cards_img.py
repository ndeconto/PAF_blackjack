# ce fichier permet de faire la conversion entre les objets Carte, Main formels
#en images affichables par l'interface graphique

from pygame import *
from GUI_component import *


import sys
#cartes etant dans le dossier parent, il faut bricoler pour pouvoir importer
sys.path.append("..")
from cartes import *



#taille des cartes en pixels
TX = 153.85 #192.3
TY = 223.4 #279

#constantes pour parametrer l'affichage
HORIZONTAL  =   0
VERTICAL    =   1

#decalage des cartes lorsqu'on en affiche plusieurs
DECALAGE_RELATIF_X = .2
DECALAGE_RELATIF_Y = .2


#matrice 4 * 13 contenant les images
img_cartes = [[None] * 13 for i in range(4)]
img_carte_cachee = None


def init_lib_cartes():
    """
        fonction d'initialisation
        doit etre appelee avant le premier appel a get_img !!!
    """
    global img_carte_cachee
    
    all_cards = image.load("img/img_cartes_2_petit.png").convert_alpha()

    

    for couleur in range(4):
        for hauteur in range(13):
            img_cartes[couleur][hauteur] = all_cards.subsurface(hauteur  * TX,
                                                                couleur * TY,
                                                                TX, TY)

    img_carte_cachee = all_cards.subsurface(2 * TX, 4 * TY, TX, TY)



def get_img(c, sens=VERTICAL, face_cachee=[], d_x=DECALAGE_RELATIF_X,
            d_y=DECALAGE_RELATIF_Y):
    """
        prend en parametre une Carte ou une Main
        renvoie une image representant cet objet

        dans le cas ou c est une Main, sens permet de choisir l'orientation
        de l'affichage : sens = HORIZONTAL ou sens = VERTICAL.

        face_cachee:
            si c est une carte, il s'agit d'un booleen d'usage evident
            si c est une Main, face_cachee est  liste des indices des cartes de
            contenu qui doivent etre affichees face cachee
            par exemple, face_cachee = [2, 5] signifie que les cartes contenu[2]
            et contenu[5] seront affichees face cachees

        d_x, d_y : decalage de position relatif entre 2 cartes
    """

    if isinstance(c, Carte):
        if face_cachee:
            return img_carte_cachee
        elif c.couleur == COEUR:
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
        l_img = [get_img(carte, face_cachee=(i in face_cachee))
                         for i, carte in enumerate(c.contenu)]
        n = len(l_img)

        if sens == VERTICAL:
            s = Surface((TX, TY * (1 + (n - 1) * d_y)), SRCALPHA, 32)

            dx = 0
            dy = TY * d_y
            

        elif sens == HORIZONTAL:
            s = Surface((TX * (1 + (n - 1) * d_x), TY), SRCALPHA, 32)

            dx = TX * d_x
            dy = 0

        else:
            raise(ValueError("la valeur de sens = " + str(sens) + 
                             " n'est pas reconnue"))



        r = Rect(0, 0, TX, TY)
        for i, img in enumerate(l_img):
            s.blit(img, r)
            r = Rect((i + 1) * dx, (i + 1) * dy, TX, TY)

        return s


    else:
        raise(TypeError("c n'est ni une Carte ni une Main"))
        

    
class MainGraphique(GUIComponent, Main):
    """
        objet graphique qui represente une Main de cartes
    """

    def __init__(self, contenu, position, sens=VERTICAL, identifier="",
                 face_cachee=[], d_x=DECALAGE_RELATIF_X, d_y=DECALAGE_RELATIF_Y):
        """
            contenu = contenu de la Main
            position = position a l'ecran
            sens = cf get_img

            face_cachee = cf get_img

            d_x et d_y : cf get_img
        """

        Main.__init__(self, contenu)
        img = get_img(self, sens, face_cachee, d_x, d_y)
        self.sens = sens
        self.dx = d_x
        self.dy = d_y
        GUIComponent.__init__(self, 1, position, img.get_size(), [], [], img,
                              identifier, e_bord=5)

        self.set_encircling_color((219, 201, 101))

        #attention, il ne faut pas que face_cachee contienne deux fois le meme
        #element (du genre face_cachee = [2, 2]) sinon les autres methodes ne
        #vont pas aimer
        self.face_cachee = list(set(face_cachee))


        #pour deplacer les cartes
        self.drag = False


    def set_face_cachee(self, new_face_cachee):
        self.face_cachee = new_face_cachee
        self.background = get_img(self, self.sens, face_cachee=new_face_cachee,
                                  d_x=self.dx, d_y=self.dy)

    def ajouter(self, nouvelle_carte): #redefinition de la methode de Main
        
        Main.ajouter(self, nouvelle_carte)
        self.background = get_img(self, self.sens, face_cachee=self.face_cachee,
                                  d_x=self.dx, d_y=self.dy)
        self.size = self.background.get_size()

    def retourner_carte(self, i):
        """
            retourne la carte d'indice i dans self.contenu
        """

        if i in self.face_cachee:
            self.face_cachee.remove(i)
        else :
            self.face_cachee.append(i)

        self.img = get_img(self, self.sens, self.face_cachee)


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

                    self.display_level += .5

                if self.drag and ev.type == MOUSEMOTION and mouse.get_pressed()[0]:
                    x, y = mouse.get_pos()
                    self.position = (x - self.offset[0], y - self.offset[1])

                if self.drag and ev.type == MOUSEBUTTONUP:
                    self.drag = False

                    self.display_level -= .5

                    print self.position

        return CONTINUE
        
            
            
class DeckGraphique(MainGraphique, Sabot):

    def __init__(self, position):
        
        Sabot.__init__(self)
        MainGraphique.__init__(self, self.pile, position, sens=HORIZONTAL,
                               identifier="",
                               face_cachee=list(range(len(self.pile))),
                               d_x=0.0001)
    
    
