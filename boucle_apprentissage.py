#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:23:29 2017

@author: majdagoumi
"""
from idee_automatisation_jeux import *

def apprentissage(n):
    for k in range(n):
        manche()
#    print("My policy : ",mypolicy)
    print("Stats victoires : ",stat_gain)
    print("Nb etat joué et nb etats ganés : ", nombre_etats_joue,nombre_etats_gagnes)
    victoire = nombre_partie_gagnee / nb_partie_jouee
