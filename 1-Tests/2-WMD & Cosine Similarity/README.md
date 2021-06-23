# Tests - WMD & Cosine Similarity

### About
Pruebas para la implementación del sistema principal de lectura automática de Curriculum Vitae.

### Requirements and How to run it.

Se debe tener instalado Anaconda (https://docs.anaconda.com/anaconda/install/linux/)
>
>
Estando ubicados en el root del proyecto, creamos nuestro entorno virtual (federicio_env) y lo activamos con:
	
    > conda create --name federicio_env

    > conda activate federicio_env
    
Luego instalamos pip con dicho entorno activado:
    
    > conda install pip
    
Nota: se pueden instalar los paquetes necesarios de 2 maneras:
	
* Forma 1 (mediante pip3):
>
    > 1.1. >pip3 install PACKAGE. 
    
    > 1.2. >/home/USER/anaconda3/envs/federicio_env/bin/pip3 install PAQUETE_QUE_QUIERA(como gensim) --> Esto es para asegurarnos que realmente corramos el pip3 instalado en nuestro entorno virtual.	

* Forma 2 (mediante conda):
>
    > conda install PACKAGE.

Recomendación: instalar los paquetes con CONDA y lo que no se puedan mediante pip3.
>
Entonces, para instalar los paquetes ejecutamos los siguientes comandos:
	
    > conda install jupyter                       -->(para instalar el jupyter notebook). 

    > conda install gensim

    > pip3 install PyPDF2                         -->(no se puede instalar por conda).

    > conda install nltk

    > conda install pandas

    > conda install spacy                         -->(opción 2: >conda install -c conda-forge spacy). 

    > conda install matplotlib

    > python -m spacy download en_core_web_lg
    
    > pip3 install wmd
    
    > pip3 install pyemd                          -->(lo usa wmd).
     
Luego nos fijamos que este todo instalado (con nuestro entorno activado):
    
    > pip3 list
    
    > conda list
  
Y por último corremos jupyter notebook (con nuestro entorno activado) y ejecutamos el archivo 'CV_Scoring_V1.ipynb' en nuestro navegador (http://localhost:8888/tree):

    > jupyter-notebook
    
### Final Results

### Improvements
