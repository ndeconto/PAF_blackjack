#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:16:17 2017

@author: majdagoumi
"""
#Créer une manche

from cartes import *
from algo_monte_carlo import *
from Bank_Playing import *


#paquet = Deck() # Paquet de carte pour la manche Si on laisse ça ici, deux manche successive piochent dans le même paquet, on arrive pas à faire une raz du paquet
nombre_etats_joue = [0 for i in range (12)] #Nombre de fois que chaque état sort : [<12,12,13,14,15,16,17,18,19,20,21,>21]
nombre_etats_gagnes = [0 for i in range (12)]
stat_gain = [0 for i in range (12)] #Proba de gagner par état [<12,12,13,...,21,>21]

def win(state,state_oponent): # 2 --> gain, 1 --> égalité, 0 --> perte
    if ((state > state_oponent) and (state < 22)):
        return(2)
    elif ((state < state_oponent) and (state_oponent < 22)):
        return(0)
    elif (state>21 and state_oponent<22):
        return(0)
    elif (state == state_oponent):
        return(1)
    elif (state > 21 and state_oponent > 21):
        return(0)          # Dans les regles qu'on prend nous, considerons que les deux dépassent donne une perte.
    elif (state < 22 and state_oponent > 21):
        return(2)
    else:
        print("Cas d'une issue non traitée dans la fx win")

def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)

def prise_decision(state,statesActions):
    decision = makeDecision(state)
    if state<12 : ind = 0
    elif state>21 : ind = 11
    else: ind = state-11
    statesActions.append([ind,decision])
    return (decision)


def update_stat_gain(statesActions,resultat):
    indices_selection_etats_sortis = []
    for tab in range (len(statesActions)):
        #print("probleme 1 dans la fx update_stat_gain")
        #print(statesActions[tab][0])
        indices_selection_etats_sortis.append(statesActions[tab][0])
    for k in range(len(indices_selection_etats_sortis)):
        ind = indices_selection_etats_sortis[k]
        nombre_etats_joue[ind] = nombre_etats_joue[ind] + 1
        if (resultat == 2 or resultat == 1):
            nombre_etats_gagnes[ind] = nombre_etats_gagnes[ind] + 1
    for i in range (len(nombre_etats_joue)):
        if (nombre_etats_joue[i] != 0):
            stat_gain[i] = nombre_etats_gagnes[i] / nombre_etats_joue[i]
    
    
def calcul_indice(valeur):
    if (valeur < 12):
        return(0)
    elif(valeur > 21):
        return(11)
    else:
        return(11 - valeur)

    
def manche(): 
    paquet = Deck() #Mettre le paquet ici revient à melanger le paquet entre deux tours
    carteb = paquet.piocher() #Premiere carte piochée de la banque
    #Le joueur joue
    statesActions = []
    IsThereAs = False
    strat_a_11 = False
    global main_cree
    
    #main_cree = False
    cartes_piochees = [] #Autre idee pour la création de la main du joueur
    
    decision = 1 #On doit piocher au moins une carte
    state = 0
    while (decision == 1 and state < 22):
        #print("debut de boucle while, etat de la main crée")
        #print(main_cree)
        carte = paquet.piocher()
        cartes_piochees.append(carte)
        valeurs_possibles = carte.get_valeur()
        
        #MAJ de la variable state
        if (isAs(carte) == False):
            
            #Gestion du cas où l'on ne pioche pas d'as
            state = state + valeurs_possibles #Ici un entier car c'est pas un As
            #Prise de décision
            decision = prise_decision(state,statesActions)
            
        else :
            #On vient de piocher un As
            
            if (IsThereAs == False):
                #C'est le premier As pioché
                #Il faut garder une trace de la proba de gagner sachant qu'on est dans un certain état... --> Stat Gain
                #On considere une égalité comme un gain dans les stat (cas d'un etat à 21)
                s1 = state + 1
                s2 = state + 11
                ind1 = calcul_indice(s1)
                ind2 = calcul_indice(s2)
                
                best = max(stat_gain[ind1],stat_gain[ind2])
                if (best == stat_gain[ind1]): #Meilleure stratégie de prendre l'As à 1
                    state = s1
                else: #meilleure stratégie à 11
                    state = s2
                    strat_a_11 = True #On retient qu'on a un as qui vaut 11
                decision = prise_decision(state,statesActions)
                IsThereAs = True #On retient qu'on a vient de piocher un as
            else :
                #C'est le second (ou plus) As pioché
                state = state + 1
                decision = prise_decision(state,statesActions)
                
        #MAJ de la main de joueur      
#        if (main_cree == False): #Gestion du cas de la première carte
#            Player_Hand = Main([carte]) #Est-ce qu'il faut créer une Main sans carte au début ?
#            print("la main n'est toujours pas créé")
#            main_cree == True
#            print("resolution du probleme de création de la main")
#            print(main_cree)
#        else:
#            Player_Hand.ajouter(carte)
#            print("main créé")
        #print("fin de fx while, valeur de decision")  
        #print(decision)
    if (strat_a_11 == True and state > 21): #Si on a choisit de prendre notre As à 11 mais qu'on a dépasser, 21, alors on remet l'As à 1 et on rejoue
        #print("cas ou l'as à 11 depasse, on le remet à 1") #En fait cela revient a dire qu'on choisit à la fin du jeu la valeur réélle de notre As
        state = state - 10
        decision = 1 
    Player_Hand = Main(cartes_piochees)
    
    #A la banque de jouer
#    carteb = paquet.piocher()
    Bank_Hand = Main([carteb])
    decision_bank = bank_playing(Bank_Hand)
    state_bank = 0
    if (isAs(carteb) == True):
        state_bank = 11
    else:
        state_bank = carteb.get_valeur()
    while (decision_bank == 1):
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
    updateValue(statesActions,result,mypolicy)
    update_stat_gain(statesActions,result)
        

def updateValue(statesActionsList,result,mypolicy):#statesActionsList est la liste de couples des (états; actions) prises lors de la partie
    for cpl in statesActionsList:
        pi = mypolicy[cpl[0]][cpl[1]];          #pi est le poids (toujours positif) de la décision cpl[1] dans l'état cpl[0]
        pi = (result + alpha*pi);             #mise à jour du poids
        #if pi<epsilon/(1-alpha) : pi = epsilon/(1-alpha);         #on est à epsilon-greedy transition (sans oublier la normalisation)
        mypolicy[cpl[0]][cpl[1]] = pi			  #mise à jour de policy
    


        
    
    