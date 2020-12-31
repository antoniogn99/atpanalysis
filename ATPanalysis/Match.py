'''
	Match.py
	Esta clase representa un enfrentamiento entre dos jugadores

	Antonio García Naranjo <antonio.garcian@estudiante.uam.es>
'''
from Player import *
class Match:

	def __init__(self,player0,player1):

		self.player0 = player0
		self.player1 = player1

	def __str__(self):
		return "Match{\n\t" + self.player0.__str__() + "\n\n\tdefeats\n\n\t" + self.player1.__str__() + "\n}\n\n"

	def __repr__(self):
		return str(self)
