#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:57:12 2017

@author: majdagoumi
"""

from cartes import *


def bank_playing(bank_hand): #parametre = la main de la banque à un instant T
    #DEBUT calcul de la valeur optimale de la main de la banque
    somme = 0
    val_possibles = bank_hand.valeur
    print(val_possibles)
    taille = len(val_possibles)
    print (taille)
    for k in range(taille):
        if (val_possibles[k] > somme):
            somme = val_possibles[k]
    #FIN
    
    #Définition de la stratégie de la banque : pioche à 16, s'arretes à 17
    if (somme < 17):
        return(1)
    else :
        return(0)
#0:draw => on s'arretes, 1:fold => on continue

    