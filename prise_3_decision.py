# -*- coding: utf-8 -*-
from cartes import *
from algo_MC_2 import *
import copy

##


mise_investie = 0
mise_gagnee = 0
nb_parties_gagnees = 0
nb_parties_jouees = 0
deck = Sabot()

###Fonction englobant tout
def symetricGame():
    bet = 1
    card1,card2 = initialise()        #On initialise les données communes aux 2 joueurs
    player_hand, bool_dobled, bool_splitted = manche_sym(card_1,card_2)       #Manche de l'IA
    enemy_hand, enemy_bool_dobled, enemy_bool_splitted = manche_sym_enemy(card_1,card_2) #Manche de l'adversaire
    if bool_dobled: bet*=2
    if enemy_bool_dobled: bet*=2                #On double la mise du joueur qu'il double
    if bool_splitted:
        if enemy_bool_splitted:
            result = win_sym_split_split(player_hand[0],player_hand[1],
                                                    enemy_hand[0],enemy_hand[1],
                                                    bet)          #Si les 2 ont split on appelle la fonction win associée
        else:
            result = win_sym_split(player_hand[0], player_hand[1], enemy_hand,bet)    #Si un a splitté on appelle win_sym_split
    elif enemy_bool_splitted:
        result = win_sym_split(enemy_hand[0], enemy_hand[1], player_hand, bet)  #Si l'autre a splitté on appelle win_sym_split "a l'envers"
    return result
    
    
###Fonction initialisant les données communes (2 cartes face visible)    
def initialise():
    global deck
    deck.nouvelle_manche()
    
    card1 = deck.piocher()
    card2 = deck.piocher()
    
    return (card1,card2)
    
    

###Fonctions de détermination du vainqueur et des gains ou pertes de chacun

##Cas ou personne ne split
def win_sym(player_hand,enemy_hand,bet): #bet est la mise 
    player_best_value = player_hand.valeur #La valeur est a tout instant la meilleur valeur possible de la main par construction
    enemy_best_value = enemy_hand.valeur
    if(player_best_value > 21 and enemy_best_value>21):
        return(0)
    elif (player_best_value>21):
        return (-bet)
    elif(player_best_value == 21 and len(player_hand) == 2):
        if (enemy_best_value == 21 and len(enemy_hand) == 2):
            return(0)
        else:
            return(1.5*bet)
    elif (enemy_best_value == 21 and len(enemy_hand) == 2):
        return(-1.5*bet)
    elif(player_best_value > enemy_best_value):
        return(bet)
    elif(enemy_best_value > 21):
        return(bet)
    elif(player_best_value == enemy_best_value):
        return(0)
    elif(player_best_value < enemy_best_value):
        return(- bet)
    else:
        print("fatal error")
    

##Cas ou l'un des deux split
def win_sym_split(player_hand_1,player_hand_2,enemy_hand, bet):
    player_best_value_1 = player_hand_1.valeur
    player_best_value_2 = player_hand_2.valeur
    enemy_best_value = enemy_hand.valeur
    enemy_blackJack = False
    if (enemy_best_value == 21 and len(enemy_hand) == 2):
        enemy_blackJack = True
    vic = 0
    draw = 0
    loose = 0
    if (enemy_blackJack == True): ##Si la banque a un BJ, de toute façon elle gagne les deux mains
        return(-2*bet)
    if (win_sym(player_hand_1,enemy_hand,bet) == bet):
        vic += 1
    if (win_sym(player_hand_2, enemy_hand,bet) == bet):
        vic += 1
    if (win_sym(player_hand_1,enemy_hand,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_2,enemy_hand,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_1,enemy_hand,bet) == 0):
        draw += 1
    if (win_sym(player_hand_2,enemy_hand,bet) == 0):
        draw += 1
    return (vic-loose)
        

##Cas ou les deux split
def win_sym_split_split(player_hand_1,player_hand_2,enemy_hand_1, enemy_hand_2, bet):
    player_best_value_1 = player_hand_1.valeur
    player_best_value_2 = player_hand_2.valeur
    enemy_best_value_1 = enemy_hand_1.valeur
    enemy_best_value_2 = enemy_hand_2.valeur
    vic = 0
    draw = 0
    loose = 0
    #On compare a la main 1 de l'adversaire
    if (win_sym(player_hand_1,enemy_hand_1,bet) == bet):
        vic += 1
    if (win_sym(player_hand_2, enemy_hand_1,bet) == bet):
        vic += 1
    if (win_sym(player_hand_1,enemy_hand_1,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_2,enemy_hand_1,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_1,enemy_hand_1,bet) == 0):
        draw += 1
    if (win_sym(player_hand_2,enemy_hand_1,bet) == 0):
        draw += 1
    #On compare a la main 2 de l'adversaire 
    if (win_sym(player_hand_1,enemy_hand_2,bet) == bet):
        vic += 1
    if (win_sym(player_hand_2, enemy_hand_2,bet) == bet):
        vic += 1
    if (win_sym(player_hand_1,enemy_hand_2,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_2,enemy_hand_2,bet) == - bet):
        loose += 1
    if (win_sym(player_hand_1,enemy_hand_2,bet) == 0):
        draw += 1
    if (win_sym(player_hand_2,enemy_hand_2,bet) == 0):
        draw += 1
    return (vic-loose)
    

###Fin des fonctions win






###Fonction manche, cad jeu de l'IA
def manche_sym(card1,card2,learning=True): #bet est la mise
    global epsilon
    if not learning:
        epsilon_copy = epsilon
        epsilon = 0
    
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
    enemy_state = card2.get_valeur()
    
    player_hand = Main([card1])
    
    ##Tirage de la carte du joueur
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
        
    counter = deck.get_counter()
    player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble, counter],(enemy_state-1) % 10)   #decision du joueur
    player_statesActions.append([player_state,player_decision, counter])
    
    
    
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
            
            counter = deck.get_counter()
                
            #Decision du joueur
            player_decision = makeDecision3([player_state,bool_as_choice,bool_can_split,bool_can_doble, counter],(enemy_state-1) % 10)
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
            player_statesActions.append([player_state,0, counter])
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

    
    
    
    
    
    ########MAJ de my policy#################
    if learning :
#        print("Main du joueur : ", player_hand)
        update_value3(player_statesActions,bool_as_choice,bool_pair,enemy_hand.get_card_at(0)-1,result,position_as) #banque state --> premiere carte
        victoire=update_stats_gains(player_statesActions,result,enemy_state,player_state)
    ########Fin de la MAJ de mypolicy########
    

    else:
        epsilon = epsilon_copy
    
    return (player_hand, bool_dobled, bool_splitted)


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

        
        
        
def update_stats_gains(statesActions,result,enemy_state,player_state):
    global nb_parties_gagnees, nb_parties_jouees, mise_gagnee, mise_investie
    
    mise_investie+=1
    nb_parties_jouees+=1
    mise_gagnee+=result
    if (result > 0):
        nb_parties_gagnees+=1
    
    pourcentage_victoire = str((nb_parties_gagnees/nb_parties_jouees)*100) + "% de victoires"
    gain = "Gain par partie : " + str(mise_gagnee/mise_investie) + " millions d'euros"
    
    return pourcentage_victoire, gain
