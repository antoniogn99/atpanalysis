'''
	Player.py
	Esta clase representa un jugador

	Antonio García Naranjo <antonio.garcian@estudiante.uam.es>
'''
from atp_requests import get_player_stats
class Player:

	def __init__(self, code):

		self.code = code
		self.stats = get_player_stats(code)

	def __str__(self):
		return "Player{code: " + self.code + ", stats: " + self.stats.__str__()

	def __repr__(self):
		return str(self)
