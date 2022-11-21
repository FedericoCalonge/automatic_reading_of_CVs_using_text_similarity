"""
Django settings for automatic_reading_CV project.
Generated by 'django-admin startproject' using Django 3.1.13.
For more information on this file, see https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#Acá definimos una variable que va a ser el directorio base:
BASE_DIR = Path(__file__).resolve().parent.parent  

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#Clave secreta que usa Django por defecto para hacer las encriptaciones de las contraseñas de los usuarios. Si lo llevamos a un servidor de producción tenemos que cambiar esto:
SECRET_KEY = 'vi@xa$aljl$javwi^boh%#zg+*65u3(((7mgq5$@dx9-e8!080'   

# SECURITY WARNING: don't run with debug turned on in production!
#Crea una variable DEBUG que si está en TRUE estamos en modo de desarrollo. Si lo llevamos a un servidor de producción tendría que estar en FALSE:
DEBUG = True  

#En modo desarrollo tenemos que poner las direcciones ip en las que el servidor recibe peticiones. Si ponemos 0.0.0.0 recibe de cualquiera:
ALLOWED_HOSTS = [] 

# Application definition

#INSTALLED_APPS es una TUPLA (son como las listas pero inmutables) que contiene las aplicaciones que forman mi proyecto. Los proyectos de Django se organizan en aplicaciones. Cuando instalemos nuevas aplicaciones las tenemos que agregar acá.

INSTALLED_APPS = [
    'django.contrib.admin',         #el administrador de Django.
    'django.contrib.auth',          #autorizaciones, permisos.
    'django.contrib.contenttypes',  #para poder hacer relaciones dinámicas con modelos.
    'django.contrib.sessions',      #sesiones de usuario.
    'django.contrib.messages',      #para poder pasar mensajes de una URL a otra.
    'django.contrib.staticfiles',   #para poner archivos static (imágenes, archivos javascript, css, etc.).
    'automatic_reading_CV_app',
]

#MIDDLEWARE permite crear una capa entre Django y nuestra aplicación para meter cosas ahí.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#Me dice dónde está la configuración de URLs. Me dice que está en el paquete automatic_reading_CV (la carpeta), módulo urls:
ROOT_URLCONF = 'automatic_reading_CV.urls'  

#Templates/plantillas de Django. Template: conjunto de archivos que determinan la estructura y el aspecto visual de un sitio web, y tiene como ventaja principal disminuir tiempos y costos de desarrollo:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#Nos indica donde está la aplicación wsgi:
WSGI_APPLICATION = 'automatic_reading_CV.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
#DICCIONARIO donde vamos a poder poner nuestra configuración de BD. Por defecto utiliza una BD con motor sqlite3. NAME es el nombre de la BD que está en el directorio base (BASE_DIR). Si queremos usar otro motor (mysql) solo cambiamos el motor por este (en ENGINE) y en NAME pondríamos los datos de conexión a la BD. Además, podemos definir más de 1 BD:

'''Original:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us' #idioma inglés- americano por defecto. Podemos cambiarlo a español (es-es).
TIME_ZONE = 'UTC'
USE_I18N = True  	#si queremos usar internacionalización.
USE_L10N = True 	#si queremos usar localización.
USE_TZ = True 	#si queremos usar lo de time zone.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
#Django nos define una ruta de archivos estáticos (imágenes, js, css). Por ej. cuando trabajamos con servidores que reciben mucho tráfico, lo que se hace es separar en varios servidores (uno que sirva solo archivos estáticos y otro que procese las peticiones dinámicas). Si estamos en un servidor de producción, envés de tener ‘/static/’ tendríamos ‘http://cdn.com/styles.css’ (algo así) --> cdn= content delivery network.
STATIC_URL = '/static/'  
