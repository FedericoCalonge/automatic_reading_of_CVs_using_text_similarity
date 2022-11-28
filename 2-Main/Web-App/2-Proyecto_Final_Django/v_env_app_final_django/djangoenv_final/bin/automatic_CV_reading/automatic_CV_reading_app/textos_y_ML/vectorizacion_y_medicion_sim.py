##########################################################################
#1.Importando librerias necesarias.
##########################################################################

from automatic_CV_reading_app.models import Candidato, Puesto #Importamos Candidato y Puesto de models.py

import pandas as pd
import numpy as np
from pandas import DataFrame

#Calculo de TFIDF y Cosine:
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import paired_cosine_distances as pcd

#Word2vec: 
import gensim
from gensim.models import Word2Vec

#Para medir tiempos de ejecución:
from datetime import datetime

#Para pasar de string a list:
import ast
##########################################################################
#2.TF-IDF & Cosine Similarity.
##########################################################################

def tf_idf_and_cosine_sim(id_cand, id_job_desc):
	start_time_cosine = datetime.now()

	cand_obj = Candidato.objects.filter(id=id_cand)
	tokens_cv = cand_obj.values()[0]['CV_clean_content']  #El '0' es porque QuerySet es un diccionario y agarramos el primer valor (en nuestro caso con el filtro de arriba sioempre agarramos igualmente el primer valor, pero es una nueva validación de python para asegurarse que hay un solo valor)

	job_obj = Puesto.objects.filter(id=id_job_desc)
	tokens_job = job_obj.values()[0]['job_clean_content']  #El '0' es porque QuerySet es un diccionario y agarramos el primer valor (en nuestro caso con el filtro de arriba sioempre agarramos igualmente el primer valor, pero es una nueva validación de python para asegurarse que hay un solo valor)

	#Transformamos string a lista: 
	tokens_cv_list = [tokens_cv]
	#print(type(tokens_cv))
	tokens_job_list = [tokens_job]
	
	##########################################################################
	#Cargamos nuestro vocabulario previamente entrenado con TF-IDF:
	##########################################################################
	tfidf_vectorizer = pickle.load(open("modelos/vectorizer_tfidf.pickle", "rb"))
	#feature_names = tfidf_vectorizer.get_feature_names()

	##########################################################################
	#Cálculo de cosin sim:
	##########################################################################
    #Parametros de pcd:
        #Xarray-like of shape (n_samples, n_features)
        #Yarray-like of shape (n_samples, n_features)
    #Retorna:
        #distancesndarray of shape (n_samples,)

	A = tfidf_vectorizer.transform(tokens_cv_list)
	B = tfidf_vectorizer.transform(tokens_job_list)
	cosine = 1 - pcd(A, B)   #array de tamaño n_samples

	#df_compar_cand_jobs['tfidf_cosine'] = cosine

	end_time_cosine = datetime.now()

	print('Duración cosine: {}'.format(end_time_cosine - start_time_cosine))

	return (cosine)

########################################################################
#3. Word Embedding (Word2vec) & WMD.
##########################################################################

#Función WMD que usaremos:
def WMD(tokens_CV_Candidate,tokens_Job_Desc, model_Word2vec):
    return (model_Word2vec.wv.wmdistance(tokens_CV_Candidate, tokens_Job_Desc))  #'wmdistance' return the word mover distance between two documents. 

def word2vec_and_wmd(id_cand, id_job_desc):
	start_time_wmd = datetime.now()

	cand_obj = Candidato.objects.filter(id=id_cand)
	tokens_cv = cand_obj.values()[0]['CV_tokens']  #El '0' es porque QuerySet es un diccionario y agarramos el primer valor (en nuestro caso con el filtro de arriba sioempre agarramos igualmente el primer valor, pero es una nueva validación de python para asegurarse que hay un solo valor)

	job_obj = Puesto.objects.filter(id=id_job_desc)
	tokens_job = job_obj.values()[0]['job_tokens']  #El '0' es porque QuerySet es un diccionario y agarramos el primer valor (en nuestro caso con el filtro de arriba sioempre agarramos igualmente el primer valor, pero es una nueva validación de python para asegurarse que hay un solo valor)

 	#Pasamos de una representación en string de una lista ( "['hola','como','estas']" ) a una lista ( ['hola','como','estas'] ): 
	#print (type(tokens_cv))
	tokens_cv = ast.literal_eval(tokens_cv)
	#print ("final list", tokens_cv)
	#print (type(tokens_cv))
	tokens_job = ast.literal_eval(tokens_job)

	##########################################################################
	#Cargamos nuestro modelo Word2vec previamente entrenado:
	##########################################################################
	model = gensim.models.Word2Vec.load("modelos/Word2vec_Model")
	#wrds=list(model.wv.vectors)   #El modelo nos da un VOCABULARIO con palabras con las cuales podemos consultar. 
	#print(len(wrds))              #Me devuelve las palabras/tokens totales y ÚNICAS (sin repetidas) de nuestro Corpus (=Nuestro VOCABULARIO).

	##########################################################################
	#Cálculo de WMD llamando a la función de arriba 'WMD' la cual le pasamos el modelo Word2Vec':
	##########################################################################

	wmd_result = round(WMD(tokens_cv,tokens_job,model),3)
	similarity_wdm = round((1/(1+wmd_result)),3)  

	end_time_wmd = datetime.now()

	print('Duración WMD: {}'.format(end_time_wmd - start_time_wmd))

	return (similarity_wdm)