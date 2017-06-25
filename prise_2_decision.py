# -*- coding: utf-8 -*-
from cartes import *
from Bank_Playing import *
from algo_MC_2 import *
import copy

##


mise_investie = 0
mise_gagnee = 0
nb_parties_gagnees = 0
nb_parties_jouees = 0

##

def win2(player_hand,bank_hand,bet): #bet est la mise 
    player_best_value = player_hand.valeur #La valeur est a tout instant la meilleur valeur possible de la main par construction
    bank_best_value = bank_hand.valeur
    if(player_best_value > 21):
        return(-bet)
    elif(player_best_value == 21 and len(player_hand) == 2):
        if (bank_best_value == 21 and len(bank_hand) == 2):
            return(0)
        else:
            return(1.5*bet)
    elif(player_best_value > bank_best_value):
        return(bet)
    elif(bank_best_value > 21):
        return(bet)
    elif(player_best_value == bank_best_value):
        return(0)
    elif(player_best_value < bank_best_value):
        return(- bet)
    else:
        print("fatal error")
    

##

def win_split(player_hand_1,player_hand_2,bank_hand,bet):
    player_best_value_1 = player_hand_1.valeur
    player_best_value_2 = player_hand_2.valeur
    bank_best_value = bank_hand.valeur
    bank_blackJack = False
    if (bank_best_value == 21 and len(bank_hand) == 2):
        bank_blackJack = True
    vic = 0
    draw = 0
    loose = 0
    blackJack = 0
    if (bank_blackJack == True): ##Si la banque a un BJ, de toute façon elle gagne les deux mains
        return(-2*bet)
    if (win2(player_hand_1,bank_hand,bet) == 1.5*bet):
        blackJack += 1
    if (win2(player_hand_2, bank_hand,bet) == 1.5*bet):
        blackJack += 1
    if (win2(player_hand_1,bank_hand,bet) == bet):
        vic += 1
    if (win2(player_hand_2, bank_hand,bet) == bet):
        vic += 1
    if (win2(player_hand_1,bank_hand,bet) == - bet):
        loose += 1
    if (win2(player_hand_2,bank_hand,bet) == - bet):
        loose += 1
    if (win2(player_hand_1,bank_hand,bet) == 0):
        draw += 1
    if (win2(player_hand_2,bank_hand,bet) == 0):
        draw += 1
    if (vic == 2):
        return(2*bet)
    if (draw == 2):
        return(0)
    if (loose == 2):
        return(-2*bet)
    if (vic == 1 and draw == 1):
        return(1*bet)
    if (draw == 1 and loose == 1):
        return(-1*bet)
    if (loose == 1 and vic == 1):
        return(0)
    if (blackJack == 2):
        return(2*bet)
    if (blackJack == 1 and vic == 1):
        return(2*bet)
    if (blackJack == 1 and draw == 1):
        return(1*bet)
    if (blackJack == 1 and loose == 1):
        return(0*bet)

##

def manche2(bet, learning=True): #bet est la mise
    global epsilon
    
    if not learning:
        epsilon_copy = epsilon
        epsilon = 0
    
    deck = Deck()
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
    player_card = deck.piocher()            #Premiere carte
    player_hand = Main([player_card])
    player_state = 0
    if (isAs(player_card)):                 #Si c'est un as
        player_state = 1
#        bool_as = True
        bool_as_choice = True
        position_as = 1
    else:
        player_state = player_card.get_valeur()
        
    player_card = deck.piocher()            #2e carte
    player_hand.ajouter(player_card)
    if (isAs(player_card)):                 #Si c'est un as
        player_state += 1
        bool_as_choice = True
        position_as = 1
    else:
        player_state += player_card.get_valeur()
        
    if (player_hand.get_card_at_high(0)==player_hand.get_card_at_high(1)):    #Si on a une paire
        bool_can_split = True
        bool_pair = True
        
        
    ##Tirage de la première carte de la banque
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
            player_decision = 0 #Une seule carte a piocher
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
        victoire=update_stats_gains(player_statesActions,result,bank_state,player_state)
        return victoire
    ########Fin de la MAJ de mypolicy########
    

    else:
        epsilon = epsilon_copy
        return result


##

def test_sans_apprendre(n):
    """
        fonction qui n'a rien a faire dans un fichier nommee prise_2_decision
        mais bref...
        cette fonction joue n parties, et renvoie le gain moyen (sachant que la
        mise est 1 de base)
    """

    s = sum(manche2(1, False) for i in range(n))
    return float(s) / n
  
  ##      

def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)
 
 ##

        
        
        
def update_stats_gains(statesActions,result,bank_state,player_state):
    global nb_parties_gagnees, nb_parties_jouees, mise_gagnee, mise_investie
    
    mise_investie+=1
    nb_parties_jouees+=1
    mise_gagnee+=result
    if (result > 0):
        nb_parties_gagnees+=1
    
    pourcentage_victoire = str((nb_parties_gagnees/nb_parties_jouees)*100) + "% de victoires"
    gain = "Gain par partie : " + str(mise_gagnee/mise_investie) + " millions d'euros"
    
    return pourcentage_victoire, gain

