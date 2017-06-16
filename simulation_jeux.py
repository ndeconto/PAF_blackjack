#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:37:38 2017

@author: majdagoumi
"""

#Créer une manche

from cartes import *
from algo_monte_carlo import *

def win(state):
    state_oponent = input("Entrez l'état du jeu adverse : ") #Etat du jeu de la personne en face
    state_oponent = int(state_oponent)
    if ((state > state_oponent) and (state < 22)):
        return(1)
    elif ((state < state_oponent) and (state_oponent < 22)):
        return(-1)
    elif (state == state_oponent):
        return(0)
    elif (state > 21 and state_oponent > 21):
        return(-1)          #Dans les regles qu'on prend nous, considerons que les deux dépassent donne une perte.



    
def manche(): 
    """Fonction qui representera une main
       Pour l'instant, les cartes ne sont pas pioché par python"""

    
    carte1 = input("Premiere carte reçue (hauteur de la carte seulement) : ")   #Respecter la syntaxe du package cartes.py
    carte2 = input("Seconde carte reçue (hauteur de la carte seulement) : ")
    carte1, carte2 = Carte(int(carte1), COEUR), Carte(int(carte2), COEUR)
    main_en_cours = Main([carte1,carte2])
    
    statesActions =[] 
    #Début calcul etat initial
    if (isinstance(carte1.get_valeur(),int) and isinstance(carte2.get_valeur(),int)):
        state = carte1.get_valeur() + carte2.get_valeur()
    elif (not((isinstance(carte1.get_valeur(),int))) and (isinstance(carte2.get_valeur(),int))):
        state = 11 + carte2.get_valeur()
    elif (isinstance(carte1.get_valeur(),int) and not(isinstance(carte2.get_valeur(),int))):
        state = carte1.get_valeur() + 11
    else :
        state = 12
    #fin
    
    
    #premiere prise de décision
    decision = makeDecision(state)
    if state<12 : ind = 0
    elif state>21 : ind = -1
    else: ind = state-11
    statesActions.append([ind,decision]) 
    #Boucle de jeu. Pour l'instant seulement deux actions. A adapter si on veut plus d'actions.
    while (decision == 1): 
        carte = input("Hauteur de la carte tirée : ")
        carte = Carte(int(carte),COEUR)
        main_en_cours.ajouter(carte)
        #selon la carte tirée, MAJ de la main puis de la valeur state
        if (isinstance(carte.get_valeur(),int)):
            state = state + carte.get_valeur()
        else :
            choix = input("Choisissez la valeur de votre AS : '1' ou '11' : ")                 #Choisir la valeur de notre As : 1 ou 11
            if (choix == '1'):
                state = state + 1
            else :
                state = state + 11
        decision = makeDecision(state)
        if state<12 : ind = 0
        elif state>21 : ind = -1
        else: ind = state-11
        statesActions.append([ind,decision])
    
    #On est à la fin de la manche : on connait l'état, reste à évaluer si c'est un gain ou une perte. Pour l'instant gain unitaire.
    result = win(state)
    updateValue(statesActions,result)
    
    
    
        
    
    