from os import system



NB_MACHINES = 36

def run(salle, repot_result, script_name, l_arg):
    """
        salle : salle dans laquelle on va faire tourner tout
        ca

        repot_result : chemin du dossier ou les resultats vont etre enregistres

        script_name : le script a lancer
        
        l_args : liste des arguments a donner au script, c'est une liste de argv
            donc une liste de liste


        exemple :
        script = bidon.py
        l_arg = [[1, 2], ["bonjour"], []]
        
        lancera
        python bidon.py 1 2
        python bidon.py bonjour
        python bidon.py

        sur des PC differents

    """

    for n in range(1, NB_MACHINES + 1):

        system("ssh ndeconto@" + salle + "-" + 


    


    



    
