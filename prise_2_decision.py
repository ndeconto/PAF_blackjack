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
deck = Sabot(counter_bound=0)

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

def IA_playing(counter,player_hand,player_decision,bank_card_ini,
               player_statesActions,player_state,position_as,bool_as_choice,
               bool_can_split,bool_splitted,bool_can_doble,
               bool_dobled,bool_pair,number_card,bank_hand,bet,bank_state):
 
###But du jeux : ecrire une fonction que joue, en prenant les parametres definissant le contexte en arguement. 
###Intialement, on appelle la fx avec des parametre de depart (0 et False un peu partout), en cas d'appel recursif,
###on peut passer le contexte en argument, et jouer la partie comme ça.    
    
    counter = deck.get_counter()
    
    player_statesActions_1 = []
    player_statesActions_2 = []
    #####################Entree de la boucle while#####################################
    #print("valeur de player decision avant la boucle while : ",player_decision)
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
            
            counter = deck.get_counter()
                
            #Decision du joueur
            player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble, counter],(bank_state-1) % 10)
            player_statesActions.append([player_state,player_decision, counter])
            
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
            
            counter = deck.get_counter()
            player_statesActions.append([player_state,0,counter])
            player_decision = 0 #Une seule carte a piocher
            
        elif(player_decision == 3):
            #print("valeur de player decision dans la boucle de split : ",player_decision)
    #####################Ce que l'on fait si la decision c'est de splitter######################################  
            bool_splitted = True
            player_card_1 = deck.piocher()
            player_card_2 = deck.piocher()
            player_hand_1 = Main([player_hand.contenu[0]])
            player_hand_2 = Main([player_hand.contenu[1]])
            player_hand_1.ajouter(player_card_1)
            player_hand_2.ajouter(player_card_2)
            player_state_1 = calcul_state(player_hand_1)
            player_state_2 = calcul_state(player_hand_2) 
            bool_as_choice_1 = is_starting_with_as(player_hand_1)
            bool_as_choice_2 = is_starting_with_as(player_hand_2)
            position_as_1 = 0
            position_as_2 = 0
            if (bool_as_choice_1 == True):
                position_as_1 = 1
            if (bool_as_choice_2 == True):
                position_as_2 = 1
            bool_can_split_1 = is_pair(player_hand_1)
            bool_can_split_2 = is_pair(player_hand_2)
            bool_pair_1 = bool_can_split_1
            bool_pair_2 = bool_can_split_2
            player_decision_1 = makeDecision3([player_state_1,bool_as_choice_1,bool_can_split_1,True, deck.get_counter()],(bank_state-1) % 10) 
            player_decision_2 = makeDecision3([player_state_2,bool_as_choice_2,bool_can_split_2,True, deck.get_counter()],(bank_state-1) % 10)
            player_statesActions_1 = [[player_state_1,player_decision_1,counter]]
            player_statesActions_2 = [[player_state_2,player_decision_2,counter]]
            #print("cas split dans appel recurcif, decisions 1 et 2 : ",player_decision_1,player_decision_2)
            
            
            
            player_hand_1, player_statesActions_1,per_vic,gain = IA_playing(deck.get_counter(),player_hand_1,player_decision_1,bank_card_ini,
               player_statesActions_1,player_state_1,position_as_1,bool_as_choice_1,
               bool_can_split_1,False,True,
               False,bool_pair_1,2,bank_hand,bet,bank_state)
            player_hand_2, player_statesActions_2,per_vic,gain = IA_playing(deck.get_counter(),player_hand_2,player_decision_2,bank_card_ini,
               player_statesActions_2,player_state_2,position_as_2,bool_as_choice_2,
               bool_can_split_2,False,True,
               False,bool_pair_2,2,bank_hand,bet,bank_state)
            player_decision = 0
    

    ########MAJ de my policy#################
    if (bool_splitted == False):
        result = win2(player_hand,bank_hand,bet)
        #print("result win2 : ", result)
    else:
        result = win_split(player_hand_1,player_hand_2,bank_hand,bet)
#        result_1 = win2(player_hand,bank_hand,bet)
#        result_2 = win2(player_hand,bank_hand,bet)
        
        ###Trois update value : le premier tableau, qui indique le win ou loose pour un split
        ###Puis dans le cas des deux sous-mains, qui correspondent eventuellement a des parties 
        ###softAs ou bien normale.
    update_value3(player_statesActions,bool_as_choice,bool_pair,bank_hand.get_card_at(0)-1,result,position_as)
#        update_value3(player_statesActions_1,bool_as_choice_1,bool_pair_1,bank_hand.get_card_at(0)-1,result_1,position_as)
#        update_value3(player_statesActions_2,bool_as_choice_2,bool_pair_2,bank_hand.get_card_at(0)-1,result_2,position_as)
        #print("result winsplit",result)

#        print("Main du joueur : ", player_hand)
    pourcentage_victoire, gain = update_stats_gains(result)
    ########Fin de la MAJ de mypolicy########
###       
    return(player_hand,player_statesActions,pourcentage_victoire,gain) ###Deux premier arg pour appel recursif, deux deuxieme pour exploitation de stats
###
def is_pair(hand_of_two_cards):
    if (hand_of_two_cards.get_card_at_high(0) == hand_of_two_cards.get_card_at_high(1)):
        return(True)
    return(False)

def calcul_state(hand):
    liste = hand.contenu
    state = 0
    for carte in liste:
        if (isAs(carte)):
            state += 1
        else:
            state += carte.get_valeur()
    return(state)
        
def is_starting_with_as(hand):
    liste = hand.contenu
    for carte in liste:
        if (isAs(carte)):
            return(True)
    return(False)






def manche2(bet, learning=True): #bet est la mise
    global epsilon
    deck.nouvelle_manche()

    
    
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
    counter = 0
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
        
        
    ###Tirage de la première carte de la banque###
    bank_state = 0
    bank_card_ini = deck.piocher()
    bank_hand = Main([bank_card_ini])
    bool_bank_at_11 = False
    if (isAs(bank_card_ini) == True):       #Si c'est un as
        bank_state = 11
        bool_bank_at_11 = True
    else:
        bank_state = bank_card_ini.get_valeur()
        
     ########A la banque de jouer###########
    bank_decision = 1
    while bank_decision == 1:
        bank_card = deck.piocher()
        bank_hand.ajouter(bank_card)
        bank_decision = bank_playing(bank_hand)
        bank_state = bank_hand.get_m_valeur()
    ########La banque a fini de jouer########
   
    ########L'IA joue#############
    player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble, counter],(bank_state-1) % 10)   #decision du joueur
    player_statesActions.append([player_state,player_decision, counter])
    player_hand,player_statesActions,pourcentage_victoire,gain = IA_playing(counter,player_hand,player_decision,bank_card_ini,
               player_statesActions,player_state,position_as,bool_as_choice,
               bool_can_split,bool_splitted,bool_can_doble,
               bool_dobled,bool_pair,number_card,bank_hand,bet,bank_state)
    return(pourcentage_victoire,gain)
    

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

        
        
        
def update_stats_gains(result):
    global nb_parties_gagnees, nb_parties_jouees, mise_gagnee, mise_investie
    
    mise_investie+=1
    nb_parties_jouees+=1
    mise_gagnee+=result
    if (result > 0):
        nb_parties_gagnees+=1
    
    pourcentage_victoire = str((nb_parties_gagnees/nb_parties_jouees)*100) + "% de victoires"
    gain = "Gain par partie : " + str(mise_gagnee/mise_investie) + " millions d'euros"
    
    return pourcentage_victoire, gain

