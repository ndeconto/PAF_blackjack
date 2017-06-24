### Algorithme de Monte-Carlo ###
from random import *;

##########################################################################################################################
actions = {"split":3,"double":2,"draw":1, "fold":0};        #Set d'actions disponibles
enemystate = {0,1,2,3,4,5,6,7,8,9} # 0 = as, 1= deux .... 9 = 10 ou tete
alpha = 1 - 0.0058;                 #Taux d'evaporation
epsilon = 0.05;               #seuil de valeur minimal

##On separe en trois matrices distinctes

policy_simple = [[[0.0]*3 for i in range(15)] for j in range(len(enemystate))]; 
#matrice state = [<9,9,....,21,>21]   
#matrice cas simple (sans As ni paire). Marche comme ca policy_simple[enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2)


policy_as = [[[0.0]*3 for i in range(9)] for j in range(len(enemystate))];
#matrice state = [A2,A3,A4,..,A9,A(figure ou 10)]
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2). On Dois choisir : as initiaux ou n'importe ou dans la partie. PLutot initialement, donc maj du booleen a modifier


policy_pair = [[[0.0]*4 for i in range(10)] for j in range(len(enemystate))]; 
#matrice state = [AA,22,33,...,99,1010)] donc 10 etats
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[enemystate][state][action]
#Les quatre actions sont possibles



###On donne un etat (genre 16) et il renvoie ca place dans la matrice : [<9,9,10,11,12,13,14,15,16,17,18,19,20,21,>21]
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
    player_state,bool_as,bool_can_split,bool_can_doble = state[0],state[1],state[2],state[3]
    ####NE PAS OUBLIER D'AJOUTER BOOL_PAIR DANS LES DEUX VESTEURS STATE DE LA FX MANCHE()
    
    ###Cas ou on a ni as ni paire
    if ( (bool_as == False and bool_can_split == False) or (bool_as == True and player_state > 11) ):
        indice = ind_simple(player_state)
        coeff = policy_simple[enemystate][indice][:]
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
        coeff = policy_pair[enemystate][indice]
        decision = coeff.index(max(coeff))
        x = random();
        if x<epsilon:            #prise de decision non optimale avec proba epsilon
            return(randint(0,3))
        return(decision)
    
    ###Cas ou on a un as
    if (bool_as == True and player_state < 12):
        indice = ind_as(player_state)
        coeff = policy_as[enemystate][indice][:]
        if (not(bool_can_doble)):
            coeff = coeff[0:2]
        decision = coeff.index(max(coeff))
        x = random();
        if x<epsilon:            #prise de decision non optimale avec proba epsilon
            return(randint(0,2))
        return(decision)




###Ecriture de la fonction pour maj des matrices de policy
def update_value3(statesActionsList,bool_as_choice,bool_pair,bank_state,result,position_as):
    ###Cas ou la main initiale ne comportait ni as ni paire
    #print("liste des parametres en entree de update_value3 : sListe, boolaschoice,boolpair,bankstate,result,posAs",statesActionsList,bool_as_choice,bool_pair,bank_state,result,position_as)
    if (bool_as_choice == False and bool_pair == False):
        for couple in statesActionsList:
            state,action = ind_simple(couple[0]),couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = (1-alpha)*result + alpha*pi
            policy_simple[bank_state][state][action] = pi
    ###Cas ou la main initiale comportait une paire
    if (bool_pair == True):
        state,action = ind_pair(statesActionsList[0][0]),statesActionsList[0][1]
        pi = policy_pair[bank_state][state][action]
        pi = (1-alpha)*result + alpha*pi
        policy_pair[bank_state][state][action] = pi  
        k = 1
        ## cas de la paire d'as : ignore pour le moment, parce que pas d'actions particulieres à mener...
        """if (state == 2):
            while (statesActionsList[k][0] < 12):
                #Revenir au tableau as
                state,action = ind_as(statesActionsList[k][0]),statesActionsList[k][1]
                pi = policy_as[bank_state][state][action]
                pi = result + alpha*pi
                policy_as[bank_state][state][action] = pi
                k += 1
                if (k < len(statesActionsList)):
                    state_to_compare = statesActionsList[k][0]
                else:
                    state_to_compare = 12 #On force la sortie de la boucle si notre IA s'arretes de piocher avant d'arriver à 12
            #revenir au tableau normal"""
        for couple in statesActionsList[k:]: #Apres avoir piocher la premiere carte, les etats suivant ne correspondent plus a des paires, on revient au tableau policy_simple
            state,action = ind_simple(couple[0]),couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = (1-alpha)*result + alpha*pi
            policy_simple[bank_state][state][action] = pi
    
    ###Cas ou la main comportait un as soft
    if (bool_as_choice == True and bool_pair == False):
        k = 0
        #Tant qu'on a pas encore tire l'as, on modifie le tableau simple
        while k < position_as - 1 :
            state,action = ind_simple(statesActionsList[k][0]),statesActionsList[k][1]
            pi = policy_simple[bank_state][state][action]
            pi = (1-alpha)*result + alpha*pi
            policy_simple[bank_state][state][action] = pi
            k += 1
        #On a trouve un as plus un total <= 11, on modifie dans le tableau as
        #print("k = " , k)
        #print("statetsAction... : ", len(statesActionsList),len(statesActionsList[0]))
        state_to_compare = statesActionsList[k][0]
        test = as_is_soft(state_to_compare)
        while ( test == True ): #while l'as est toujours soft, on modifie le tableau as soft
            #print("On a trouve un as plus un total <= 11, on modifie dans le tableau as")
            #print("STC : ",state_to_compare)
            #Revenir au tableau as
            state,action = ind_as(statesActionsList[k][0]),statesActionsList[k][1]
            pi = policy_as[bank_state][state][action]
            pi = (1-alpha)*result + alpha*pi
            policy_as[bank_state][state][action] = pi
            k += 1
            if (k < len(statesActionsList)):
                state_to_compare = statesActionsList[k][0]
                test = as_is_soft(state_to_compare)
            else:
                test = False #On force la sortie de la boucle si notre IA s'arretes de piocher alors que l'as est toujours soft
        #revenir au tableau normal lorsque le total depasse 11 : l'as vaut maintenant 1
        for couple in statesActionsList[k:]:
            state,action = ind_simple(couple[0]),couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = (1-alpha)*result + alpha*pi
            policy_simple[bank_state][state][action] = pi


def as_is_soft(state):
    if (state + 10 < 22) : return(True) #Si on peut toujours compter l'AS comme un 1 ou un 11
    else : return(False)
    

  