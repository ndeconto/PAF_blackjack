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
        self._stop_event = Event()
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
        self.cartes_du_serveur = [] #cartes de l'humain
        
       
        try :
            self.start()
        except self._stop_event.is_set():
            self._stop()
    
    def closing(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.closing():
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            (clientsock, address) = self.sock.accept()
            instr_totale = clientsock.recv(1024).decode().split(';')
            instr = instr_totale[0]
            print("received : "+instr+" from client")
            print instr_totale

            
            if self.closing():
                clientsock.send("close".encode())
            elif instr == 'draw':
                
                #le client a toujours le droit de piocher !
                #le serveur ne pioche jamais
                c = self.pioche.piocher()
                self.cartes_donnees.append(c)
                self.has_client_drawn(c)
                if self.client_has_drawn : 
                    clientsock.send(('True;'+ self.client_card_drawn).encode())
                    self.client_has_drawn = False
                else : clientsock.send('False'.encode())

                
            elif instr == 'op_card' :
                clientsock.send(self.opponent_showing_card.encode())
            elif instr == 'decision' :
                self.client_wants_to_draw = (instr_totale[1]=='True')
                self.client_mise = int(instr_totale[2])
                self.client_has_split = (instr_totale[3]=='True')
            elif instr == 'state':
                if self.fin_manche : clientsock.send((self.main).encode())
                else : clientsock.send('False'.encode())
            elif instr == 'stop':
                self.fin_manche = True
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
        self._stop_event.set()

if __name__ == "__main__":
    s = Serveur(5000,"localhost", Deck())
    #c=Carte(8,14)
    #s.has_client_drawn(c)
    print( "c'est fini pour le serveur")
