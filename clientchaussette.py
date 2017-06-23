import socket
from cartes import *

class Client():

	def __init__(self, givenport, givenip):
	self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.host = givenip
	self.port = givenport

	def connect_chaussette(self):
		s.connect((host,port))

	def disconnect_chaussette(self):
		s.close()

	def get_data(instr):
		connect_chaussette()
		s.send(instr.encode()) 
	    disconnect_chaussette()
	    return s.recv(1024).decode().split(';')

	def has_drawn(self):   #returns a list containing a boolean True=we have drawn then the card drawn if we have drawn 
		data = get_data('draw')
	    if data[0]=='True':
			return [True,Carte(int(data[1]),int(data[2]))]
		else: return [False]

	def opponent_card(self):  #returns the visible card of the opponent's hand
		connect_chaussette()
		s.send('op_card'.encode()) 
		data = ''
		data = s.recv(1024).decode().split(';')
		disconnect_chaussette()
		return Carte(int(data[0]),int(data[1]))

	def send_decision(self,bool_draw,mise,bool_split):
		connect_chaussette()
		s.send('decision'.encode())
		s.send(str(bool_draw).encode())
		s.send(str(mise).encode())
		s.send(str(bool_split).encode())
		disconnect_chaussette()

	def end_turn_state(self):                       #renvoie [True, carte1_adversaire, carte2_adversaire...] si la partie est finie, [False] sinon
		connect_chaussette()
		s.send('state'.encode())
		data = ''
		data = s.recv(1024).decode().split(';')
		disconnect_chaussette()
		if data[0]=='True':
			l=[True]
			for i in range(len(data)):
				if i%2==1:
					l.append(Carte(int(data[i]),int(data[i+1])))
			return l
		else : return[False]