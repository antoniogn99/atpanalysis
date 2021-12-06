'''
	atp_requests.py
	Utiliza la librería requests. Proporciona primitivas para hacer peticiones a atptour.com

	Antonio García Naranjo <antonio.garcian@estudiante.uam.es>
'''
import requests
from bs4 import BeautifulSoup

#URL del servidor al que vamos a hacer las peticiones
URL = "https://www.atptour.com/en/"

def percentage_string_to_integer(s):
	"""Recibe un string de la forma "27%" y devuelve el entero 27

	Parameters
	----------
	s: str
		Cadena con un porcentaje

	Returns
	-------
	Entero corresponditente al porcentaje
	"""

	return int(s[:len(s)-1])

def get_player_stats(code):

	"""Recibe el código de un jugador y devuelve una lista con sus estadísticas

	Parameters
	----------
	code: str
		Código del jugador

	Returns
	-------
	Lista con las estadíticas del jugador
	"""

	#Construimos la request
	url = URL + "players/"+ code + "/player-stats"
	args = {"year": "2018", "surfaceType": "all"}

	#Hacemos la request
	response = requests.post(url, json=args)

	#Control de errores
	if(not response.ok):
		print("ERROR")
		return

	#Manejamos los datos de  respuesta y los devolvemos
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.findAll('table', attrs={'class':'mega-table'})
	if(len(tables)==0):
		return [0,0,0,0,0,0,0,0,0,0,0]

	#Estadísticas al servicio
	table = tables[0]
	table_body = table.find('tbody')
	service_record = []
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    service_record.append([ele for ele in cols if ele])
	service_stats = [	percentage_string_to_integer(service_record[2][1]),
		percentage_string_to_integer(service_record[3][1]),
		percentage_string_to_integer(service_record[4][1]),
		percentage_string_to_integer(service_record[6][1]),
		percentage_string_to_integer(service_record[8][1]),
		percentage_string_to_integer(service_record[9][1])]

	#Estadísticas al resto
	table = tables[1]
	table_body = table.find('tbody')
	return_record = []
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    return_record.append([ele for ele in cols if ele])
	return_stats = [	percentage_string_to_integer(return_record[0][1]),
		percentage_string_to_integer(return_record[1][1]),
		percentage_string_to_integer(return_record[3][1]),
		percentage_string_to_integer(return_record[5][1]),
		percentage_string_to_integer(return_record[6][1])]
	return service_stats+return_stats

def extract_player_code(s):
	"""Recibe una dirección de la forma /en/players/roberto-carballes-baena/cf59/overview
	y devuelve el código roberto-carballes-baena/cf59

	Parameters
	----------
	s: str
		Cadena con una dirección

	Returns
	-------
	Código del jugador
	"""
	return s[12:-9]
	
def get_tournament_results(code,year):
	"""Recibe el código de un torneo y devuelve la lista de pares [code0,code1]
	donde code0 es el código del jugador que ganó

	Parameters
	----------
	code: str
		Código del torneo

	Returns
	-------
	Lista de pares [code0,code1] donde code0 es el código del jugador que ganó
	"""

	#Construimos la request
	url = URL + "scores/archive/"+ code + "/" + year + "/results"
	args = {"matchType": "singles"}

	#Hacemos la request
	response = requests.post(url, json=args)

	#Control de errores
	if(not response.ok):
		print("ERROR")
		return

	#Manejamos los datos de  respuesta y los devolvemos
	soup = BeautifulSoup(response.text, 'html.parser')
	div = soup.find('div', attrs={"scores-results-content"})
	tds = div.findAll('td', attrs={"day-table-name"})
	results = []
	for i in range(0,int(len(tds)),2):
		td0=tds[i]
		a0=td0.find('a')
		code0 = extract_player_code(a0['href'])
		td1=tds[i+1]
		a1=td1.find('a')
		code1 = extract_player_code(a1['href'])
		results.append([code0,code1])
	return results
