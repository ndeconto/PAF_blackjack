STOP = 0
HIT = 1
DOUBLE = 2
SPLIT = 3

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