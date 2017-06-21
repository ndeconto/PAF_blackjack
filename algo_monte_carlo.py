### Algorithme de Monte-Carlo ###
from random import *;

def nb_action_dispo(k):
	if k<2:
		return 3
	return 4

actions = {"split":3,"double":2,"draw":1, "fold":0};        #Set d'actions disponibles
states = range(12);           #Set de states disponibles {<12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, >21}
enemystate = {0,1,2,3,4,5,6,7,8,9} # 0 = as, 1= deux .... 9 = 10 ou tete
alpha = 0.95;                 #Taux d'evaporation
epsilon = 0.05;               #seuil de valeur minimal
mypolicy = [[[[10.0]*nb_action_dispo(k) for i in range(len(states))] for j in range(len(enemystate))] for k in range(3)];    #valeurs initiales de chaques coups dans chaque situatio 


def ind(state):
    if state<12 : return 0
    elif state>21 : return 11
    else: return state-11

def level(gotas, cansplit):
	if gotas: return 1
	if cansplit: return 2
	return 0

def makeDecision2(state,enemystate):       #renvoie la meilleure decision a epsilon pres
	mystate, gotas, cansplit, candouble = state[0],state[1],state[2],state[3]
	if gotas and candouble and not(cansplit) and mystate<21 : mystate = mystate-2
	elif gotas and not(cansplit) : mystate = ind(mystate)
	elif cansplit : mystate = int(mystate/2) - 1
	else : mystate = ind(mystate)
	coeff = mypolicy[level(gotas,cansplit)][enemystate][mystate][:]
	if level(gotas,cansplit)==0 and not candouble : coeff=coeff[0:2]
	x = random();
	if x<epsilon:            #prise de decision non optimale avec proba epsilon
		return(randint(0,len(coeff)-1))
	s = 0
	for i in range(len(coeff)):
		if coeff[i]>coeff[s]: s=i;
	if s==2 and not candouble : s = 1
	return(s)

def makeBestDecision(state,enemystate):
	state, gotas, cansplit, candouble = mystate[0],mystate[1],mystate[2],mystate[3]
	if gotas and gotdouble : return 3
	elif gotas : state = state - 1
	elif cansplit : state = int(state/2) - 1
	else : state = ind(state)
	coeff = mypolicy[level(gotas,gotdouble)][enemystate][ind(state)]
	s = 0
	for i in range(len(coeff)):
		if coeff[i]>coeff[s]: s=i
	if s==2 and not candouble : s = 1
	return(s)

def updateValue(statesActionsList,bool_as,bool_pair,bank_state,result,mypolicy):
	for cpl in statesActionsList:
		#print("cpl ",cpl)
		pi = mypolicy[level(bool_as,bool_pair)][bank_state]
		pi = pi[ind(cpl[0])]
		pi = pi[cpl[1]];          #pi est le poids (toujours positif) de la decision cpl[1] dans l'etat cpl[0]
		pi = (result + alpha*pi);             #mise a jour du poids
		#if pi<epsilon/(1-alpha) : pi = epsilon/(1-alpha);      #on est a epsilon-greedy transition (sans oublier la normalisation)
		mypolicy[level(bool_as,bool_pair)][bank_state][ind(cpl[0])][cpl[1]] = pi	 #mise a jour de policy
