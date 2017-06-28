# -*- coding: utf-8 -*-
import socket
from cartes import *
from threading import *


IP_SERVEUR  = "localhost"
PORT        = 5000


class Serveur(Thread):
    def __init__(self, myport, myaddress, pioche):
        print "serveur init"
        Thread.__init__(self)
        self.running = True
        self.host = myaddress
        self.port = myport

        self.pioche = pioche

        self.server_up = True
        self.client_mise = 0
        self.client_has_split = False
        self.client_has_drawn = False
        self.client_wants_to_draw = False
        self.client_card_drawn = ''
        self.opponent_showing_card=''
        self.fin_manche = False
        self.main = 'True'

        self.cartes_donnees = []    #cartes pour l'ordi
        self.index_buffer_local = 0
        self.index_buffer_distant = 0
        
        self.cartes_du_serveur = [] #cartes de l'humain
        self.pos_split = 0 #info sur le split du joueur cote serveur

        self.human_finish = False

        self.a_un_client = False
        
       
        self.start()
    
    def closing(self):
        return not self.running


    def demander_carte_donne(self):

        #methode appelee en local uniquement

        if self.index_buffer_local < len(self.cartes_donnees):
            c = self.cartes_donnees[self.index_buffer_local]

        else :
            c = self.pioche.piocher()
            self.cartes_donnees.append(c)

        self.index_buffer_local += 1
        return c


    def get_info_reconstruction(self):
        #renvoie les cartes donnees au meme format que end_turn_state de
        #clientchaussette, avec le split en moins
        if self.pos_split == 0:
            return self.cartes_donnees
        a, b = (self.cartes_donnees[:self.pos_split],
                self.cartes_donnees[self.pos_split:])
        b = [a.pop(1)] + b
        return ()
        

    def run(self):
        while self.running:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            (self.clientsock, address) = self.sock.accept()
            instr_totale = self.clientsock.recv(1024).decode().split(';')
            instr = instr_totale[0]
            print("received : "+instr+" from client")
            print instr_totale

            self.a_un_client = True

            
            if self.closing():
                self.clientsock.send("close".encode())

                
            elif instr == 'draw':
                #le client a toujours le droit de piocher !
                #le serveur ne pioche jamais
                if self.index_buffer_distant < len(self.cartes_donnees):
                    c = self.cartes_donnees[self.index_buffer_distant]
                else :
                    c = self.pioche.piocher()
                    self.cartes_donnees.append(c)

                self.index_buffer_distant += 1
                    
                self.has_client_drawn(c)
                if self.client_has_drawn : 
                    self.clientsock.send(('True;'+ self.client_card_drawn).encode())
                    self.client_has_drawn = False
                else : self.clientsock.send('False'.encode())

                
            elif instr == 'op_card' :
                self.clientsock.send(self.opponent_showing_card.encode())
            elif instr == 'decision' :
                self.client_wants_to_draw = (instr_totale[1]=='True')
                self.client_mise = int(instr_totale[2])
                self.client_has_split = (instr_totale[3]=='True')
                
            elif instr == 'state': #quand le client demande le jeu de l'humain
                sp = str(self.pos_split) #info du split
                main = ";".join( str(c.hauteur) + ';' + str(c.couleur)
                              for c in self.cartes_du_serveur[1:])
                self.clientsock.send((sp + ";" + main).encode())

            elif instr == 'chg_jeu':
                #on recoit la position du split
                self.pos_split = int(instr_totale[1])
                
            elif instr == 'stop':
                self.fin_manche = True
            elif instr == "human_finished":
                self.clientsock.send(str(self.human_finish).encode())
            else : print('unknown instruction')
            self.sock.close()
        print('server properly shut down')

    def has_client_drawn(self,card):
        self.client_card_drawn = str(card.hauteur)+';'+str(card.couleur)
        self.client_has_drawn = True

    def set_opponent_card(self,card):
        self.opponent_showing_card = str(card.hauteur)+';'+str(card.couleur)

    def end_manche(self):
        self.fin_manche = True

    def ajouter_a_main_du_server(card):
        self.main+=';'+str(card.hauteur)+';'+str(card.couleur)

    def close_server(self):
        self.running = False
        try:
            #satan
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host,self.port))
            s.close()
            
            self.sock.close()
            self.clientsock.close()
            self._stop()
            print " ========   server closed ====== "
        except Exception as e:
            print e

if __name__ == "__main__":
    s = Serveur(5000,"localhost", Deck())
    #c=Carte(8,14)
    #s.has_client_drawn(c)
    print( "c'est fini pour le serveur")
