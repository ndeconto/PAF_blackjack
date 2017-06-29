# -*- coding: utf-8 -*-
from algo_MC_2 import *
from boucle_apprentissage import *
from cartes import *
###############################################################################

###On donne les mains que l'on souhaite entrainer###

def apprentissage_specifique(player_hands_list,bet,ent_by_hand):
    for hand in player_hands_list:
        for k in range (ent_by_hand):
            manche_apprentissage_specifique(hand,1)
        




###On donne une liste comportant la main qu'on souhaite entrainer, et il entraine avec un etat de la banque aleatoire### 
def manche_apprentissage_specifique(player_cards_list,bet, learning = True):
    
    deck = DeckTruque(player_cards_list[:])
    player_hand = Main(player_cards_list[:])
    
    ##########
    
    player_statesActions = []
    position_as = 0
    bool_as_choice = False
    bool_can_split = False
    bool_splitted = False
    bool_can_doble = True
    bool_dobled = False
    bool_pair = False
    number_card = 2
    result = 0
    
    ##Tirage des cartes du joueur
    player_state = 0
    if (player_hand.get_card_at_high(0) == 1):   #Si la premiere carte est un as
        player_state = 1
        bool_as_choice = True
        position_as = 1
    else:
        player_state = player_hand.get_card_at(0)
        

    if (player_hand.get_card_at_high(1) == 1):                 #Si la deuxieme carte est un as
        player_state += 1
        bool_as_choice = True
        position_as = 1
    else:
        player_state += player_hand.get_card_at(1)
        
    if (player_hand.get_card_at_high(0) == player_hand.get_card_at_high(1)):    #Si on a une paire
        bool_can_split = True
        bool_pair = True
        
        
    ##Tirage de la premiÃ¨re carte de la banque
    bank_state = 0
    bank_card = deck.piocher()
    bank_hand = Main([bank_card])
    bool_bank_at_11 = False
    if (isAs(bank_card) == True):       #Si c'est un as
        bank_state = 11
        bool_bank_at_11 = True
    else:
        bank_state = bank_card.get_valeur()
        
      
    
    player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble],(bank_state-1) % 10)   #decision du joueur
    player_statesActions.append([player_state,player_decision])
    
    #####################Entree de la boucle while#####################################
    while(player_decision != 0 and player_state < 32):
        if (player_decision == 1):
    #####################Ce que l'on fait si la decision c'est de tirer#########################################
            player_card = deck.piocher()            #On pioche
            number_card += 1
            bool_can_split,bool_can_doble = False,False
            player_hand.ajouter(player_card)
            if (isAs(player_card) and player_state < 11 and bool_as_choice == False):     #Si c'est un as soft
                bool_as_choice = True
                if (position_as == 0):
                    position_as = len(player_statesActions) + 1
                player_state += 1
            elif (isAs(player_card)): #Si c'est pas un as soft
                player_state += 1
                if (position_as == 0):
                    position_as = len(player_statesActions) + 1
            else :
                player_state += player_card.get_valeur()
            #Decision du joueur
            player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble],(bank_state-1) % 10)
            player_statesActions.append([player_state,player_decision])
        elif(player_decision == 2):
    #####################Ce que l'on fait si la decision c'est de doubler#######################################
            bet = 2*bet #mise doublee
            bool_dobled = True
            player_card = deck.piocher()
            number_card += 1
            player_hand.ajouter(player_card)
            if (isAs(player_card) and player_state < 11 and bool_as_choice == False):     #Si c'est un as soft
                bool_as_choice = True
                if (position_as == 0):
                    position_as = len(player_statesActions) + 1
                player_state += 1
            elif (isAs(player_card)): #Si c'est pas un as soft
                player_state += 1
                if (position_as == 0):
                    position_as = len(player_statesActions) + 1
            else :
                player_state += player_card.get_valeur()
            player_statesActions.append([player_state,0])
            player_decision = 0 #Une seule carte a piocher
            
        elif(player_decision == 3):
    #####################Ce que l'on fait si la decision c'est de splitter######################################    
            bool_splitted = True
            player_card_1 = deck.piocher()
            player_card_2 = deck.piocher()
            player_hand_1 = Main([player_hand.contenu[0]])
            player_hand_2 = Main([player_hand.contenu[0]])
            player_hand_1.ajouter(player_card_1)
            player_hand_2.ajouter(player_card_2)
            player_decision = 0 #Une seule carte a  piocher
    ###############################################FIN DU WHILE#################################################
    
    
    
    
    ########A la banque de jouer###########
    bank_decision = 1
    while bank_decision == 1:
        bank_card = deck.piocher()
        bank_hand.ajouter(bank_card)
        bank_decision = bank_playing(bank_hand)
        bank_state = bank_hand.get_m_valeur()
    ########La banque a fini de jouer########
    
    
    
    
    
    ########MAJ de my policy#################
    if (bool_splitted == False):
        result = win2(player_hand,bank_hand,bet)
        #print("result win2 : ", result)
    else:
        result = win_split(player_hand_1,player_hand_2,bank_hand,bet)
        #print("result winsplit",result)

    if learning :
#        print("Main du joueur : ", player_hand)
        update_value3(player_statesActions,bool_as_choice,bool_pair,bank_hand.get_card_at(0)-1,result,position_as) #banque state --> premiere carte
        victoire = update_stats_gains(player_statesActions,result,bank_state,player_state)
        return victoire
    ########Fin de la MAJ de mypolicy########
    
    
def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)
    
