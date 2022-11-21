from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse #Importamos el objeto / clase HttpResponse que usamos abajo.

#Acá creamos nuestras vistas / controladores:

def home(httprequest): #Página Inicial.
		return HttpResponse("Hola")

