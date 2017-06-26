# -*- coding: utf-8 -*-
import socket
from cartes import *

class Client():

        def __init__(self, givenport, givenip):
                self.host = givenip
                self.port = givenport

        def connect_chaussette(self):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host,self.port))

        def disconnect_chaussette(self):
                self.s.close()

        def get_data(self,instr):
                self.connect_chaussette()
                self.s.send(instr.encode())
                st=self.s.recv(1024).decode()
                self.disconnect_chaussette()
                return st.split(';')

        def has_drawn(self):   #returns a list containing a boolean True=we have drawn then the card drawn if we have drawn 
                data = self.get_data('draw')
                if data[0]=='True':
                        return [True,Carte(int(data[1]),int(data[2]))]
                else: return [False]

        def opponent_card(self):  #returns the visible card of the opponent's hand
                data = self.get_data('op_card')
                return Carte(int(data[0]),int(data[1]))

        def send_decision(self,bool_draw,mise,bool_split):
                connect_chaussette()
                s.send('decision'.encode())
                s.send(str(bool_draw).encode())
                s.send(str(mise).encode())
                s.send(str(bool_split).encode())
                disconnect_chaussette()

        def end_turn_state(self):                       #renvoie [True, carte1_adversaire, carte2_adversaire...] si la partie est finie, [False] sinon
                data = self.get_data('state')
                if data[0]=='True':
                        l=[True]
                        for i in range(len(data)):
                                if i%2==1:
                                        l.append(Carte(int(data[i]),int(data[i+1])))
                        return l
                else : return[False]

c = Client(5000,"137.194.57.193")
print(c.has_drawn())
