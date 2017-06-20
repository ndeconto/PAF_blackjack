from cartes import *
from algo_monte_carlo import *
from Bank_Playing import *
############################################################################################################################
nombre_etats_joue = [0 for i in range (12)] #Nombre de fois que chaque état sort : [<12,12,13,14,15,16,17,18,19,20,21,>21]
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
    elif(player_best_player == bank_best_value):
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
    if (win2(player_best_value_1,bank_best_value,bet) == bet):
        vic += 1
    if (win2(player_best_value_2,bank_best_value,bet) == bet):
        vic += 1
    if (win2(player_best_value_1,bank_best_value,bet) == - bet):
        loose += 1
    if (win2(player_best_value_2,bank_best_value,bet) == - bet):
        loose += 1
    if (win2(player_best_value_1,bank_best_value,bet) == 0):
        draw += 1
    if (win2(player_best_value_2,bank_best_value,bet) == 0):
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


def manche2(bet): #bet est la mise
    deck = Deck()
    player_statesActions = []
    bool_as = False
    bool_can_split = False
    bool_splitted = False
    bool_can_doble = False
    bool_dobled = False
    bool_paire = False
    number_card = 1
    bank_card = deck.piocher()
    ennemy_state = 0 # 1 = as, 2= deux .... 10 = 10 ou tete
    player_card = deck.piocher()
    bank_hand = Main([bank_card])
    player_hand = Main([player_card])
    player_state = 0
    bank_state = 0
    player_decision = 0
    bank_decision = 0
    result = 0
    if (isAs(player_card)):
        player_state = 1
        bool_as = True
    else:
        player_state = player_card.get_valeur()
    if (isAs(bank_card)):
        ennemy_state = 1
    else:
        ennemy_state = bank_card.get_valeur()
        
    player_decision = makeDecision2([player_state,bool_as,bool_can_split,bool_can_doble],bank_state-1)
    player_statesActions.append([player_state,Player_decision])
    #####################Ce que l'on fait si la decision c'est de s'arreter#####################################
    while(player_decision != 0):
        if (player_decision == 1):
    #####################Ce que l'on fait si la decision c'est de tirer#########################################
            if(number_card != 2):
                bool_can_split,bool_can_doble = False,False
            player_card = deck.piocher()
            number_card += 1
            player_hand.ajouter(player_card)
            if (isAs(player_card)):
                bool_as = True
                player_state += 1
            else:
                player_state += player_card.get_valeur()
            if(number_card == 2):
                bool_can_doble = True
                bool_pair = True
                if (get_card_at(0)==get_card_at(1)):
                    bool_can_split = True
            player_decision = makedecision2([player_state,bool_as,bool_can_split,bool_can_doble],bank_state-1)
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
            player_statesActions.append([player_state,player_decision])
            player_decision = 0 #Une seule carte à piocher
        elif(player_decision == 3):
    #####################Ce que l'on fait si la decision c'est de splitter######################################    
            bool_splitted = True
            player_card_1 = deck.piocher()
            player_card_2 = deck.piocher()
            player_hand_1 = copy.deepcopy(player_hand)
            player_hand_2 = copy.deepcopy(player_hand)
            player_hand_1.ajouter(player_card_1)
            player_hand_2.ajouter(player_card_2)
            if(isAs(player_card_1) or isAs(player_card_2)):
                bool_as = True
            player_statesActions.append([player_state,player_decision])
            player_decision = 0 #Une seule carte à piocher
    ###############################################FIN DU WHILE#################################################
    
    ########A la banque de jouer###########
    bank_decision = bank_playing(bank_hand)
    bank_state = 0
    bool_bank_at_11 = False
    if (isAs(bank_card) == True):
        bank_state = 11
        bool_bank_at_11 = True
    else:
        bank_state = bank_card.get_valeur()
    while (bank_decision == 1 and bank_state < 22):
        bank_card = paquet.piocher()
        bank_hand.ajouter(carteb)
        bank_decision = bank_playing(bank_hand)
        if (isAs(bank_card) == False):
            state_bank = state_bank + carteb.get_valeur()
        else:
            bool_bank_get_as
            if (state_bank + 11 < 22):
                state_bank = state_bank + 11
                bool_bank_at_11 = True
            else:
                state_bank = state_bank + 1
        if(state_bank > 21 and bool_bank_at_11 == True):
            bank_state = bank_state - 10
            bool_bank_at_11 = False
            bank_decision = 1    
    ########La banque a fini de jouer########
    
    ########MAJ de my policy#################
    if (bool_splited == False):
        result = win2(player_hand,bank_hand,bet)
    else:
        result = win_split(player_hand_1,player_hand_2,bank_hand,bet)
    updateValue(player_statesActions,bool_as,bool_pair,bank_hand.get_card_at(0),result,mypolicy) #banque state --> premiere carte
    update_stat_gain(player_statesActions,result,bank_state,player_state)
    ########Fin de la MAJ de mypolicy########
    





def isAs(carte):
    if (isinstance(carte.get_valeur(),int)):
        return(False)
    else:
        return(True)

def update_stat_gain(statesActions,resultat,state_bank,state):
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
#                print("Etats opposant : ", state_bank)
#                print("etat de la main : ", state)  
    for i in range (len(nombre_etats_joue)):
        if (nombre_etats_joue[i] != 0):
            stat_gain[i] = nombre_etats_gagnes[i] / nombre_etats_joue[i]
    return(nombre_partie_gagnee / nb_partie_jouee)
