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
from .textos_y_ML.calculo_sim_final import calculo_similitudes

#Para ocultar warnings de tipo "futuros" (que ahora no afectan pero pueden afectar en versiones de librerias posteriores):
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

##################################################################################################################################################
@login_required
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
		#for parametro, valor in form_data.items():
		#	print(parametro, valor)

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

		(clean_cv, tokens_CV) = preprocesamiento_pdf(f_CV_pdf,f_nombre_y_apellido) 		#Acá realizamos la función para limpiar el PDF reutilizando lo de los jupyter notebooks:

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

#LÓGICA:
#En 'best_matching_select' mostramos un formulario / tabla con los puestos disponibles (html: busqueda_mejor_cand_list_jobs) para calcular la similitud. La idea es seleccionar un número de esta tabla (que sería el ID del job) y pasar este id a 'best_matching_show'. Ahi agarramos a TODOS los ids de los candidatos (lista_ids_todos_candidatos), y, en base a los ids de esta lista, nos fijamos en la tabla de similitudes intermedia: 
	#IF está el id del job y el id del candidato en esta tabla intermedia: es que ya se calculó la similitud y no hay que calcularla nuevamente.
	#ELSE, se calcula la similitud y se agrega el registro correspondiente a ese job y a ese candidato con la similitud calculada. 

#Y por último mostramos la tabla final (html: busqueda_mejor_cand_show)

#¿Qué es "calcular la similitud"? --> Es aplicar tf_idf_and_cosine_sim(x,y), luego word2vec_and_wmd(x,y) y por último esas salidas llevarlas a calculo_knn(salida_1,salida_2). Todas estas salidas se guardan en la BD en 'similitud_cand_puesto'. 

@login_required
def best_matching_select(request): 

	#Enviamos la lista de puestos para seleccionar el que queremos:
	queryset_2 = Puesto.objects.all().order_by("creado_a")  #si pongo "-creado_a" es descendente.

	#Esto es lo que enviamos al html:
	context = { 
		"puestos": queryset_2, #"puestos" lo usamos en el html que renderizo (ver abajo).  
	}
	#print(request.GET.get('internal-id'))
	
	if request.method == 'GET' and str(request.GET.get('internal-id'))!='None':
		id_job = request.GET.get('internal-id')
		return redirect(best_matching_show, id=id_job, permanent=False)  #Le pasamos el id para que lo muestre en la URL (/"best_match/<id>/")
	else: 
		return render(request,"busqueda_mejor_cand_list_jobs.html",context) #Acá le enviamos el diccionario 'context' a nuestro 'busqueda_mejor_cand.html'.

@login_required
def best_matching_show(request, id): #id = id del puesto.
	
	queryset_candidatos = Candidato.objects.all()
	lista_ids_todos_candidatos = queryset_candidatos.values_list('id', flat=True) #Agarramos todos los ids de los candidatos.
	#Sin el flat me lo imprimia como: <QuerySet [(1,), (2,),...']>. En cambio con el flat es una lista: [1, 2, 3, ...]
	#print(len(lista_ids_todos_candidatos))  #imprime cantidad de cantidatos totales.
	#print(type(lista_ids_todos_candidatos)) #<class 'django.db.models.query.QuerySet'>

	queryset_sim = Similitud_Cand_Puesto.objects.filter(puesto_id = id) #Obtengo solo las filas del modelo con nuestro puesto_id = id ingresado.
	lista_ids_cand_del_puesto_ya_calculados = queryset_sim.values_list('candidato_id', flat=True) #Obtengo lista con los ids de los candidatos donde su similitud ya fue calculada para ese puesto.

	#En base a los ids de lista_ids_todos_candidatos veo en la tabla de similitudes intermedia: 
		#IF está el id del job y el id del candidato en esta tabla intermedia: es que ya se calculó la similitud y no hay que calcularla nuevamente.
		#ELSE, se calcula la similitud y se agrega el registro correspondiente a ese job y a ese candidato con la similitud calculada. 
	
	if queryset_sim:  #Me fijo si alguna vez se calculó algo en Similitud_Cand_Puesto, en caso contrario (else abajo) calculo para TODOS.
		#Recorro los candidatos (queryset_candidatos):
		for candidato in queryset_candidatos:
			#Si el candidato aparece en esta lista, es que ya fue calculado para ese puesto y no calculamos nada, solo mostramos un print:
			if (candidato.id) in lista_ids_cand_del_puesto_ya_calculados: 	
				print("La similitud para el candidato "+ str(candidato.id) +" y el puesto "+ str(id) +" ya fue calculada.") 
			#Sino, entonces lo calculamos. 
			else:
				(tf_idf_cos_sim_format, w2v_wmd, knn_final) = calculo_similitudes(candidato.id,id)
				#Agregamos los resultados a nuestro modelo Similitud_Cand_Puesto:
				objeto_sim_cand_puesto = Similitud_Cand_Puesto.objects.create(cos_sim=tf_idf_cos_sim_format, wmd_sim=w2v_wmd, clasif_knn=knn_final, candidato_id=candidato.id, puesto_id=id)
				objeto_sim_cand_puesto.save()

	else: 
		print("Calculando similitud para todos los candidatos.")
		for candidato in queryset_candidatos: 		#Recorro los candidatos (queryset_candidatos)
			(tf_idf_cos_sim_format, w2v_wmd, knn_final) = calculo_similitudes(candidato.id,id)
			#Agregamos los resultados a nuestro modelo Similitud_Cand_Puesto:
			objeto_sim_cand_puesto = Similitud_Cand_Puesto.objects.create(cos_sim=tf_idf_cos_sim_format, wmd_sim=w2v_wmd, clasif_knn=knn_final, candidato_id=candidato.id, puesto_id=id)
			objeto_sim_cand_puesto.save()

	#Acá enviariamos la lista con los candidatos y sus calificaciones:
	queryset_sim_2 = Similitud_Cand_Puesto.objects.filter(puesto_id = id).order_by("-clasif_knn") #- es orden asc.
	queryset_puesto = Puesto.objects.filter(id = id)
	titulo_puesto = queryset_puesto.values()[0]['titulo'] #El '0' es porque QuerySet es un diccionario y agarramos el primer valor (en nuestro caso con el filtro de arriba sioempre agarramos igualmente el primer valor, pero es una nueva validación de python para asegurarse que hay un solo valor)

	#Esto es lo que enviamos al html:
	context = { 
		"similitudes": queryset_sim_2,
		"candidatos":queryset_candidatos, 
		"puesto": titulo_puesto,
	}

	return render(request, "busqueda_mejor_cand_show.html", context)