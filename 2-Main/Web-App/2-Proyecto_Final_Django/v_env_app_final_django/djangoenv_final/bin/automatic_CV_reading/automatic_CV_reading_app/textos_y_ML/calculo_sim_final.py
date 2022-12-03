from .vectorizacion_y_medicion_sim import tf_idf_and_cosine_sim, word2vec_and_wmd
from .knn import calculo_knn

def calculo_similitudes(id_candidato, id_job):
	print("Calculando similitud para el candidato "+ str(id_candidato) +" y el puesto "+ str(id_job) +".")
	#Calculamos la similitud y lo agregamos a Similitud_Cand_Puesto.
	tf_idf_cos_sim = tf_idf_and_cosine_sim(id_candidato,id_job)		
	tf_idf_cos_sim_format = ('%.3f'%(tf_idf_cos_sim[0]))
	w2v_wmd = word2vec_and_wmd(id_candidato,id_job)
	print ('TF_IDF_COS_SIM: ' + str(tf_idf_cos_sim_format))
	print ('Word2Vec_WMD: ' + str(w2v_wmd))
	knn_final = calculo_knn(tf_idf_cos_sim_format, w2v_wmd)
	print ('Result KNN: ' + str(knn_final))

	return(tf_idf_cos_sim_format, w2v_wmd, knn_final)