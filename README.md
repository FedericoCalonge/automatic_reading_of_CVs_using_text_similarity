# Lectura automática de CVs usando Text Similarity

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

* Carpeta "2-Main/Jupyter_Notebooks": Aquí se encuentran los análisis iniciales realizados en Jupyter Notebooks junto al entrenamiento de distintos modelos: KNN, Word2vec, bigrams. 

* Carpeta "2-Main/Web-App/": Aquí se encuentra el desarrollo del sistema Web realizada en Django, el cual utiliza los procedimientos y los modelos previamente entrenados en los análisis de Jupyter Notebooks.

### Requirements & How to run it 

**Nota: Todos estos pasos fueron detallados utilizando Ubuntu, pero son similares en Windows y Mac debido a que Python es multiplataforma.**

#### Para el caso de los análisis en Jupyter Notebooks (carpeta "2-Main/Jupyter_Notebooks"):

Se debe descargar anaconda (versión 4.10.1) y python (versión 3.8.8) y activar el entorno virtual **conda** y descargar las librerías necesarias (archivo 'requirements_conda.txt' ubicado en '2-Main/Jupyter_Notebooks') mediante el comando:

	> pip install -r requirements_conda.txt
	
Otra opción es previamente a crear el entorno virtual, correr el comando (ubicado previamente en '2-Main/Jupyter_Notebooks'):

	> conda create --name <conda_env> --file requirements_conda.txt
	
Y utilizar conda_env como nuestro entorno virtual. 

#### Para el caso del sistema web realizado en Django (carpeta "2-Main/Web-App/"):

**Paso 1:** Configuración de MySQL y creación de la BD. 

Como primer paso instalamos MySQL Workbench (GUI de MySQL, que en nuestro caso utilizamos como complemento para visualizar nuestra BD). Esto se puede hacer desde el catálogo de aplicaciones de Ubuntu (la versión utilizada en este proyecto fue la 8.0.29 - Community).

Luego instalamos mysql server en nuestro sistema:

	> sudo apt install mysql-server

Vemos la versión de mysql (en mi caso devolvió 'mysql Ver 8.0.31-0ubuntu0.20.04.1 for Linux on x86_64 ((Ubuntu))'):

	> mysql --version

Chequeamos que esté corriendo:

	> sudo systemctl status mysql

Nos logeamos: 

	> sudo mysql -u root -p

Para poder logearnos por MySQL Workbench:

	> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'COMPLETAR_CONTRASEÑA';

Ahora si creamos la BD:

	> CREATE DATABASE db_candidates_and_jobs;

Y salimos:

	> exit

Luego abrimos Workbench y creamos una nueva conexión ingresando como root y la password indicada anteriormente ('COMPLETAR_CONTRASEÑA') y ya podremos entrar y ver mediante la UI la BD 'db_candidates_and_jobs' creada. En un futuro paso debemos verificar que los candidatos y puestos registrados en la app se inserten en la BD para corroborar el correcto funcionamiento de la misma.

**Paso 2:** Creación del entorno virtual e instalación de requirements.

Instanciamos un entorno virtual de python (al cual llamaremos 'djangoenv_final'). Para esto nos ubicamos primero en la carpeta donde queremos crear nuestro entorno virtual, en nuestro caso fue en:

	> cd automatic_reading_of_CVs_using_text_similarity/2-Main/Web-App/2-Proyecto_Final_Django/v_env_app_final_django
	
Ahora instanciamos nuestro djangoenv_final:
	
	> python3 -m venv djangoenv_final

Lo activamos:

	> source djangoenv_final/bin/activate

Descargamos las librerías necesarias (archivo 'requirements.txt' ubicado en '2-Main/Web-App/2-Proyecto_Final_Django/v_env_app_final_django/djangoenv_final/bin/automatic_CV_reading') -ubicandonos con >cd previamente ahí-:

	>pip install -r requirements.txt

**Paso 3:** Interacción con manage.py para correr la app y realizar migraciones de la BD.

Nos ubicamos en la carpeta donde está el archivo manage.py: 

	> cd djangoenv_final/bin/automatic_CV_reading

Creamos un super-usuario administrador (en caso que no lo hayamos creado previamente): 

	> python manage.py createsuperuser

Y ejecutamos los siguientes comandos (los cuales verifican si hay cambios en la BD -si colocamos algo nuevo en 'models.py'-, y actualizan la BD si esto sucedió):

	> python manage.py makemigrations 
	> python manage.py migrate

Corremos el server:

	> python manage.py runserver

Ahora podremos acceder por primera vez mediante nuestro navegador favorito a **localhost:8000/admin** logeandonos con el super-usuario administrador de Django previamente creado. 

Una vez dentro de **localhost:8000/admin** se debe crear un usuario (el cual será nuestro reclutador) yendo a 'Users --> + Add' para que acceda al sistema web mediante **localhost:8000/login**. Al logearse correctamente en **localhost:8000/login** el mismo será redirijido a **localhost/home**, donde podrá navegar por el sistema cargando candidatos, puestos y obteniendo los mejores candidatos para dichos puestos de acuerdo a las mediciones de similitud.

>NOTA 1:
En caso que en el Paso 1 o 2 tire en algún momento algún error de MySQL una posible solución es ejecutar los comandos (fuera del entorno virtual): 

	> sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
	> sudo apt install libmysqlclient-dev

>NOTA 2:
Comandos para resetear los ids de las tablas en caso que sea necesario (mediante MySQL Workbench):

	> ALTER TABLE `db_candidates_and_jobs`.`automatic_CV_reading_app_candidato` AUTO_INCREMENT=0
	> ALTER TABLE `db_candidates_and_jobs`.`automatic_CV_reading_app_puesto` AUTO_INCREMENT=0
	> ALTER TABLE `db_candidates_and_jobs`.`automatic_CV_reading_app_similitud_cand_puesto` AUTO_INCREMENT=0

### Entry points

Los accesos al sistema web son mediante:
* **localhost:8000/admin** (para acceder al administrador del sitio en Django).
* **localhost:8000/login** (para acceder al sistema web; previamente se debe haber creado un usuario con el cual acceder en **localhost:8000/admin**). 
		
### Final results & improvements

Ver secciones ' ' (resultados de los análisis realizados en Jupyter Notebooks), ' ' (resultados de casos de uso en el sistema web) y 'Conclusiones' (conclusiones finales del proyecto de tesis) del informe de tesis (Ubicado en ....). 
