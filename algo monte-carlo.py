### Algorithme de Monte-Carlo ###
from random import *;

actions = {"draw":0, "fold":1};        #Set d'actions disponibles
states = range(12);           #Set de states disponibles {<12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, >21}
alpha = 0.95;                 #Taux d'évaporation
epsilon = 0.05;               #seuil de valeur minimal

policy = [[1]*len(actions)]*len(states);    #valeurs initiales de chaques coups dans chaque situation

def updateValue(statesActionsList,result):    #statesActionsList est la liste de couples des (états; actions) prises lors de la partie
	for cpl in statesActionsList:
		pi = policy[cpl[0]][cpl[1]];          #pi est le poids (toujours positif) de la décision cpl[1] dans l'état cpl[0]
		pi = (result + alpha*pi);             #mise à jour du poids
		if pi<epsilon/(1-alpha) : pi = epsilon/(1-alpha);         #on est à epsilon-greedy transition (sans oublier la normalisation)

def getRealValues():          #renvoie le poids de chaque décision normalisé 
	return(policy*(1-alpha));

def makeDecision(state):      #renvoie une décision étant donné un état
	coeff = policy[state];    #liste des poids des décisions dans l'état donné
	summ = 0;                 #summ est un coefficient de normalisation
	for i in coeff:
		summ += i;
	x = random()*summ;
	decis = 0;
	for i in range len(coeff):
		decis += coeff[i];
		if x <= decis : return(i);   #prise de décision aléatoire
	return(len(coeff)-1);
