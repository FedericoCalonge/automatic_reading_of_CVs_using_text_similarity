##########################################################################
#1.Importando librerias necesarias.
##########################################################################

from automatic_CV_reading_app.models import Candidato, Puesto #Importamos Candidato y Puesto de models.py

import pickle

##########################################################################
#3.KNN.
##########################################################################

def calculo_knn(similitud_coseno, similitud_wmd):
	#Cargamos nuestro modelo KNN previamente entrenado:
	knn_model_loaded = pickle.load(open('modelos/Modelo_KNN_esquema_2_Cross_Validation.sav', 'rb'))

	#Realizamos el cálculo para 1 candidato y 1 puesto:
	lista = [[similitud_coseno,similitud_wmd]]
	y_pred=knn_model_loaded.predict(lista)

	return(y_pred)