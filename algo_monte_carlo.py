### Algorithme de Monte-Carlo ###
from random import *;


actions = {"fold":0, "draw":1};        #Set d'actions disponibles --> 1 on tire, 2 on s'arretes
states = range(12);           #Set de states disponibles {<12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, >21}
alpha = 0.95;                 #Taux d'évaporation
epsilon = 0.05;               #seuil de valeur minimal
mypolicy = [[1.0]*len(actions) for i in range(len(states))];    #valeurs initiales de chaques coups dans chaque situatio 


		
def getRealValues():          #renvoie le poids de chaque décision normalisé
	return(policy*(1-alpha));
	
def makeDecision(state):      #renvoie une décision étant donné un état
	if state<12 : ind = 0
	elif state>21 : ind = 11
	else: ind = state-11
	coeff = mypolicy[ind][:];    #liste des poids des décisions dans l'état donné
	summ = 0;                 #summ est un coefficient de normalisation
	for i in coeff:
		summ += i;
	x = random()*summ;
	decis = 0;
	for i in range (len(coeff)):
		decis += coeff[i];
		if x <= decis : return(i);   #prise de décision aléatoire
	return(len(coeff)-1);
	

