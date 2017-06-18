#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:37:38 2017

@author: majdagoumi
"""

#Créer une manche

from cartes import *
from algo_monte_carlo import *

def win(state, state_oponent):
    if (((state > state_oponent) or (state_oponent>21)) and (state < 22)):
        return(2)
    elif ((state < state_oponent) and (state_oponent < 22)):
        return(0)
    elif (state>21 and state_oponent<22):
        return(0)
    elif (state == state_oponent):
        return(1)
    elif (state > 21 and state_oponent > 21):
        return(0)          #Dans les regles qu'on prend nous, considerons que les deux dépassent donne une perte.

def ind(state):
    if state<12 : return 0
    elif state>21 : return 11
    else: return state-11

    
def manche(): 
    """Fonction qui representera une main
       Pour l'instant, les cartes ne sont pas pioché par python"""

    jeu = Deck()
    """
    carte1 = int(input("Premiere carte reçue (hauteur de la carte seulement) : "))   #Respecter la syntaxe du package cartes.py
    carte2 = int(input("Seconde carte reçue (hauteur de la carte seulement) : "))
    state_oponent = int(input("Entrez l'état du jeu adverse : ")) #Etat du jeu de la personne en face
    carte1, carte2 = Carte(carte1, COEUR), Carte(carte2, COEUR)"""
    carte1, carte2 = jeu.piocher(), jeu.piocher()  #cartes piochée par nous
    carte3, carte4 = jeu.piocher(), jeu.piocher()  #cartes de la banque
    main_en_cours = Main([carte1,carte2])
    main_adverse = Main([carte3,carte4])
    statesActions =[] 
    #Début calcul etat initial
    
    #à conserver pour le cas où l'as prendra plusieurs valeurs?
    '''if (isinstance(carte1.get_valeur(),int) and isinstance(carte2.get_valeur(),int)):
        state = carte1.get_valeur() + carte2.get_valeur()
    elif (not((isinstance(carte1.get_valeur(),int))) and (isinstance(carte2.get_valeur(),int))):
        state = 11 + carte2.get_valeur()
    elif (isinstance(carte1.get_valeur(),int) and not(isinstance(carte2.get_valeur(),int))):
        state = carte1.get_valeur() + 11
    else :
        state = 12

    if (isinstance(carte3.get_valeur(),int)):
    	state_oponent = carte3.get_valeur() - 1
    else : state_oponent = 0'''

    state = main_en_cours.get_m_valeur()
    score_oponent = main_adverse.get_m_valeur()
    state_oponent = carte3.get_valeur() - 1
    #fin

    #stratégie de la banque
    while score_oponent<17 :
    	main_adverse.ajouter(jeu.piocher())
    	score_oponent = main_adverse.get_m_valeur()
    
    #premiere prise de décision
    decision = makeDecision2(state,state_oponent)
    statesActions.append([state_oponent, ind(state), decision]) 
    #Boucle de jeu. Pour l'instant seulement deux actions. A adapter si on veut plus d'actions.
    while (decision == 1 and state<22): 
        carte = jeu.piocher()
        main_en_cours.ajouter(carte)
        #selon la carte tirée, MAJ de la main puis de la valeur state
        state = main_en_cours.get_m_valeur()
        decision = makeDecision2(state,state_oponent)
        statesActions.append([state_oponent,ind(state),decision])
    
    #On est à la fin de la manche : on connait l'état, reste à évaluer si c'est un gain ou une perte. Pour l'instant gain unitaire.
    result = win(state, score_oponent)
    updateValue(statesActions, result, mypolicy)
 

def updateValue(statesActionsList,result,mypolicy):#statesActionsList est la liste de couples des (états; actions) prises lors de la partie
    #print(mypolicy)
    #print(statesActionsList)
    for cpl in statesActionsList:
    	#print(cpl)
        pi = mypolicy[cpl[0]]
        pi = pi[cpl[1]]
        pi = pi[cpl[2]];          #pi est le poids (toujours positif) de la décision cpl[1] dans l'état cpl[0]
        pi = (result + alpha*pi);             #mise à jour du poids
        #if pi<epsilon/(1-alpha) : pi = epsilon/(1-alpha);         #on est à epsilon-greedy transition (sans oublier la normalisation)
        mypolicy[cpl[0]][cpl[1]][cpl[2]] = pi			  #mise à jour de policy
    