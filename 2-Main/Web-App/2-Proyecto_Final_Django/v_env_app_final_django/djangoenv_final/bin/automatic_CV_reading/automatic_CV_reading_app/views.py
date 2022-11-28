from django.shortcuts import render
from .forms import CandidateForm, RecruiterForm  #Importamos los 2 formularios (clases) que tenemos en forms.py de automatic_CV_reading_app.
# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse #Importamos el objeto / clase HttpResponse que usamos abajo.
from .models import Candidato, Puesto, Similitud_Cand_Puesto #Importamos Candidato y Puesto de models.py

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

#Acá creamos nuestras vistas / controladores:
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from .textos_y_ML.preprocesamiento_pdf_y_job_desc import preprocesamiento_pdf, preprocesamiento_job_desc
from .textos_y_ML.vectorizacion_y_medicion_sim import tf_idf_and_cosine_sim, word2vec_and_wmd
from .textos_y_ML.knn import calculo_knn

##################################################################################################################################################

def inicio(request): #Página Inicial.
	titulo = "Bienvenido/a %s" %(request.user)

	#Esto es lo que enviamos al html:
	context = {
		"el_titulo":titulo,
	}

	return render(request,"inicio.html",context) #Acá le enviamos el diccionario 'context' a nuestro 'inicio.html'.

##################################################################################################################################################

@login_required
def form_candidate(request): 
	form=CandidateForm(request.POST or None, request.FILES or None)        #nuestro formulario hecho en forms.py.
	#Para imprimir los permisos:
	#permissions = Permission.objects.filter(user=request.user)
	#print(permissions)

	#Formulario.
	if form.is_valid():
		form_data = form.cleaned_data #diccionario unicode... lo descomponemos abajo para agarrar e imprimir lo que queremos.
		
		#Test para printear lo que trae por consola:
		print(form_data.get("nombre_y_apellido"))
		print(form_data.get("CV_pdf"))
		print("*********************************")

		#Sino otra forma para printear por consola es iterando:
		for parametro, valor in form_data.items():
			print(parametro, valor)

		#Creamos distintas variables para guardar en nuestro modelo 'Candidato' (que importamos arriba) lo que se ingresa por el formulario (puse "f_" para referenciar a formulario y para no confundir con las variables de más abajo):
		f_nombre_y_apellido = form_data.get("nombre_y_apellido")
		f_fecha_de_nacimiento = form_data.get("fecha_de_nacimiento")
		f_sexo = form_data.get("sexo")
		f_telefono = form_data.get("telefono")
		f_email = form_data.get("email")
		f_CV_pdf = form_data.get("CV_pdf")
		
		#Acá creamos el objeto con las variables de arriba que se guardará nuestro en nuestro modelo:
		obj = Candidato.objects.create(nombre_y_apellido=f_nombre_y_apellido, fecha_de_nacimiento=f_fecha_de_nacimiento, sexo=f_sexo, telefono=f_telefono, email=f_email, CV_pdf=f_CV_pdf, CV_clean_content='-', CV_tokens='-')
		#Cuando se guarda en el modelo es que se carga el PDF en /uploads/CVs. Entonces, una vez guardado, realizamos la función de preprocesamiento:

		(clean_cv, tokens_CV) = preprocesamiento_pdf(f_CV_pdf) 		#Acá realizamos la función para limpiar el PDF reutilizando lo de los jupyter notebooks:

		#Ahora hacemos un update del objeto de nuestro modelo con que tenga el último ID (que es autoincremental) con nuestros 2 campos:
		last_cand_id=Candidato.objects.last().id
		Candidato.objects.filter(id=last_cand_id).update(
    			CV_clean_content=clean_cv,
    			CV_tokens=tokens_CV
		)

		return redirect(listar_cand, permanent=False)   #Una vez que el formulario es valido (o sea se submiteó) acá directamente redirijimos a la función listar_cand de abajo, que carga el htlm que dice en su 'return render...'

	#Esto es lo que enviamos al html:
	context = { 
		"el_form": form,  #{{el_form}} es la variable que cargamos en 'candidatos_agregar.html'
	}

	return render(request,"candidatos_agregar.html",context) #Como vemos, acá le enviamos 'context'

##################################################################################################################################################

@login_required
def form_job(request): 
	form_2=RecruiterForm(request.POST or None, request.FILES or None)        #nuestro formulario hecho en forms.py.
	#Para imprimir los permisos:
	#permissions = Permission.objects.filter(user=request.user)
	#print(permissions)

	#Formulario.
	if form_2.is_valid():
		form_data_2 = form_2.cleaned_data #diccionario unicode... lo descomponemos abajo para agarrar e imprimir lo que queremos.

		f_titulo = form_data_2.get("titulo")
		f_descripcion = form_data_2.get("descripcion")
		f_ubicacion = form_data_2.get("ubicacion")

		obj_2 = Puesto.objects.create(titulo=f_titulo, descripcion=f_descripcion, ubicacion=f_ubicacion)

		#Una vez guardado el modelo usamos el campo 'f_descripcion' para sacar su preprocesamiento 'limpio' y los tokens:
		(clean_job, tokens_job) = preprocesamiento_job_desc(f_descripcion) 	

		#Ahora hacemos un update del objeto de nuestro modelo con que tenga el último ID (que es autoincremental) con nuestros 2 campos:
		last_job_id=Puesto.objects.last().id
		Puesto.objects.filter(id=last_job_id).update(
    			job_clean_content=clean_job,
    			job_tokens=tokens_job
		)

		return redirect(listar_puestos, permanent=False)  #Una vez que el formulario es valido (o sea se submiteó) acá directamente redirijimos a la función listar_puestos de abajo, que carga el htlm que dice en su 'return render...'

	#Esto es lo que enviamos al html:
	context_2 = { 
		"el_form_2": form_2,  #{{el_form_2}} es la variable que cargamos en 'puestos_it_agregar.html'
	}

	return render(request,"puestos_it_agregar.html",context_2) #Como vemos, acá le enviamos 'context'

##################################################################################################################################################

@login_required
def listar_puestos(request):	
	#Esto es por si queremos imprimir los datos de los puestos por pantalla, pero lo hacemos directamente sobre el html.
	#contador_puestos = 0
	#for obj_puesto in (Puesto.objects.all()): #Puesto.objects.all()) me da todos los objetos guardados en la BD mediante este Modelo:		
	#	print(obj_puesto.titulo)  #titulo es un atributo dentro de models.py (todo lo que podemos imprimir está ahi: descripcion, ubicacion, creado_a, modificado_a)
	#	contador_puestos=contador_puestos+1
	#print("Número de Puestos totales: " + str(contador_puestos))
	
	queryset = Puesto.objects.all().order_by("creado_a")  #si pongo "-creado_a" es descendente.
	#Esto es lo que enviamos al html:
	context = {
		"puestos": queryset,   #"puestos" lo uso en el html que renderizo (ver abajo).
	}

	return render(request,"puestos_it_listar.html",context) #Acá le enviamos el diccionario 'context' a nuestro 'puestos_it_listar.html'.

##################################################################################################################################################

@login_required
def listar_cand(request):
	
	queryset = Candidato.objects.all().order_by("creado_a")
	#Esto es lo que enviamos al html:
	context = {
		"candidatos": queryset, 
	}

	return render(request,"candidatos_listar.html",context) 

##################################################################################################################################################

@login_required
def best_matching(request): 
	
	#Me llega el ID del job, y saco todos los ids de los puestos y para todas las combinaciones hago tf_idf_and_cosine_sim(x,y) y word2vec_and_wmd(x,y) y las salidas calculo_knn(salida,salida_3) y esa salida la guardo en la columna correspondiente. 

	#Y por último muestro la tabla final.

	##################
	#VER COMO HACER PARA CARGAR 1 SOLA VEZ LOS MODELOS Y APLICAR LAS MENOS POSIBLES VECES LAS TÉCNICAS.
	##################

	#SI SE AÑADE UN CANDIDATO, ENTONCES TRAEMOS EL QUERYSET CON TODOS LOS JOBS Y LOS AÑADIMOS AL CANDIDATO COMO RELACIÓN EN LA M-M
	#Y SI SE AÑADE UN JOB AL REVES, TRAEMOS EL QUERYSET CON TODOS LOS CANDIDATOS Y LOS AÑADIMOS AL JOB COMO RELACIÓN EN LA M-M
	#El único problema acá creo que es al principio, si añado un candidato y no hay ningún puesto... VER
	#Y en los cálculos de distancias tendría que ver si hay alguna combinación de null y solo esa calcular nuevam,ente... para no recalcular todos los valores de los que ya calculé previamente.

	#ANDA esto de abajo, pero es uno por uno:
	'''
	salida = tf_idf_and_cosine_sim(57,17)
	print('%.3f'%(salida[0]))

	salida_2 = tf_idf_and_cosine_sim(57,18)
	print('%.3f'%(salida_2[0]))

	salida_3 = word2vec_and_wmd(57,17)
	print(salida_3)

	salida_4 = word2vec_and_wmd(57,18)
	print(salida_4)

	salida_final = 
	print(salida_final)
	'''

	#Acá enviariamos la lista con los candidatos y sus calificaciones:
	queryset = Similitud_Cand_Puesto.objects.all().order_by("clasif_knn")
	#Esto es lo que enviamos al html:
	context = {
		"similitudes": queryset,   #"similitudes" lo uso en el html que renderizo (ver abajo).
	}

	return render(request,"busqueda_mejor_cand.html",context) #Acá le enviamos el diccionario 'context' a nuestro 'busqueda_mejor_cand.html'.

