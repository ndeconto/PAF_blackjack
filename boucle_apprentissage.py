#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:23:29 2017

@author: majdagoumi
"""
from idee_automatisation_jeux import *

def apprentissage(n):
    victoire = 0
    for k in range(n):
        victoire = manche()
#    print("My policy : ",mypolicy)
    print("Stats victoires : ",stat_gain)
    print("Nb etat joué et nb etats ganés : ", nombre_etats_joue,nombre_etats_gagnes)
    print("Pourcentage de victoire : ",100*nombre_etats_gagnes[0]/nombre_etats_joue[0])
    