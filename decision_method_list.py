STOP = 0
HIT = 1
DOUBLE = 2
SPLIT = 3

"""
cf dans load_object.py le fichier qui est load dans policy
"""

POLICY_FILE = "policy_a_utilise_python2"

from random import *;
from load_object import *

##########################################################################################################################
enemystate = {0,1,2,3,4,5,6,7,8,9} # 0 = as, 1= deux .... 9 = 10 ou tete
alpha = 1 - 0.0058;                 #Taux d'evaporation
epsilon = 0.05;               #seuil de valeur minimal


##On separe en trois matrices distinctes

valeur_possible_compteur = 1 #11 valeurs de compteur autorisees

policy_simple = [[[[0.0]*3 for i in range(15)] for j in range(len(enemystate))] for k in range(valeur_possible_compteur)]; 
#matrice state = [<9,9,....,21,>21]   
#matrice cas simple (sans As ni paire). Marche comme ca policy_simple[compteur][enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2)
    
    
policy_as = [[[[0.0]*3 for i in range(9)] for j in range(len(enemystate))] for k in range (valeur_possible_compteur)];
#matrice state = [A2,A3,A4,..,A9,A(figure ou 10)]
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[compteur][enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2). On Dois choisir : as initiaux ou n'importe ou dans la partie. PLutot initialement, donc maj du booleen a modifier
    
    
policy_pair = [[[[0.0]*4 for i in range(10)] for j in range(len(enemystate))]for k in range(valeur_possible_compteur)]; 
#matrice state = [AA,22,33,...,99,1010)] donc 10 etats
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[compteur][enemystate][state][action]
#Les quatre actions sont possibles
  
def initialize_policy():
    global policy_as,policy_pair,policy_simple
    p_simple,p_as,p_pair = getPolicy(POLICY_FILE)

    for k in range (len(p_as[0])):
        for i in range(len(p_as[0][0])):
            for j in range (len(p_as[0][0][0])):
                policy_as[0][k][i][j] = p_as[0][k][i][j]
    for k in range (len(p_simple[0])):
        for i in range(len(p_simple[0][k])):
            for j in range (len(p_simple[0][k][i])):
                policy_simple[0][k][i][j] = p_simple[0][k][i][j]
    for k in range (len(p_pair[0])):
        for i in range(len(p_pair[0][k])):
            for j in range (len(p_pair[0][k][i])):
                policy_pair[0][k][i][j] = p_pair[0][k][i][j]

    
initialize_policy()
###
    

###On donne un etat (genre 16) et il renvoie sa place dans la matrice : [<9,9,10,11,12,13,14,15,16,17,18,19,20,21,>21]
def ind_simple(state):
    if state<9 : return 0
    elif state>21 : return 14
    else: return state-8


###On donne un etat (genre 18) et il renvoie ca place dans la matrice : [AA,22,...,99]
def ind_pair(state):
    return(int(state/2)-1)


###On donne un etat (genre 17) et il renvoie ca place dans la matrice state
def ind_as(state):
    return(state-3)


###Reecriture de la prise de decision donne un etat
def makeDecision3(state,enemystate):
    player_state,bool_as,bool_can_split,bool_can_doble, compteur = state[0],state[1],state[2],state[3],state[4]
    ####NE PAS OUBLIER D'AJOUTER BOOL_PAIR DANS LES DEUX VESTEURS STATE DE LA FX MANCHE()
    
    ###Cas ou on a ni as soft ni paire
    if ( (bool_as == False and bool_can_split == False) or (bool_as == True and player_state > 11) ):
        indice = ind_simple(player_state)
        coeff = policy_simple[compteur][enemystate][indice][:]
        if (not(bool_can_doble)):
            coeff = coeff[0:2]
        decision = coeff.index(max(coeff))
        x = random();
        if x<epsilon:            #prise de decision non optimale avec proba epsilon
            return(randint(0,2))
        return(decision)
    
    ###Cas ou on a une paire (le cas as et paire est inclu dans le cas paire)
    if (bool_can_split == True):
        indice = ind_pair(player_state)
        coeff = policy_pair[compteur][enemystate][indice]
        decision = coeff.index(max(coeff))
        x = random();
        if x<epsilon:            #prise de decision non optimale avec proba epsilon
            return(randint(0,3))
        return(decision)
    
    ###Cas ou on a un as
    if (bool_as == True and player_state < 12):
        indice = ind_as(player_state)
        coeff = policy_as[compteur][enemystate][indice][:]
        if (not(bool_can_doble)):
            coeff = coeff[0:2]
        decision = coeff.index(max(coeff))
        x = random();
        if x<epsilon:            #prise de decision non optimale avec proba epsilon
            return(randint(0,2))
        return(decision)

def makeBestDecision(state,enemystate):
    player_state,bool_as,bool_can_split,bool_can_doble, compteur = state[0],state[1],state[2],state[3],state[4]
    ####NE PAS OUBLIER D'AJOUTER BOOL_PAIR DANS LES DEUX VESTEURS STATE DE LA FX MANCHE()


    print "make best decision", state, enemystate
    if player_state < 14: return SPLIT
    
    ###Cas ou on a ni as soft ni paire
    if ( (bool_as == False and bool_can_split == False) or (bool_as == True and player_state > 11) ):
        indice = ind_simple(player_state)
        coeff = policy_simple[compteur][enemystate][indice][:]
        if (not(bool_can_doble)):
            coeff = coeff[0:2]
        decision = coeff.index(max(coeff))
        return(decision)
    
    ###Cas ou on a une paire (le cas as et paire est inclu dans le cas paire)
    if (bool_can_split == True):
        indice = ind_pair(player_state)
        coeff = policy_pair[compteur][enemystate][indice]
        decision = coeff.index(max(coeff))
        return(decision)
    
    ###Cas ou on a un as
    if (bool_as == True and player_state < 12):
        indice = ind_as(player_state)
        coeff = policy_as[compteur][enemystate][indice][:]
        if (not(bool_can_doble)):
            coeff = coeff[0:2]
        decision = coeff.index(max(coeff))
        return(decision)

def bankDecision(state,enemystate):
    player_state,bool_as,bool_can_split,bool_can_doble, compteur = state[0],state[1],state[2],state[3],state[4]
    if player_state<17 :
        return(HIT)
    else :
        return(STOP)
    
    
print(makeBestDecision([11,False,False,True,0],3))
