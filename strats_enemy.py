# -*- coding: utf-8 -*-
from cartes import *
from Bank_Playing import *
from algo_MC_2 import *

def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)

###Strategie de l'IA --> pour qu'elle joue contre elle-même
def bank_manche_sym(deck,card1,card2):
    bank_state = 0
    bank_hand = Main([card1])
    bool_bank_at_11 = False
    if (isAs(card1) == True):       #Si c'est un as
        bank_state = 11
        bool_bank_at_11 = True
    else:
        bank_state = card1.get_valeur()
    ########A la banque de jouer###########
    bank_decision = 1
    while bank_decision == 1:
        bank_card = deck.piocher()
        bank_hand.ajouter(bank_card)
        bank_decision = bank_playing(bank_hand)
        bank_state = bank_hand.get_m_valeur()
    ########La banque a fini de jouer########
    return [], False, False, 0,False, bank_hand, False, False