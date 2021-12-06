from atp_requests import *
from Player import *
from Tournament import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle

all_codes = ["miami/403","madrid/1536","indian-wells/404","monte-carlo/410","rome/416","toronto/421","cincinnati/422","shanghai/5014","paris/352"]
codes = [all_codes[8]]
training_data_year = "2018"
test_data_year = "2019"

def main():

	#Consideramos un clasficador vecinos pŕoximos
	clf = KNeighborsClassifier(n_neighbors=25)

	#Obtenemos los datos de entrenamiento 
	X_train,y_train = read_training_data()

	#Entrenamos el clasificador con los datos de entrenamiento
	X_train = StandardScaler().fit_transform(X_train)
	clf.fit(X_train, y_train)

	#Obtenemos los datos de test
	X_test,y_test = read_test_data()
	X_test = StandardScaler().fit_transform(X_test)

	#Puntuación total del rendimiento del clasificador
	score = clf.score(X_test, y_test)
	print(score)

	#Puntuación del clasificador quitando los partidos para los que se estima victoria/derrota con probabilidades entre 0.4 y 0.6
	X = []
	y = []
	probabilities = clf.predict_proba(X_test)
	for i in range(len(probabilities)):
		if(probabilities[i][0] < 0.4 or probabilities[i][0] > 0.6):
			X.append(X_test[i])
			y.append(y_test[i])
	score = clf.score(X, y)
	print(score)


def read_training_data():
	return read_data(training_data_year)

def read_test_data():
	return read_data(test_data_year)

def read_data(year):
	#Cada elemento de X es un vector de datos de un partido player0 Vs player1
	X = []

	#Cada elemento de y es un valor (0 o 1) que indica si player0 gano
	y = []

	for code in codes:
		tournament = load(code,year)
		for match in tournament.matches:
			stats0 = match.player0.stats
			stats1 = match.player1.stats

			#Añadimos la informacion del partido player0 Vs player1
			data_vector = []
			for i in range(len(stats0)):
				data_vector.append(stats0[i] - stats1[i])
			X.append(data_vector)
			y.append(1)

			#Añadimos la informacion del partido player1 Vs player0
			data_vector = []
			for i in range(len(stats0)):
				data_vector.append(stats1[i] - stats0[i])
			X.append(data_vector)
			y.append(0)
	return X,y
			

def get_training_data():
	get_data(training_data_year)

def get_test_data():
	get_data(test_data_year)

def get_data(year):
	for code in codes:
		save(code,year)
		t = load(code,year)
		print(t)

def save(code,year):
	tournament = Tournament(code,year)
	file_name = code + ".pkl"
	file_name = file_name.replace("/","_")
	with open("data/" + year + "/" + file_name, 'wb') as f:
		pickle.dump(tournament, f, pickle.HIGHEST_PROTOCOL)

def load(code,year):
	file_name = code + ".pkl"
	file_name = file_name.replace("/","_")
	with open("data/" + year + "/" + file_name, 'rb') as f:
		tournament = pickle.load(f)
	return tournament

if __name__ == "__main__":
	main()
