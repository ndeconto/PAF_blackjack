#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 15:41:44 2017

@author: majdagoumi
"""

#Définition du paquet de cartes
paquet = Deck()

Bank_Hand_used = Main([paquet.piocher()])
Player_Hand_used = Main([paquet.piocher()])



def manche():
    statesActions = []
    decision = tour(Player_Hand_used,statesActions)
    while (decision == 1 and state<22):
        Player_Hand_used.piocher()
        #MAJ de la valeur de la main
        tableau_valeur_poosibles_joueur = Player_Hand_used.valeur
        state = 0
        for k in range (len(tableau_valeur_poosibles_joueur)):
            if (tableau_valeur_poosibles_joueur[k] > state and tableau_valeur_poosibles_joueur[k] < 22):
                state = tableau_valeur_poosibles_joueur[k]   







#Adaptation de la simulation joueur
def tour(player_hand,statesActions): 
    """Fonction qui representera une main
       Pour l'instant, les cartes ne sont pas pioché par python"""
    #Début calcul etat initial
    tableau_valeur_poosibles_joueur = player_hand.valeur
    state = 0
    for k in range (len(tableau_valeur_poosibles_joueur)):
        if (tableau_valeur_poosibles_joueur[k] > state and tableau_valeur_poosibles_joueur[k] < 22):
            state = tableau_valeur_poosibles_joueur[k]   
    #fin

    
    #premiere prise de décision
    decision = makeDecision(state)
    if state<12 : ind = 0
    elif state>21 : ind = 11
    else: ind = state-11
    statesActions.append([ind,decision]) 
    return(decision)
    
    
    #Boucle de jeu. Pour l'instant seulement deux actions. A adapter si on veut plus d'actions.
    while (decision == 1 and state<22): 
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
        print(decision)
        if state<12 : ind = 0
        elif state>21 : ind = 11
        else: ind = state-11
        statesActions.append([ind,decision])
    
    #On est à la fin de la manche : on connait l'état, reste à évaluer si c'est un gain ou une perte. Pour l'instant gain unitaire.
    result = win(state)
    print(statesActions)
    updateValue(statesActions,result, mypolicy)
 