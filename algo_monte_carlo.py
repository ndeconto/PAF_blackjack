### Algorithme de Monte-Carlo ###
from random import *;


actions = {"draw":1, "fold":0};        #Set d'actions disponibles
states = range(12);           #Set de states disponibles {<12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, >21}
enemystate = {0,1,2,3,4,5,6,7,8,9} # 0 = as, 1= deux .... 9 = 10 ou tête
alpha = 0.95;                 #Taux d'évaporation
epsilon = 0.05;               #seuil de valeur minimal
mypolicy = [[[10.0]*len(actions) for i in range(len(states))] for j in range(len(enemystate))];    #valeurs initiales de chaques coups dans chaque situatio 

def ind(state):
    if state<12 : return 0
    elif state>21 : return 11
    else: return state-11

	
def makeDecision(state,enemystate):      #renvoie une décision aléatoire étant donné un état
	coeff = mypolicy[enemystate][ind(state)][:];    #liste des poids des décisions dans l'état donné
	summ = 0;                 #summ est un coefficient de normalisation
	for i in coeff:
		summ += i;
	x = random()*summ;
	decis = 0;
	for i in range (len(coeff)):
		decis += coeff[i];
		if x <= decis : return(i);   #prise de décision aléatoire
	return(len(coeff)-1);
	
def makeDecision2(state,enemystate):
	coeff = mypolicy[enemystate][ind(state)][:];
	x = random();
	if x<epsilon:            #prise de décision non optimal avec proba epsilon
		return(randint(0,len(coeff)-1))
	s = 0
	for i in range(len(coeff)):
		if coeff[i]>coeff[s]: s=i;
	#print(s)
	return(s)

def makeBestDecision(state,enemystate):
	coeff = mypolicy[enemystate][ind(state)][:]
	s = 0
	for i in range(len(coeff)):
		if coeff[i]>coeff[s]: s=i
	return(s)