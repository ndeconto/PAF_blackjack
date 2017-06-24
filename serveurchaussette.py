# -*- coding: utf-8 -*-
import socket
from threading import *

class Serveur(Thread):
    def __init__(self, myport, myaddress):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = myaddress
        self.port = myport
        self.sock.bind((self.host, self.port))

        self.server_up = True
        self.client_mise = 0
        self.client_has_split = False
        self.client_has_drawn = False
        self.client_wants_to_draw = False
        self.client_card_drawn = ''
        self.opponent_showing_card=''
        self.fin_manche = False
        self.main = 'True'
        self.start()

    def run(self):
        self.sock.listen(5)
        while self.server_up:
            (clientsock, address) = self.sock.accept()
            instr = clientsock.recv(1024).decode()
            if instr == 'draw':
                if self.client_has_drawn : 
                    clientsock.send(('True;'+client_card_drawn).encode())
                    self.client_has_drawn = False
                else : clientsock.send('False'.encode())
            elif instr == 'op_card' :
                clientsock.send(opponent_showing_card.encode())
            elif instr == 'decision' :
                client_wants_to_draw = (clientsock.recv(1024).decode()=='True')
                client_mise = int(clientsock.recv(1024).decode())
                client_has_split = (clientsock.recv(1024).decode()=='True')
            elif instr == 'state':
                if fin_manche : clientsock.send((self.main).encode())
                else : clientsock.send('False'.encode())
            else : print('unknown instruction')
            self.sock.close()

    def client_has_drawn(self,card):
        self.client_card_drawn = str(card.hauteur)+';'+str(card.couleur)
        self.client_has_drawn = True

    def set_opponent_card(self,card):
        self.opponent_showing_card = str(card.hauteur)+';'+str(card.couleur)

    def end_manche(self):
        self.fin_manche = True

    def ajouter_a_main_du_server(card):
        self.main+=';'+str(card.hauteur)+';'+str(card.couleur)

    def close_server(self):
        self.server_up = False

Serveur(5000,"192.168.0.33")
