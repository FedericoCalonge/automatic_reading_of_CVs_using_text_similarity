from django.contrib import admin
from automatic_CV_reading_app.models import Candidato, Puesto, Similitud_Cand_Puesto  #del paquete automatic_CV_reading_app, modulo models importamos estas 3 clases.

class AdminCandidatos(admin.ModelAdmin):
	list_display=["__str__","email","CV_pdf","creado_a","modificado_a"]
	class Meta:
		model=Candidato

	list_filter=["creado_a","modificado_a"]
	search_fields=["nombre_y_apellido"]

class AdminPuestos(admin.ModelAdmin):
	list_display=["titulo","descripcion","ubicacion","creado_a","modificado_a"]
	class Meta:
		model=Puesto

	list_filter=["creado_a","modificado_a"]
	search_fields=["titulo"]

##################################################################################################

#Aca le vamos a decir que registre a nuestros 3 modelos en el administrador:
admin.site.register(Candidato, AdminCandidatos)
admin.site.register(Puesto, AdminPuestos)
admin.site.register(Similitud_Cand_Puesto)  #Vista por default.