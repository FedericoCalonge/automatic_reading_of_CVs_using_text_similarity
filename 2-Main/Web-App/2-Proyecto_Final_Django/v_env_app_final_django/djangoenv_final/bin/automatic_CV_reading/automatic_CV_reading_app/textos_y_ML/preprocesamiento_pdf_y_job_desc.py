########################################################################
#1.Importando librerias necesarias.
##########################################################################

from gensim.models import KeyedVectors
import matplotlib.pyplot as  plt
from collections import Counter
import pandas as pd
import numpy as np
import random
import string
import math
from pathlib import Path

#Limpieza de datos:
import regex as re                        #Usado en la función remove_punctuation_and_special_characters.
import nltk
from nltk.stem import WordNetLemmatizer   #Usado para lematización.
nltk.download("stopwords")                #Se descargan por única vez al correr el server.
nltk.download('wordnet')                  #Se descargan por única vez al correr el server.
from nltk.tokenize import word_tokenize   #Usado para tokenizar.
from nltk.corpus import stopwords
stop_words = stopwords.words('english')   #Se descargan por única vez al correr el server.

#PDF a text mediante pdfplumber:
import pdfplumber
import os
import collections
from os import listdir
from os.path import isfile, join

#Obtención de bi-grams:
import gensim
from gensim.models.phrases import Phraser, Phrases
import string

#########################################################################
#2-Funciones necesarias para la Limpieza de datos.
##########################################################################
            
def lower_text(DF,clean_column):
    DF[clean_column] = DF[clean_column].apply(lambda x: x.lower() if isinstance(x,str) else x)

def delete_emails_and_web_pages(DF,clean_column):
    DF[clean_column] = DF[clean_column].apply(lambda x: re.sub('(www|http:|https:)+[^\s]+[\w]',' ', x) if isinstance(x,str) else x)     #Macheamos páginas con www, http o https:
    DF[clean_column] = DF[clean_column].apply(lambda x: re.sub('\S*@\S*\s?',' ', x) if isinstance(x,str) else x)                        #Macheamos e-mails:

def delete_common_words(DF,clean_column):
    #Creamos previamente un txt donde colocamos palabras comunes que NO son necesarias para nuestro análisis y macheo (meses y sus abreviaciones, categorías de un cv -education, work experience, etc.) y eliminamos estas palabras de nuestra columna.
    path_txt =Path('txts_adicionales/common_words.txt') 
    
    with open(path_txt) as f2:
        content = f2.read()

    tokens_common_words = word_tokenize(content)  #tokenizo las common words
    DF[clean_column] = DF[clean_column].apply(lambda x: ' '.join([item for item in x.split() if item not in tokens_common_words]))

def delete_candidate_name(DF,clean_column):
    path_txt =Path('txts_adicionales/candidate_names.txt') 

    with open(path_txt) as f2:
        content = f2.read()
        
    tokens_common_words = word_tokenize(content)
    DF[clean_column] = DF[clean_column].apply(lambda x: ' '.join([item for item in x.split() if item not in tokens_common_words]))

def remove_stop_words(DF,clean_column):
    DF[clean_column] = DF[clean_column].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))

def remove_punctuation_and_special_characters(DF,clean_column):
    DF[clean_column] = DF[clean_column].apply(lambda x: re.sub('[\W+]|(\d+)',' ', x) if isinstance(x,str) else x) #Macheamos cualquier non-word [\W+]  ; y  los números (\d+)
    
def tokenize_and_lemmatization(text_column):
    tokens = word_tokenize(text_column)     #Tokenizamos.
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [wordnet_lemmatizer.lemmatize(tok).lower() for tok in tokens]   #Stem words.
    return list(lemmatized_tokens)

def cleaning_DF(DF,column_to_clean,flag_candidate): #Si es un candidato (flag_candidate=True) entonces eliminamos todas las apariciones del Nombre en el CV.
                                                    #Si es una descripción de un puesto entonces no es necesario.
    clean_column='clean_'+column_to_clean
    DF[clean_column]=DF[column_to_clean]            #Copiamos el contenido de 'column_to_clean' en 'clean_column' para utilizarla en las funciones posteriores.
    lower_text(DF,clean_column)
    delete_emails_and_web_pages(DF,clean_column)
    remove_punctuation_and_special_characters(DF,clean_column)
    remove_stop_words(DF,clean_column)
    delete_common_words(DF,clean_column)
    if(flag_candidate==True):                       #Si es un candidato...
        delete_candidate_name(DF,clean_column)
    
def tokenize_and_lemmatize(DF,column_to_clean):
    clean_column='clean_'+column_to_clean
    tokens_column='tokens_'+column_to_clean
    DF[tokens_column] = DF[clean_column].apply(tokenize_and_lemmatization)  #tokenize_and_lemmatization devuelve tokens.
    DF[clean_column] = DF[tokens_column].apply(' '.join)                    #destokenizamos para obtener nuevamente nuestro texto (luego de aplicar lematización) y colocarlo en DF[clean_column].


#########################################################################
#3-Preprocesamiento de los CVs:
##########################################################################

#########################################################################
#3.1. Funciones para extraer las palabras del CV (PDF a texto mediante pdfplumber):
##########################################################################

def pdfextract(PDF_file):
    single_page_text = ""
    all_text = ""
    pdf = pdfplumber.open(PDF_file)
    for pdf_page in pdf.pages:
        single_page_text = pdf_page.extract_text()
        all_text = all_text + '\n' + single_page_text
    pdf.close()
    #return(all_text)        
    return(all_text.encode('utf-8'))

def extract_text(file):
    text = pdfextract(file).decode('utf-8')
    #text = pdfextract(file)
    return text

#########################################################################
#3.2. Funciones para el preprocesamiento en si:
##########################################################################

def preprocesamiento_pdf(CV_path, nombre_y_apellido):
    
    #Antes que nada añadimos el nombre_y_apellido colocado en el formulario en candidates_names.txt para que se elimine en el posterior procesamiento.
    path_txt_cand_names =Path('txts_adicionales/candidate_names.txt') 
    file_txt = open(path_txt_cand_names, "a")  # append mode (insertamos a lo último)
    file_txt.write(nombre_y_apellido.lower() + "\n")
    file_txt.close()
    
    #Ahora si procedemos con el preprocesamiento del pdf:
    CV_path_without_spaces = str(CV_path).replace(' ', '_')    #Es necesaria esta función porque al guardar el CV luego del formulario me agrega "_" en los espacios en blanco del nombre del PDF.

    file =Path('uploads/CVs/'+CV_path_without_spaces)    #Tengo que enviarle un objeto Path, no un string.
    #print(os.listdir()) #['automatic_CV_reading', 'manage.py', 'templates', 'uploads', 'static', 'automatic_CV_reading_app'] --> SABER: es la ubicación desde donde esta el manage.py.
    #print(CV_path)  #MLEngineer_Jonathon_Price.pdf
    
    df_Candidato=pd.DataFrame(columns = ['Content_CV'])
    dat=extract_text(file)                                        #Acá en file debería estar el PDF. 
    data = [{'Content_CV':dat}]            
    df_Candidato=df_Candidato.append(data, ignore_index=True)     #En nuestro DF solo tenemos 1 candidato.
    
    #print("*************DF Candidato:********************")
    #print (df_Candidato) 
    #print("*********************************")
    
    #####################################################################################################################
    # Limpieza DF
    ######################################################################################################################
    cleaning_DF(df_Candidato,'Content_CV',True)
    tokenize_and_lemmatize(df_Candidato,'Content_CV')
    corpus_token_cvs = df_Candidato['tokens_Content_CV'].tolist() #Armamos una lista con las palabras que transformaremos (si corresponde) a bi-grams.

    #####################################################################################################################
    #Bi grams:  #Lo que hacemos acá es obtener en la columna 'tokens_Content_CV' palabras bigramas como: machine_learning, big_Data deep_learning.
    #Para esto usaremos el modelo Phraser del análisis previo en Jupyters (que contiene los bigrams luego de haber analizado TODOS los Cvs y todas las descripciones de los puestos: bigrams_cvs_model.pkl y bigrams_jobs_model.pkl respectivamente) 
    #y como resultado final actualizaremos la columna ‘'tokens_Content_CV'’ reemplazando las palabras que se detectaron como bigramas. Por ej. si antes habían 2 palabras (“machine”, “learning”) y el modelo detectó que “machine_learning” era un bi-grama, entonces se reemplazan estas 2 palabras por el bi-grama (“machine_learning”). 
    ######################################################################################################################
    #Carga del modelo Phraser del análisis previo en Jupyters (que contiene los bigrams luego de haber analizado TODOS los Cvs):
    bigram = Phrases.load("modelos/bigrams_cvs_model.pkl")
    all_sentences = list(bigram[corpus_token_cvs])          # Aplicamos el Phraser para transformar nuestras oraciones a algo más simple (una lista).
    df_Candidato['tokens_Content_CV'] = all_sentences       # Actualizamos columna 'tokens_Content_CV' de nuestro DF con los bigramas.
    df_Candidato['clean_Content_CV'] = df_Candidato['tokens_Content_CV'].apply(lambda x: ' '.join(map(str, x))) #Convertimos la lista de nuestros bigramas (columna 'tokens_Content_CV') a string y lo colocamos en la columna 'clean_Content_CV'.
    df_Candidato.drop('Content_CV', axis=1, inplace=True)   # Borramos la columna 'Content_CV' que no la necesitamos más.

    #print("**************DF_CLEAN_CANDIDATO******************")    
    clean_cv = df_Candidato['clean_Content_CV'].iloc[0]
    tokens_CV = df_Candidato['tokens_Content_CV'].iloc[0]
    #print(clean_cv)  #hcm technical consultant working oracle tool p...
    #print(tokens_CV)  #[hcm, technical, consultant, working, oracle, ...
    #print("*********************************")

    return(clean_cv, tokens_CV)

#########################################################################
#4-Preprocesamiento de las descripciones de los puestos:
##########################################################################

def preprocesamiento_job_desc(campo_descripcion_job):
    
    df_Job=pd.DataFrame(columns = ['Content_Job'])
    data = [{'Content_Job':campo_descripcion_job}]            
    df_Job=df_Job.append(data, ignore_index=True)     
    
    #####################################################################################################################
    #Limpieza DF
    ######################################################################################################################
    cleaning_DF(df_Job,'Content_Job',False)
    tokenize_and_lemmatize(df_Job,'Content_Job')

    #Acá usamos df_all_Jobs porque los bi-gramas los obtenemos a partir de todo el corpus de Jobs, no solo el que ingresa al sistema:
    corpus_token_jobs = df_Job['tokens_Content_Job'].tolist() #Armamos una lista con las palabras que transformaremos (si corresponde) a bi-grams.

    #####################################################################################################################
    #Bi grams:  #Lo que hacemos acá es obtener en la columna 'tokens_Content_Job' palabras bigramas como: machine_learning, big_Data deep_learning.
    ######################################################################################################################
    #Carga del modelo Phraser del análisis previo en Jupyters (que contiene los bigrams luego de haber analizado TODAS las descripciones de puestos de IT):
    bigram = Phrases.load("modelos/bigrams_jobs_model.pkl")
    all_sentences = list(bigram[corpus_token_jobs])         # Aplicamos el Phraser para transformar nuestras oraciones a algo más simple (una lista):
    df_Job['tokens_Content_Job'] = all_sentences      # Actualizamos columna 'tokens_Content_Job' de nuestro DF con los bigramas.
    df_Job['clean_Content_Job'] = df_Job['tokens_Content_Job'].apply(lambda x: ' '.join(map(str, x))) #Convertimos la lista de nuestros bigramas (columna 'tokens_Content_Job') a string y lo colocamos en la columna 'clean_Content_Job'.
    df_Job.drop('Content_Job', axis=1, inplace=True)        # Borramos la columna 'Content_Job' que no la necesitamos más.

    #print("**************DF_CLEAN_JOB******************")    
    clean_job = df_Job['clean_Content_Job'].iloc[0]
    tokens_job = df_Job['tokens_Content_Job'].iloc[0]
    #print(clean_job)  #hcm technical consultant working oracle tool p...
    #print(tokens_job)  #[hcm, technical, consultant, working, oracle, ...
    #print("*********************************")

    return(clean_job, tokens_job)