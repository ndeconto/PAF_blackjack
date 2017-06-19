
"""
fichier qui contient les fonctions de prise de decision dans une situation
donnee
il y a plusieurs fonctions qui correspondent chacune a une regle de jeu
differente
noter qu'on n'est plus dans la phase d'apprentissage, mais bien dans le cas ou
on utilise ce qu'on a appris

toutes les fonctions ont les memes entrees / sortie
ENTREES :
    main :
        la main que l'on a avant de prendre la decision
        
    carte_adversaire :
        la carte de l'adversaire que l'on voit
        
    l_cartes_passees :
        les cartes qui sont deja passees et qui ne peuvent pas retomber
        ie, c'est l'historique pour compter les cartes

SORTIES :
    la decision a prendre, a savoir l'une des quatre constantes :
    CONTINUER
    ARRETER
    SPLITTER
    DOUBLER
"""


CONTINUER   =   0
ARRETER     =   1
SPLITTER    =   2
DOUBLER     =   0


def decision_banque(main, carte_adversaire, l_cartes_passees):
    """
        fonction de la prise de decision de la banque
        classiquement, cette prise de decision est resumee par la regle :
        "la banque tire a 16, s'arrete a 17"

        mais on peut bien sur essayer des choses plus exotiques...
    """

    if main.get_m_valeur() < 17:
        return CONTINUER

    return ARRETER


def decision_joueur_vs_banque(main, carte_adversaire, l_cartes_passees):
    #TODO a implementer
    return


def decision_un_vs_un(main, carte_adversaire, l_cartes_passees):
    #TODO a implementer
    return
