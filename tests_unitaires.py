import unittest

from cartes import *
from prise_3_decision import*

def mf(*liste):
    """
        constructeur d'une main quand on est faineant
    """
    return Main([Carte(x, COEUR) for x in liste])


#format de data: chaque ligne est une liste de deux elements (un cas de test)
#premier element : liste des arguments en entree
#deuxieme element : resultat attendu
def test_function(f, data):

    for entree, sortie in data:
        try:
            assert(f(*entree) == sortie)

        except AssertionError as e:
            print ("\n==============================")
            print ("------- entree ----- ")
            print (entree)
            print ("\n----- Sortie ------ ")
            print (f(*entree))

            print ("\n----- Sortie Attendue ----")
            print(sortie)
            
            raise (e)

        
        
            
            

data = [
    [[mf(AS, 10),        mf(8, 8, 5),           1],         1.5],  
    [[mf(10, 3, 1),     mf(1, 1, 1, 1),     1],         0],
    [[mf(7, 5),         mf(10, 9, 3),       2],         2],
    [[mf(10, 1),        mf(10, 10, 1),      1],         1.5],
    [[mf(1, DAME),     mf(9, 9, 3),        1],         1.5],
    [[mf(1, ROI),       mf(DAME, 1),        2],         0]
]
test_function(win_sym, data)


data = [
    [[mf(5, 7), mf(7, 3, 9),          mf(6, 5, 7),    1],     0],
    [[mf(AS, VALET), mf(7, 8, 2),     mf(10, 9, 1),   1],     0],
    [[mf(AS, VALET), mf(7, 8, 2),     mf(10, 9, 2),   1],     -1],
    [[mf(AS, VALET), mf(7, 8, 6),     mf(10, AS),     1],     -2],
    [[mf(8, 8, 5), mf(7, 8, 2),       mf(7, 4),       1],     2],
    [[mf(5, 3), mf(5, 8),             mf(10, 9),      1],     -2]
]
test_function(win_sym_split, data)


data = [
    [[mf(5, 9, 3), mf(5, 3, 7),       mf(8, 8, 6), mf(8, 7, 6),     1], 0],
    [[mf(5, 9, 3), mf(5, 3, 7),       mf(8, 8), mf(8, 7, 5),        1], -2],
    [[mf(5, 9, 3), mf(5, 6, 7),       mf(8, 4, 4), mf(8, 7, 5),     1], 0],
    [[mf(5, 9, 3), mf(5, 6, 5),       mf(8, 4, 4), mf(8, 7, 5),     1], -1],
    [[mf(5, 9, 7), mf(ROI, AS),       mf(8, 8), mf(8, 7, 6),        1], 2],
    [[mf(5, 9, 7), mf(5, 3, 7),       mf(8, 7), mf(8, 2, 2),        1], 3],
    [[mf(10, 10), mf(10, 9),          mf(8, 8, 6), mf(8, 4, 6),     1], 4]
]
test_function(win_sym_split_split, data)
    





    

