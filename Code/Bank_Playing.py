#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:57:12 2017

@author: majdagoumi
"""

from cartes import *
import pickle
import os

def bank_playing(bank_hand): #parametre = la main de la banque a un instant T
    
    somme = bank_hand.get_m_valeur()
    
    #Definition de la strategie de la banque : pioche a 16, s'arretes a 17
    if (somme < 17):
        return(1)
    else :
        return(0)
#0 => on s'arretes, 1 => on continue
