'''
	Tournament.py
	Esta clase representa un torneo

	Antonio García Naranjo <antonio.garcian@estudiante.uam.es>
'''
from atp_requests import get_tournament_results
from Match import *
from Player import *

class Tournament:

	def __init__(self,code,year):

		self.code = code
		self.year = year
		self.matches = []
		self.players_dic = {}
		results = get_tournament_results(code, year)
		for result in results:
			code0 = result[0]
			code1 = result[1]
			player0 = self.players_dic.get(code0)
			if(player0 == None):
				player0 = Player(code0)
				self.players_dic[code0] = player0
			player1 = self.players_dic.get(code1)
			if(player1 == None):
				player1 = Player(code1)
				self.players_dic[code1] = player1
			self.matches.append(Match(player0,player1))

	def __str__(self):
		return "Tournament: " + self.code + " (" + self.year + ")"
