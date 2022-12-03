from django import forms

#Tupla con clave-valor para usar abajo en 'sexo':
SEXOS=(
	('MASCULINO','Masculino'),
	('FEMENINO', 'Femenino'),
	('OTRO','Otro'),
)

class CandidateForm(forms.Form):
	nombre_y_apellido= forms.CharField(max_length=30)  
	fecha_de_nacimiento=forms.DateField(widget=forms.TextInput(     
        attrs={'type': 'date'} 
    ), help_text="Formato MM/DD/AAAA")
	sexo=forms.ChoiceField(choices=SEXOS)
	telefono=forms.CharField(max_length=30)
	email=forms.EmailField()
	CV_pdf=forms.FileField()
	#creado_a= forms.DateTimeField(auto_now_add=True)  #Después ver.
	#modificado_a= forms.DateTimeField(auto_now=True)  #Después ver.

class RecruiterForm(forms.Form):
	titulo= forms.CharField(max_length=30)  
	descripcion=forms.CharField(widget=forms.Textarea)
	ubicacion=forms.CharField(max_length=20)
	#creado_a= forms.DateTimeField(auto_now_add=True)  #Después ver.
	#modificado_a= forms.DateTimeField(auto_now=True)  #Después ver.