#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:16:17 2017

@author: majdagoumi
"""
#Creer une manche

from cartes import *
from algo_monte_carlo import *
from Bank_Playing import *


#paquet = Deck() # Paquet de carte pour la manche. Si on laisse ça ici, deux manche successive piochent dans le meme paquet, on arrive pas a faire une raz du paquet
nombre_etats_joue = [0 for i in range (12)] #Nombre de fois que chaque etat sort : [<12,12,13,14,15,16,17,18,19,20,21,>21]
nombre_etats_gagnes = [0 for i in range (12)]
stat_gain = [0 for i in range (12)] #Proba de gagner par état [<12,12,13,...,21,>21]
nb_partie_jouee = 0
nombre_partie_gagnee = 0


def win(state,state_oponent): # 2 --> gain, 1 --> egalite, 0 --> perte
    if (state > 21):
        return(0)
    elif (state_oponent > 21):
        return(2)
    elif (state > state_oponent):
        return(2)
    elif (state < state_oponent):
        return(0)
    elif (state == state_oponent):
        return(1)
    else:
        print("Cas d'une issue non traitee dans la fx win")

def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)

def prise_decision(state,ennemy_state,statesActions):
    decision = makeDecision2(state,ennemy_state)
    if state<12 : ind = 0
    elif state>21 : ind = 11
    else: ind = state-11
    statesActions.append([ind,decision])
    return (decision)


def update_stat_gain(statesActions,resultat,state_bank,state):
    global nb_partie_jouee
    global nombre_partie_gagnee
    nb_partie_jouee = 0
    nombre_partie_gagnee = 0
    indices_selection_etats_sortis = []
    nb_partie_jouee += 1
    for tab in range (len(statesActions)):
        #print("probleme 1 dans la fx update_stat_gain")
        #print(statesActions[tab][0])
        indices_selection_etats_sortis.append(statesActions[tab][0])
    for k in range(len(indices_selection_etats_sortis)):
        ind = indices_selection_etats_sortis[k]
        nombre_etats_joue[ind] = nombre_etats_joue[ind] + 1
        if (resultat == 2 or resultat == 1):
            nombre_etats_gagnes[ind] = nombre_etats_gagnes[ind] + 1
            nombre_partie_gagnee += 1 
            if (ind == 11):
                print("stateActions : ",statesActions[k])
                print("statesActions : ", statesActions)
                print("Etats opposant : ", state_bank)
                print("etat de la main : ", state)  
    for i in range (len(nombre_etats_joue)):
        if (nombre_etats_joue[i] != 0):
            stat_gain[i] = nombre_etats_gagnes[i] / nombre_etats_joue[i]
    return(nombre_partie_gagnee / nb_partie_jouee)
    
def calcul_indice(valeur):
    if (valeur < 12):
        return(0)
    elif(valeur > 21):
        return(11)
    else:
        return(11 - valeur)
    
    
def manche(): 
    paquet = Deck() #Mettre le paquet ici revient a melanger le paquet entre deux tours
    carteb = paquet.piocher() #Premiere carte piochee de la banque
    state_bank = 0
    ennemy_state = 0
    if (isAs(carteb)):
        #La carte de la banque est un as
        ennemy_state = 1
    else:
        ennemy_state = carteb.get_valeur()
    #Le joueur joue
    statesActions = []
    IsThereAs = False
    strat_a_11 = False
    indiceAs = 0
    global main_cree
    
    #main_cree = False
    cartes_piochees = [] #Autre idee pour la creation de la main du joueur
    
    decision = 1 #On doit piocher au moins une carte
    state = 0
    while (decision == 1 and state < 22):
        #print("debut de boucle while, etat de la main cree")
        #print(main_cree)
        carte = paquet.piocher()
        cartes_piochees.append(carte)
        valeurs_possibles = carte.get_valeur()
        
        #MAJ de la variable state
        if (isAs(carte) == False):
            
            #Gestion du cas ou l'on ne pioche pas d'as
            state = state + valeurs_possibles #Ici un entier car c'est pas un As
            #Prise de decision
            decision = prise_decision(state,ennemy_state,statesActions)
            
        else :
            #On vient de piocher un As
            
            if (IsThereAs == False or strat_a_11 == False):
                #C'est le premier As pioche
                #Il faut garder une trace de la proba de gagner sachant qu'on est dans un certain etat... --> Stat Gain
                #On considere une egalite comme un gain dans les stat (cas d'un etat a 21)
                s1 = state + 1
                s2 = state + 11
                ind1 = calcul_indice(s1)
                ind2 = calcul_indice(s2)
                
                best = max(stat_gain[ind1],stat_gain[ind2])
                if (best == stat_gain[ind1]): #Meilleure strategie de prendre l'As a 1
                    state = s1
                else: #meilleure strategie a 11
                    indiceAs = len(statesActions)
                    state = s2
                    strat_a_11 = True #On retient qu'on a un as qui vaut 11
                decision = prise_decision(state,ennemy_state,statesActions)
                IsThereAs = True #On retient qu'on a vient de piocher un as
            else:
                #C'est le second (ou plus) As pioche
                state = state + 1
                decision = prise_decision(state,ennemy_state,statesActions)
                IsThereAs = True #On retient qu'on a vient de piocher un as
        #MAJ de la main de joueur      
#        if (main_cree == False): #Gestion du cas de la premiere carte
#            Player_Hand = Main([carte]) #Est-ce qu'il faut creer une Main sans carte au debut ?
#            print("la main n'est toujours pas cree")
#            main_cree == True
#            print("resolution du probleme de creation de la main")
#            print(main_cree)
#        else:
#            Player_Hand.ajouter(carte)
#            print("main cree")
        #print("fin de fx while, valeur de decision")  
        #print(decision)
##############################################################################################        
        if (strat_a_11 == True and state > 21): #Si on a choisit de prendre notre As a 11 mais qu'on a depasser, 21, alors on remet l'As a 1 et on rejoue
            #print("cas ou l'as a 11 depasse, on le remet a 1") #En fait cela revient a dire qu'on choisit a la fin du jeu la valeur reelle de notre As
            state = state - 10
            decision = 1 
            for o in range(indiceAs,len(statesActions)):
                statesActions[o][0] = 0
            statesActions.append([calcul_indice(state),1])
##############################################################################################
    Player_Hand = Main(cartes_piochees)
    
    #A la banque de jouer
#    carteb = paquet.piocher()
    Bank_Hand = Main([carteb])
    decision_bank = bank_playing(Bank_Hand)
    if (isAs(carteb) == True):
        state_bank = 11
    else:
        state_bank = carteb.get_valeur()
    while (decision_bank == 1 and state_bank < 22):
        carteb = paquet.piocher()
        Bank_Hand.ajouter(carteb)
        decision_bank = bank_playing(Bank_Hand)
        if (isAs(carteb) == False):
            state_bank = state_bank + carteb.get_valeur()
        else:
            if (state + 11 < 22):
                state_bank = state_bank + 11
            else:
                state_bank = state_bank + 1
            
        
    #resultat de la manche
    #print("fx manche : avant calcul du resultat")
    #print(statesActions)
    result = win(state,state_bank)
    #print("main joueur + valeur main : ",Player_Hand," / ",state)
    #print("Main de la banque / valeur de la banque : ",Bank_Hand," / ",state_bank)
    #print("issue : ",result)
    #print("fx manche : resultat obtenu")
    #print(result)
    updateValue(statesActions,ennemy_state,result,mypolicy)
    pourcentage_gagne = update_stat_gain(statesActions,result,state_bank,state)
    return(pourcentage_gagne)

def updateValue(statesActionsList,ennemy_state,result,mypolicy):#statesActionsList est la liste de couples des (etats; actions) prises lors de la partie
    for cpl in statesActionsList:
        #print("cpl[0]" , cpl[0])
        #print("cpl[1]" , cpl[1])
        #print("ennemy_state : ", ennemy_state )
        pi = mypolicy[ennemy_state-1][cpl[0]][cpl[1]];          #pi est le poids (toujours positif) de la decision cpl[1] dans l'etat cpl[0]
        pi = (result + alpha*pi);             #mise a jour du poids
        #if pi<epsilon/(1-alpha) : pi = epsilon/(1-alpha);         #on est a epsilon-greedy transition (sans oublier la normalisation)
        mypolicy[ennemy_state-1][cpl[0]][cpl[1]] = pi			  #mise a jour de policy
    


        
    
    