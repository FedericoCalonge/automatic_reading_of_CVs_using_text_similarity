from django.shortcuts import render
from .forms import CandidateForm, RecruiterForm  #Importamos los 2 formularios (clases) que tenemos en forms.py de automatic_CV_reading_app.
# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse #Importamos el objeto / clase HttpResponse que usamos abajo.
from .models import Candidato, Puesto #Importamos Candidato de models.py

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

#Acá creamos nuestras vistas / controladores:
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

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
		obj = Candidato.objects.create(nombre_y_apellido=f_nombre_y_apellido, fecha_de_nacimiento=f_fecha_de_nacimiento, sexo=f_sexo, telefono=f_telefono, email=f_email, CV_pdf=f_CV_pdf)

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
	titulo = "Bienvenido/a %s" %(request.user)

	#Esto es lo que enviamos al html:
	context = {
		"el_titulo":titulo,
	}

	return render(request,"busqueda_mejor_cand.html",context) #Acá le enviamos el diccionario 'context' a nuestro 'inicio.html'.