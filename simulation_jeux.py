#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:37:38 2017

@author: majdagoumi
"""

#Créer une manche

from cartes import *
from algo monte-carlo import *

class Jouer:
    """Classe qui representera une main
       Pour l'instant, les cartes ne sont pas pioché par python"""
    carte1 = input()                        #Respecter la syntaxe du package cartes.py
    carte2 = input()
    main_en_cour = Main(carte1,carte2)
    
    
    
    