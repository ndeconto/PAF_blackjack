#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:37:38 2017

@author: majdagoumi
"""

#Créer une manche

from cartes import *
from algo monte-carlo import *

def win(state):
    state_oponent = input("Entrez l'état du jeu adverse") #Etat du jeu de la personne en face
    if (state > state_oponent && state < 22):
        return(1)
    else if (state < state_oponent && state_oponent < 22):
        return(-1)
    else if (state == state_oponant):
        return(0)
    else if (state > 21 and state_oponent > 21):
        return(-1)          #Dans les regles qu'on prend nous, considerons que les deux dépassent donne une perte.

class Jouer : 
    game = AlgoMC
    play = input("Entrez 'play' pour jouer une autre manche")  #entrer "play" pour jouer une manche
    if (play == "play"):
        Manche(game.actions,game.states,game.alpha,game.epsilon,game.policy)
    
class Manche : 
    """Classe qui representera une main
       Pour l'instant, les cartes ne sont pas pioché par python"""
    def __init__(self,actions,states,alpha,epsilon,policy):
    decision = 0 
    state = 0
    carte1 = input("Premiere carte reçue (hauteur de la carte seulement)")                        #Respecter la syntaxe du package cartes.py
    carte2 = input("Seconde carte reçue (hauteur de la carte seulement)")
    main_en_cour = Main(carte1,carte2)
    
    #Début calcul etat initial
    if (isinstance(carte1.get_valeur(),int) && isinstance(carte1.get_valeur(),int)):
        state = carte1.get_valeur() + carte2.get_valeur()
    else if (!isinstance(carte1.get_valeur(),int) && isinstance(carte1.get_valeur(),int)):
        state = 11 + carte2.get_valeur()
    else if (isinstance(carte1.get_valeur(),int) && !isinstance(carte1.get_valeur(),int)):
        state = carte1.get_valeur() + 11
    else :
        state = 12
    #fin
    
    
    #premiere prise de décision
    decision = makeDecision(state)
    
    #Boucle de jeu. Pour l'instant seulement deux actions. A adapter si on veut plus d'actions.
    while (decision == 1): 
        carte = input("Hauteur de la carte tirée")
        Main.ajouter(carte)
        #selon la carte tirée, MAJ de la main puis de la valeur state
        if (isinstance(carte.get_valeur(),int)):
            state = state + carte.get_valeur()
        else :
            choix = input("Choisissez la valeur de votre AS : '1' ou '11')                 #Choisir la valeur de notre As : 1 ou 11
            if (choix == '1'):
                state = state + 1
            else :
                state = state + 11
        decision = makeDecision(state)
    
    #On est à la fin de la manche : on connait l'état, reste à évaluer si c'est un gain ou une perte. Pour l'instant gain unitaire.
    result = win(state)
    
    
        
    
    