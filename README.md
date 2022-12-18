# Lectura automática de CVs usando Text Similarity (en desarrollo)

>Proyecto de Tesis, Universidad Nacional de Avellaneda.
>
>Carrera: Ingeniería en Informática.
>
>Autor: Federico Calonge.

### About

Sistema de lectura automática de Curriculum Vitae accesible vía Web. La finalidad del mismo es ayudar al reclutador laboral a elegir a los mejores candidatos para los puestos laborales de IT que tenga disponible. Esta elección se realiza mediante el uso de algoritmos de machine learning y basándose, principalmente, en una medición de similitud entre textos: **Curriculum Vitae de los candidatos** por un lado, y **descripciones de los puestos laborales de IT** por el otro. 

Las técnicas que se utilizarán basadas en **text similariy** serán: 
* Cosine Similarity.
* Word Mover's Distance (WMD).

Previamente se debe utilizar algún **algoritmo de vectorización** que permita representar las palabras de nuestros textos a un espacio vectorial de forma que Cosine Similarity y WMD puedan interpretarlos de la mejor manera. De esta manera, como algoritmos de vectorización se utilizarán:
* TF-IDF.
* Word Embeddings.

Además, se utiliza un modelo entrenado de KNN el cual toma como entradas los valores de dichas mediciones de similitud.

### Structure 

El proyecto consiste en 2 partes: 

* Carpeta "2-Main...": Aquí se encuentran los análisis en Jupyter Notebooks. 

* Carpeta "2-Main/Web-App/": Aquí se encuentra el desarrollo del sistema Web realizada en Django.

### Requirements & How to run it 

* Para el caso de los análisis en Jupyter Notebooks (carpeta "...."):

Se debe descargar anaconda (versión ....), activar el entorno virtual **conda** y descargar las librerías necesarias (archivo 'requirements_conda.txt' ubicado en el root del proyecto).

* Para el caso del sistema web realizado en Django (carpeta "2-Main/Web-App/"):

Como primer paso se debe crear la BD: ........

Luego se debe instanciar un entorno virtual de python y descargar las librerías necesarias (archivo 'requirements.txt' ubicado en 2-Main/Web-App/2-Proyecto_Final_Django/v_env_app_final_django/djangoenv_final/bin/automatic_CV_reading).

Por último, se debe acceder por primera vez a **localhost/admin** mediante un usuario administrador de Django. Para crear este usuario se debe: ..........

Una vez dentro de /admin se debe crear un usuario (el cual será nuestro reclutador) para que acceda al sistema web mediante **localhost/login**. Al logearse correctamente en /login será redirijido a **localhost/home**, donde podrá navegar por el sistema cargando candidatos, puestos y obteniendo los mejores candidatos para dichos puestos de acuerdo a las mediciones de similitud.

### Entry points

Los accesos al sistema web son mediante:
* localhost/admin (para acceder al administrador del sitio en Django).
* localhost/login (para acceder al sistema web; previamente se debe haber creado un usuario con el cual acceder en localhost/admin). 
		
### Final results & improvements

Ver secciones ' ' (resultados de los análisis realizados en Jupyter Notebooks), ' ' (resultados de casos de uso en el sistema web) y 'Conclusiones' (conclusiones finales del proyecto de tesis) del informe de tesis (Ubicado en ....). 
