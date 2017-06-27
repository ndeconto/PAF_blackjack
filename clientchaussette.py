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
                print (instr + " send")
                st=self.s.recv(1024).decode()
                self.disconnect_chaussette()
                return st.split(';')

        def has_drawn(self):   #returns a list containing a boolean True=we have drawn then the card drawn if we have drawn 
                data = self.get_data('draw')
                
                if data[0]=='True':
                        return [True,Carte(int(data[1]),int(data[2]))]
                else :
                        if data[0]!='False':print('Closed socket or unknown instruction')
                        return [False]

        def opponent_card(self):  #returns the visible card of the opponent's hand
                data = self.get_data('op_card')
                if data[0]=='close':
                        print('Closed socket or unknown instruction')
                        return None
                return Carte(int(data[0]),int(data[1]))

        def send_decision(self,bool_draw,mise,bool_split):
                self.connect_chaussette()
                a_envoyer = ('decision' + ";" + str(bool_draw)
                             + ";" + str(mise)
                             + ";" + str(bool_split)
                             ).encode()
                self.s.send(a_envoyer)
                self.disconnect_chaussette()

        def stop_playing(self):
                self.connect_chaussette()
                self.s.send('stop'.encode())
                print ("stop envoye")
                self.disconnect_chaussette()

        def end_turn_state(self):                       #renvoie [True, carte1_adversaire, carte2_adversaire...] si la partie est finie, [False] sinon
                data = self.get_data('state')
                if data[0]=='True':
                        l=[True]
                        for i in range(len(data)):
                                if i%2==1:
                                        l.append(Carte(int(data[i]),int(data[i+1])))
                        return l
                else :
                        if data[0]!='False':print('Closed socket or unknown instruction')
                        return[False]



def piocher_bloquant(client):

        c = client.has_drawn()

        while not c[0]:

             c = client.has_drawn()

        return c[1]


if __name__ == "__main__":
        c = Client(5000,"localhost")
        print(c.has_drawn())
