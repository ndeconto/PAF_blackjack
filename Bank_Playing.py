#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:57:12 2017

@author: majdagoumi
"""

from cartes import *

#Définition du paquet de cartes
paquet = Deck()

def bank_playing():
    
    #Main de la banque
    carte1 = paquet.piocher()
    carte2 = paquet.piocher()
    bank_hand = [carte1,carte2]
    
    #Début calcul etat initial
    somme = 0
    if (isinstance(carte1.get_valeur(),int) and isinstance(carte2.get_valeur(),int)):
        somme = carte1.get_valeur() + carte2.get_valeur()
    elif (not((isinstance(carte1.get_valeur(),int))) and (isinstance(carte2.get_valeur(),int))):
        somme = 11 + carte2.get_valeur()
    elif (isinstance(carte1.get_valeur(),int) and not(isinstance(carte2.get_valeur(),int))):
        somme = carte1.get_valeur() + 11
    else :
        somme = 12
    #fin
        
    #Définition de la stratégie de la banque
    while (somme < 17) : 
        carte = paquet.piocher()
        card_value = carte.get_valeur()
        if (not(isinstance(card,int))):
            if (somme < 11):
                somme = somme + 11
            else :
                somme = somme + 1
        else : 
            somme = somme + card_value
    

    