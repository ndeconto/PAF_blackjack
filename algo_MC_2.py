#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:39:31 2017

@author: majdagoumi
"""

### Algorithme de Monte-Carlo ###
from random import *;

def nb_action_dispo(k):
	if k<2:
		return 3
	return 4

actions = {"split":3,"double":2,"draw":1, "fold":0};        #Set d'actions disponibles
enemystate = {0,1,2,3,4,5,6,7,8,9} # 0 = as, 1= deux .... 9 = 10 ou tete
alpha = 0.95;                 #Taux d'evaporation
epsilon = 0.05;               #seuil de valeur minimal

##On separe en trois matrices distinctes

policy_simple = [[[10.0]*3 for i in range(15)] for j in range(len(enemystate))]; 
#matrice state = [<9,9,....,21,>21]   
#matrice cas simple (sans As ni paire). Marche comme ca policy_simple[enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2)


policy_as = [[[10.0]*3 for i in range(9)] for j in range(len(enemystate))];
#matrice state = [A2,A3,A4,..,A9,A(figure ou 10)]
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[enemystate][state][action]
#trois actions disponibles ici : draw(1), fold(0), doble(2). On Dois choisir : as initiaux ou n'importe ou dans la partie. PLutot initialement, donc maj du booleen a modifier


policy_pair = [[[10.0]*4 for i in range(10)] for j in range(len(enemystate))]; 
#matrice state = [AA,22,33,...,99] donc 10 etats
#matrice cas on pioche un as sans paire. Marche comme ca policy_simple[enemystate][state][action]
#Les quatre actions sont possibles



###On donne un etat (genre 16) et il renvoie ca place dans la matrice : [<12,12,13,14,15,16,17,18,19,20,21,>21]
def ind_simple(state):
    if state<9 : return 0
    elif state>21 : return 14
    else: return state-8


###On donne un etat (genre 17) et il renvoie ca place dans la matrice : [AA,22,...,99]
def ind_pair(state):
    return(int(state/2)-1)


###On donne un etat (genre 17) et il renvoie ca place dans la matrice state
def ind_as(state):
    return(state-3)



##Reecriture de la prise de decision donne un etat
def makeDecision3(state,enemystate):
    player_state,bool_as,bool_can_split,bool_can_doble,bool_pair = state[0],state[1],state[2],state[3],state[4]
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
def update_value3(statesActionsList,bool_as,bool_pair,bank_state,result,position_as):
    
    ###Cas ou la main initiale ne comportait ni as ni pair
    if (bool_as == False and bool_pair == False):
        for couple in statesActionsList:
            state,action = couple[0],couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = result + alpha*pi
            policy_simple[bank_state][state][action] = pi
    ###Cas ou la main initiale comportait une pair
    if (bool_pair == True):
        state,action = statesActionsList[O][0],statesActionsList[0][1]
        pi = policy_pair[bank_state][state][action]
        pi = result + alpha*pi
        policy_simple[bank_state][state][action] = pi  
        k = 1
        if (state == 2):
            while (statesActionsList[k][0] < 12):
                #Revenir au tableau as
                state,action = statesActionsList[k][0],statesActionsList[k][1]
                pi = policy_as[bank_state][state][action]
                pi = result + alpha*pi
                policy_as[bank_state][state][action] = pi
                k += 1
            #revenir au tableau normal
        for couple in statesActionsList[k:]:
            state,action = couple[0],couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = result + alpha*pi
            policy_simple[bank_state][state][action] = pi
    
    ###Cas ou la main initiale comportait un as
    if (bool_as == True):
        k = 0
        #Tant qu'on a pas encore tire l'as, on modifie le tableau simple
        while k < position_as - 1 :
            state,action = statesActionsList[k][0],statesActionsList[k][1]
            pi = policy_simple[bank_state][state][action]
            pi = result + alpha*pi
            policy_simple[bank_state][state][action] = pi
        #On a trouve un as plus un total <= 11, on modifie dans le tableau as               
        while (statesActionsList[k][0] < 12):
            #Revenir au tableau as
            state,action = statesActionsList[k][0],statesActionsList[k][1]
            pi = policy_as[bank_state][state][action]
            pi = result + alpha*pi
            policy_as[bank_state][state][action] = pi
            k += 1
        #revenir au tableau normal lorsque le total depasse 11 : l'as vaut maintenant 1
        for couple in statesActionsList[k:]:
            state,action = couple[0],couple[1]
            pi = policy_simple[bank_state][state][action]
            pi = result + alpha*pi
            policy_simple[bank_state][state][action] = pi




  