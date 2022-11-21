from django.contrib import admin

from automatic_CV_reading_app.models import Candidato, Puesto  #del paquete automatic_CV_reading_app, modulo models importo la CLASE Candidato

class AdminCandidatos(admin.ModelAdmin):
	list_display=["__str__","nombre_y_apellido","CV_pdf","creado_a","modificado_a"]
	class Meta:
		model=Candidato

	list_filter=["creado_a","modificado_a"]
	search_fields=["nombre_y_apellido"]

# Register your models here:
#Aca le vamos a decir que registre mi modelo Candidato en el administrador:
admin.site.register(Candidato, AdminCandidatos)

class AdminPuestos(admin.ModelAdmin):
	list_display=["titulo","descripcion","ubicacion","creado_a","modificado_a"]
	class Meta:
		model=Puesto

	list_filter=["creado_a","modificado_a"]
	search_fields=["titulo"]

admin.site.register(Puesto, AdminPuestos)