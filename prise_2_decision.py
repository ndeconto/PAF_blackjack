# -*- coding: utf-8 -*-
from cartes import *
from algo_monte_carlo import *
from Bank_Playing import *
import copy
############################################################################################################################
nombre_etats_joue = [0 for i in range (12)] #Nombre de fois que chaque Ã©tat sort : [<12,12,13,14,15,16,17,18,19,20,21,>21]
nombre_etats_gagnes = [0 for i in range (12)]
stat_gain = [0 for i in range (12)] #Proba de gagner par etat [<12,12,13,...,21,>21]
nb_partie_jouee = 0
nombre_partie_gagnee = 0

def win2(player_hand,bank_hand,bet): #bet est la mise 
    player_best_value = player_hand.valeur
    bank_best_value = bank_hand.valeur
    if(player_best_value > 21):
        return(-bet)
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
    

def win_split(player_hand_1,player_hand_2,bank_hand,bet):
    player_best_value_1 = player_hand_1.valeur
    player_best_value_2 = player_hand_2.valeur
    bank_best_value = bank_hand.valeur
    vic = 0
    draw = 0
    loose = 0
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
        return(2)
    if (draw == 2):
        return(0)
    if (loose == 2):
        return(-2)
    if (vic == 1 and draw == 1):
        return(1)
    if (draw == 1 and loose == 1):
        return(-1)
    if (loose == 1 and vic == 1):
        return(0)


def manche2(bet, learning=True): #bet est la mise
    global epsilon
    
    if not learning:
        epsilon_copy = epsilon
        epsilon = 0
    
    deck = Deck()
    player_statesActions = []
    bool_as = False
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
        bool_as = True
    else:
        player_state = player_card.get_valeur()
        
    player_card = deck.piocher()            #2e carte
    player_hand.ajouter(player_card)
    if (isAs(player_card)):                 #Si c'est un as
        player_state += 1
        bool_as = True
    else:
        player_state += player_card.get_valeur()
        
    if (player_hand.get_card_at(0)==player_hand.get_card_at(1)):    #Si on a une paire
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
        
      
    
    #print("etat initial", player_state)
    #print("boulasses", bool_as)
    #print("bool_can_split", bool_can_split)
    #print("bool_can_DOBLE", bool_can_doble)
    #print("bank_state", bank_state)    
    print("new game")
    player_decision = makeDecision2([player_state,bool_as,bool_can_split,bool_can_doble],(bank_state-1) % 10)   #decision du joueur
    #print("decision initiale", player_decision)
    player_statesActions.append([player_state,player_decision])
    #####################Ce que l'on fait si la decision c'est de s'arreter#####################################
    while(player_decision != 0):
        print("boucle while")
        if (player_decision == 1):
    #####################Ce que l'on fait si la decision c'est de tirer#########################################
            player_card = deck.piocher()            #On pioche
            #print("state", player_state)
            #print("bank_state", (bank_state-1) % 10)
            #print("split" , bool_can_split)
            #print("double", bool_can_doble)
            number_card += 1
            bool_can_split,bool_can_doble = False,False
            player_hand.ajouter(player_card)
            if (isAs(player_card)):     #Si c'est un as
                bool_as = True
                player_state += 1
            else:
                player_state += player_card.get_valeur()
                
            #Decision du joueur
            player_decision = makeDecision2([player_state,bool_as,bool_can_split,bool_can_doble],(bank_state-1) % 10)
            print("decision", player_decision)
            player_statesActions.append([player_state,player_decision])
        elif(player_decision == 2):
    #####################Ce que l'on fait si la decision c'est de doubler#######################################
            bet = 2*bet #mise doublee
            bool_dobled = True
            player_card = deck.piocher()
            number_card += 1
            player_hand.ajouter(player_card)
            if (isAs(player_card)):
                bool_as = True
                player_state += 1
            else:
                player_state += player_card.get_valeur()
            player_decision = 0 #Une seule carte Ã  piocher
        elif(player_decision == 3):
    #####################Ce que l'on fait si la decision c'est de splitter######################################    
            bool_splitted = True
            player_card_1 = deck.piocher()
            player_card_2 = deck.piocher()
            player_hand_1 = copy.deepcopy(player_hand)
            player_hand_2 = copy.deepcopy(player_hand)
            player_hand_1.ajouter(player_card_1)
            player_hand_2.ajouter(player_card_2)
            player_decision = 0 #Une seule carte Ã  piocher
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
        updateValue(player_statesActions,bool_as,bool_pair,bank_hand.get_card_at(0)-1,result,mypolicy) #banque state --> premiere carte
        #update_stat_gain(player_statesActions,result,bank_state,player_state)
    ########Fin de la MAJ de mypolicy########
    

    else:
        epsilon = epsilon_copy
        return result


def test_sans_apprendre(n):
    """
        fonction qui n'a rien a faire dans un fichier nommee prise_2_decision
        mais bref...
        cette fonction joue n parties, et renvoie le gain moyen (sachant que la
        mise est 1 de base)
    """

    s = sum(manche2(1, False) for i in range(n))
    return float(s) / n
        

def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)

def update_stat_gain(statesActions,resultat,bank_state,state):
    global nb_partie_jouee
    global nombre_partie_gagnee
    nb_partie_jouee = 0
    nombre_partie_gagnee = 0
    indices_selection_etats_sortis = []
    nb_partie_jouee += 1
    for tab in range (len(statesActions)):
        #print("probleme 1 dans la fx update_stat_gain")
        #print(statesActions[tab][0])
        indices_selection_etats_sortis.append(statesActions[tab][0])
    for k in range(len(indices_selection_etats_sortis)):
        ind = indices_selection_etats_sortis[k]
        nombre_etats_joue[ind] = nombre_etats_joue[ind] + 1
        if (resultat == 2 or resultat == 1):
            nombre_etats_gagnes[ind] = nombre_etats_gagnes[ind] + 1
            nombre_partie_gagnee += 1 
#            if (ind == 11):
#                print("stateActions : ",statesActions[k])
#                print("statesActions : ", statesActions)
#                print("Etats opposant : ", bank_state)
#                print("etat de la main : ", state)  
    for i in range (len(nombre_etats_joue)):
        if (nombre_etats_joue[i] != 0):
            stat_gain[i] = nombre_etats_gagnes[i] / nombre_etats_joue[i]
    return(nombre_partie_gagnee / nb_partie_jouee)
