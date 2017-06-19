#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:41:44 2017

@author: majdagoumi
"""
from cartes import *
from algo_monte_carlo import *


#Definition du paquet de cartes
paquet = Deck()

Bank_Hand_used = Main([paquet.piocher()])
carte = paquet.piocher()
Player_Hand_used = [Main([carte])]##Mettre la valeur 1 de l'AS
#Gestion du cas de l'AS

global premierAs
premierAs = False

if (isinstance(carte.get_valeur(),int) == False):
    Player_Hand_used.append(Main([carte])) ##Mettre la valeur 11 de l'AS
    premierAs = True
else:
    premierAs = False


def manche():
    statesActions = [[] for k in range (len(Player_Hand_used))]
    forward = 1
    while (forward == 1):
        forward = tour(Player_Hand_used,statesActions)
            
        
decision0 = 1
decision1 = 1
#Adaptation de la simulation joueur
def tour(hand,statesActions): 
    """renvoie une prise de décision et modifie la main du joueur"""
    if (premierAs == True):
        ###On traite le cas ou le premier as compte pour 1
        if decision0 == 1 :
            state0 = Player_Hand_used[0].valeur
            decision0 = makeDecision(state0)
            if state0<12 : ind = 0
            elif state0>21 : ind = 11
            else: ind = state0-11
            statesActions[0].append([ind,decision0])
        ###Cas ou l'as vaut 11
        if decision1 == 1 :
            state1 = Player_Hand_used[0].valeur
            decision1 = makeDecision(state0)
            if state1<12 : ind = 0
            elif state1>21 : ind = 11
            else: ind = state1-11
            statesActions[1].append([ind,decision1])
        if (decision0 == 1 or decision1 ==1):
            carte = paquet.piocher()
            if decision0==1:
                if (isinstance(carte.get_valeur(),int) == False):
                    Player_Hand_used[0].ajouter(Carte(ASUN,carte.couleur))
                else:
                    Player_Hand_used[0].ajouter(carte)
            if decision1 == 1:
                if (isinstance(carte.get_valeur(),int) == False):
                    Player_Hand_used[1].ajouter(Carte(ASUN,carte.couleur))
                else:
                    Player_Hand_used[1].ajouter(carte)
            return 1
        return 0
    else :
        state = Player_Hand_used[0].valeur
        decision = makeDecision(state)
        if state<12 : ind = 0
        elif state>21 : ind = 11
        else: ind = state-11
        statesActions[0].append([ind,decision])
        if (decision == 1):
            carte = paquet.piocher()
            if (isinstance(carte.get_valeur(),int) == False):
                Player_Hand_used.append(copy.deepcopy(Player_Hand_used[0])) 
                statesActions.append(copy.deepcopy(statesActions[0]))
                Player_Hand_used[0].ajouter(Carte(ASUN,carte.couleur))
                Player_Hand_used[0].ajouter(Carte(ASONZE,carte.couleur))
                premierAs = True
            else :
                Player_Hand_used[0].ajouter(carte)
            return(1)
        else:
            return(0)
