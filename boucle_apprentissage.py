#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 18:23:29 2017

@author: majdagoumi
"""
from algo_MC_2 import *
from prise_2_decision import *
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Color, PatternFill, Font, Border, Side, Alignment
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
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
    ws['A2']=""
    ws.append(["","< 9"]+list(range(9,22))+["> 21"])
    
    policy = getPolicy()[:]
    i=1
    for row in policy[0] :
        for k in range(len(row)):
            row[k] = row[k].index(max(row[k]))
        ws.append([i]+row)
        i+=1
    
    ws['A14'] = ""
    ws['A15'] = "As :"
    ws['A16'] = ""
    ws.append([""]+["A,"+str(k) for k in range (2,11)])
    
    i=1
    for row in policy[1] :
        for k in range(len(row)):
            row[k] = row[k].index(max(row[k]))
        ws.append([i]+row)
        i+=1
    
    ws['A28'] = ""
    ws['A29'] = "Paires :"
    ws['A30'] = ""
    ws.append([""]+["A,A"]+[str(k)+","+str(k) for k in range (2,11)])
    
    i=1
    for row in policy[2] :
        for k in range(len(row)):
            row[k] = row[k].index(max(row[k]))
        ws.append([i]+row)
        i+=1
    
    ws.conditional_formatting.add('B4:P13',
    ColorScaleRule(start_type='percentile', start_value=10, start_color='FF6666',
                        mid_type='percentile', mid_value=50, mid_color='FFC966',
                        end_type='percentile', end_value=90, end_color='6DC066')
                  )
    
    ws.conditional_formatting.add('B18:J27',
    ColorScaleRule(start_type='percentile', start_value=10, start_color='FF6666',
                        mid_type='percentile', mid_value=50, mid_color='FFC966',
                        end_type='percentile', end_value=90, end_color='6DC066')
                  )
    
    redFill = PatternFill(start_color='FF6666',
                   end_color='FF6666',
                   fill_type='solid')
    
    orangeFill = PatternFill(start_color='FFC966',
                        end_color='FFC966',
                        fill_type='solid')
    
    greenFill = PatternFill(start_color='6DC066',
                        end_color='6DC066',
                        fill_type='solid')
    
    alignment=Alignment(horizontal='center',
                        vertical='center',
                        text_rotation=0,
                        wrap_text=False,
                        shrink_to_fit=False,
                        indent=0)
    
    
    rows = ws['A3:P13']
    side = Side(border_style='thin', color="FF000000")

    rows = list(rows)  # we convert iterator to list for simplicity, but it's not memory efficient solution
    max_y = len(rows) - 1  # index of the last row
    for pos_y, cells in enumerate(rows):
        max_x = len(cells) - 1  # index of the last cell
        for pos_x, cell in enumerate(cells):
            border = Border(
                left=cell.border.left,
                right=cell.border.right,
                top=cell.border.top,
                bottom=cell.border.bottom
            )
            border.left = side
            border.right = side
            border.top = side
            border.bottom = side

            cell.border = border
            cell.alignment=alignment
    
    rows = ws['A17:J27']
    side = Side(border_style='thin', color="FF000000")

    rows = list(rows)  # we convert iterator to list for simplicity, but it's not memory efficient solution
    max_y = len(rows) - 1  # index of the last row
    for pos_y, cells in enumerate(rows):
        max_x = len(cells) - 1  # index of the last cell
        for pos_x, cell in enumerate(cells):
            border = Border(
                left=cell.border.left,
                right=cell.border.right,
                top=cell.border.top,
                bottom=cell.border.bottom
            )
            border.left = side
            border.right = side
            border.top = side
            border.bottom = side

            cell.border = border
            cell.alignment=alignment
    
    rows = ws['A31:K41']
    side = Side(border_style='thin', color="FF000000")

    rows = list(rows)  # we convert iterator to list for simplicity, but it's not memory efficient solution
    max_y = len(rows) - 1  # index of the last row
    for pos_y, cells in enumerate(rows):
        max_x = len(cells) - 1  # index of the last cell
        for pos_x, cell in enumerate(cells):
            border = Border(
                left=cell.border.left,
                right=cell.border.right,
                top=cell.border.top,
                bottom=cell.border.bottom
            )
            border.left = side
            border.right = side
            border.top = side
            border.bottom = side
            if (cell.value==0 and pos_x!=0) :
                cell.fill=redFill
            if (cell.value==1 and pos_x!=0) :
                cell.fill=orangeFill
            if (cell.value==2 and pos_x!=0) :
                cell.fill=greenFill
            if (cell.value==3 and pos_x!=0) : 
                cell.style='Accent4'
            cell.border = border
            cell.alignment=alignment
    
    # Save the file
    wb.save("policy.xlsx")



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

