# -*- coding: utf-8 -*-
import socket
from cartes import *

from time import sleep

from warnings import warn

class Client():

        def __init__(self, givenport, givenip):
                self.host = givenip
                self.port = givenport

                self.get_data_essai = 10

        def connect_chaussette(self):
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self.host,self.port))

        def disconnect_chaussette(self):
                self.s.close()

        def get_data(self,instr):
                try:
                        self.connect_chaussette()
                        self.s.send(instr.encode())
                        print (instr + " send")
                        st=self.s.recv(1024).decode()
                        self.disconnect_chaussette()

                        self.get_data_essai = 10
                        return st.split(';')
                except (Exception) as e:

                        warn(UserWarning("get data n'a pas fonctionne !"))
                        sleep(.2)
                        self.get_data_essai -= 1
                        if self.get_data_essai > 0:
                                return self.get_data(instr)
                        return "0"
                        

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

        def send_split_position(self, split_pos):
                self.connect_chaussette()
                self.s.send(('chg_jeu;' + str(split_pos)).encode())
                print ('chg_jeu;' + str(split_pos) + " envoye")
                self.disconnect_chaussette()

        def human_is_finished(self):
                data = self.get_data('human_finished')
                if data[0] == "True": return True
                return False


        def get_server_mise(self):
                return int(self.get_data('get_server_mise')[0])

        def end_turn_state(self):                       #renvoie [True, carte1_adversaire, carte2_adversaire...] si la partie est finie, [False] sinon
                data = self.get_data('state')
                print "\n===============================\nSTATE : ", data
                if data[0]=='0':        #si pas de split
                        l=[]
                        for i in range(len(data)):
                                if i%2==1:
                                        l.append(Carte(int(data[i]),int(data[i+1])))
                        return (False, l)
                else :
                        n = int(data[0])
                        l1 = [Carte(int(data[i]), int(data[i + 1]))
                              for i in range(1, 2 * n, 2)]
                        l2 = [Carte(int(data[i]), int(data[i + 1]))
                              for i in range(2  * n + 1, len(data) - 1, 2)]
                        return (True, (l1, l2))

        def server_up(self):
                try :
                        self.connect_chaussette()
                        self.disconnect_chaussette()
                        print "la chaussette repond"
                        return(True)
                except Exception :
                        return(False)

def piocher_bloquant(client):

        c = client.has_drawn()

        while not c[0]:

             c = client.has_drawn()

        return c[1]


        


