#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:23:29 2017

@author: majdagoumi
"""
from idee_automatisation_jeux import *
from algo_MC_2 import *
from prise_2_decision import *
import numpy as np
import csv
import collections
from openpyxl import Workbook
from load_object import *


def f(values):
	return values.index(max(values))

def apprentissage(n):
    victoire = 0
    for k in range(n):
        victoire = manche()
    print("My policy : ",mypolicy)
    print("Stats victoires : ",stat_gain)
    print("Nb etat joué et nb etats ganés : ", nombre_etats_joue,nombre_etats_gagnes)
    print("Pourcentage de victoire : ",100*nombre_etats_gagnes[0]/nombre_etats_joue[0])

    result = [[f(values) for values in i]for i in mypolicy]
#    print("     ↑ low enemy card   | high enemy card ↓")
#    print("     <- low value hand  |  high value hand ->")
#    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in result]))

def apprentissage2(n,bet,f):
    victoire = 0
    global epsilon
    for k in range(int(n/2)):
        epsilon = f(k)
        victoire = manche2(bet)
    print("Statistiques :\n")
    print(victoire)
    print("Epsilon final, alpha : ",epsilon,", ",alpha)

def f(k):
        return(0.05)


def save_mypolicy(p1,p2,p3): #Le fichier sauvegarde est un vecteur comportant les trois tableaux
#from load_object import *
#IND : Pour sauvegarder : ecrire save_mypolicy(policy_simple,policy_as,policy_pair)
#      Pour charger ecrire : policy_simple,policy_as,policy_pair = getPolicy()[0],getPolicy()[1],getPolicy[2]

    policy = [p1,p2,p3]
    file_handler = open("mypolicy", "wb")
    pickle.dump(policy,file_handler)
    

def save_to_xlsx():
    wb = Workbook()
    
    # grab the active worksheet
    ws = wb.active
    
    ws['A1']="Simple :"
    for row in getPolicy()[0] :
        ws.append(row)
    
    
    # Save the file
    wb.save("policy_simple.xlsx")



def presenter_resultats(mypolicy):
    matrice_simple = mypolicy[0]
    matrice_as = mypolicy[1]
    matrice_paire = [2]

    
def graphe_vitesse_apprentissage():

    from matplotlib.pyplot import plot, show, xlabel, ylabel

    pas = 2 * 10**5
    a_max = 10**6

    
    lx = range(0, a_max, pas)
    ly = [0] * len(lx)
    
    for i in range(len(lx)):
        ly[i] = test_sans_apprendre(10**5)
        apprentissage2(pas, 1)
        
    xlabel("nombre d'iterations d'apprentissage")
    ylabel("gain moyen pour une mise de 1")
    plot(lx, ly)
    show()

