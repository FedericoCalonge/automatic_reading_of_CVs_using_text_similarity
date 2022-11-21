from django.db import models


#Tupla con clave-valor para usar abajo en 'sexo':
SEXOS=(
	('MASCULINO','Masculino'),
	('FEMENINO', 'Femenino'),
	('OTRO','Otro')
)

# Create your models here.
class Candidato(models.Model): #Lo de los () indica que la clase Candidato (que es un modelo) hereda de la clase Model (que esta en django.db.models y que arriba ya se habia importado)
	
	#Campos que va a tener nuestro modelo de Candidato:

	nombre_y_apellido= models.CharField(max_length=30)  
	#nombre_y_apellido es de tipo models.CharField y por parametro le pasamos max_lenght con un valor de 30.
	#CharField() y los demás de abajo (TextField(), etc.) son CONSTRUCTORES de las clases.
	#Mientras que los campos (nombre_y_apellido, CV, etc. son las INSTANCIAS de los objetos/clases)
	
	fecha_de_nacimiento=models.DateField(help_text="Formato AAAA-MM-DD")

	sexo=models.CharField(choices=SEXOS,max_length=10)
	
	telefono=models.CharField(max_length=30)

	email=models.EmailField()

	CV_pdf=models.upload = models.FileField(upload_to='uploads/CVs')  #Curriculum Vitae en formato PDF.
	# file will be uploaded to MEDIA_ROOT/uploads/CVs

	#Para cada entidad que tengo en la BD creamos una fecha de creacion del archivo, y fecha de ultima modificacion --> esto es UTIL por ej. si quiero Candidatos solo que se cargaron desde alguna fecha. Entonces creamos:
	creado_a= models.DateTimeField(auto_now_add=True)
	#Cuando guardemos el objeto, automaticamente Django (gracias al auto_now_add=True) en el campo creado_a guarda el instante de tiempo en que se añadio/creo el objeto (add):
	modificado_a= models.DateTimeField(auto_now=True)
	#En modificado_a se guarda el tiempo en que el objeto es modificado/guardado. 

	def __str__(self):
		return self.nombre_y_apellido