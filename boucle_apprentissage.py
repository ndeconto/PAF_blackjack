#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:23:29 2017

@author: majdagoumi
"""
from idee_automatisation_jeux import *
from algo_monte_carlo import *

def f(values):
	return values.index(max(values))

def apprentissage(n):
    victoire = 0
    for k in range(n):
        victoire = manche()
#    print("My policy : ",mypolicy)
    print("Stats victoires : ",stat_gain)
    print("Nb etat joué et nb etats ganés : ", nombre_etats_joue,nombre_etats_gagnes)
    print("Pourcentage de victoire : ",100*nombre_etats_gagnes[0]/nombre_etats_joue[0])

    result = [[f(values) for values in i]for i in mypolicy]
    print("     ↑ low enemy card   | high enemy card ↓")
    print("     <- low value hand  |  high value hand ->")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in result]))

def apprentissage2(n,bet):
    victoire = 0
    for k in range(n):
        victoire = manche2(bet)
    print("Stats victoires : ",stat_gain)
    print("Nb etat joué et nb etats ganés : ", nombre_etats_joue,nombre_etats_gagnes)
    print("Pourcentage de victoire : ",100*nombre_etats_gagnes[0]/nombre_etats_joue[0])

    result = [[f(values) for values in i]for i in mypolicy]
    print("     ↑ low enemy card   | high enemy card ↓")
    print("     <- low value hand  |  high value hand ->")
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in result]))


def save_mypolicy(policy):
    file_handler = open("mypolicy", "w")
    pickle.dump(policy,file_handler)
