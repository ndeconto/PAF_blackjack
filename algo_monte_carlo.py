### Algorithme de Monte-Carlo ###
from random import *;

actions = {"draw":1, "fold":0};        #Set d'actions disponibles
states = range(12);           #Set de states disponibles {<12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, >21}
enemystate = {1,2,3,4,5,6,7,8,9,10} #1 = as, 2= deux .... 10 = 10 ou tete
alpha = 0.95;                 #Taux d'evaporation
epsilon = 0.05;               #seuil de valeur minimal
mypolicy = [[[10.0]*len(actions) for i in range(len(states))] for j in range(len(enemystate))];    #valeurs initiales de chaques coups dans chaque situatio 


		
def getRealValues():          #renvoie le poids de chaque decision normalise
	return(policy*(1-alpha));
	
def makeDecision(state,enemystate):      #renvoie une decision aleatoire etant donne un etat
	if state<12 : ind = 0
	elif state>21 : ind = 11
	else: ind = state-11
	coeff = mypolicy[enemystate-1][ind][:];    #liste des poids des decisions dans l'etat donne
	summ = 0;                 #summ est un coefficient de normalisation
	for i in coeff:
		summ += i;
	x = random()*summ;
	decis = 0;
	for i in range (len(coeff)):
		decis += coeff[i];
		if x <= decis : return(i);   #prise de decision aleatoire
	return(len(coeff)-1);
	
def makeDecision2(state,enemystate):
	if state<12 : ind = 0
	elif state>21 : ind = 11
	else: ind = state-11
	coeff = mypolicy[enemystate-1][ind][:];
	x = random();
	if x<epsilon:            #prise de decision non optimal avec proba epsilon
		return(randint(0,len(coeff)-1))
	s = 0
	for i in range(len(coeff)):
		if coeff[i]>coeff[s]: s=i;
	#print(s)
	return(s)
