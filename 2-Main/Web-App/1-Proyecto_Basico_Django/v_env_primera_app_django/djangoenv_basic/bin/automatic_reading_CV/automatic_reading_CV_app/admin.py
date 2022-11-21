from django.contrib import admin

from automatic_reading_CV_app.models import Candidato  #del paquete automatic_reading_CV_app, modulo models importo la CLASE Candidato

# Register your models here:
#Aca le vamos a decir que registre mi modelo Candidato en el administrador:
admin.site.register(Candidato)