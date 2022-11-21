"""automatic_reading_CV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path     #Nuevo
from django.conf.urls import url #Viejo, seguimos usando este igual.

from automatic_reading_CV_app import views as aut_read_cv

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', aut_read_cv.home),  #Aca conectamos una URL (Explicacion abajo de r'^$') con la funcion home que queremos ejecutar, la cual esta en el modulo views, paquete automatic_reading_CV_app. 
]

#Explicacion de r'^$'
#r'' significa que lo que esta adentro de las comillas es una expresion regular. Como la pagina que queremos cargar es la home (la que no tiene nada despues de la barra del dominio). Entonces queremos una expresion regular VACIA, esto lo indicamos con ^=inicio cadena y $=fin cadena. Osea en todopoda mi home es www.todopoda.com.ar/ (sin nada despues de la /)

