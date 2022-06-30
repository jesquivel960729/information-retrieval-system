# Sistema de Recuperación de Información

## Autores

| **Nombre(s) y Apellidos**    |            **Correo**            | **Grupo** |
| :-----------------------:    | :------------------------------: | :-------: |
|  Juan Carlos Esquivel Lamis  |    jesquivel960729@gmail.com     |   C-511   |
|  Juan Carlos Vázquez García  |    vazquezjc097@gmail.com        |   C-512   |
|  Yandy Sánchez Orosa         |    skullcandy961205@gmail.com    |   C-511   |

## Descripción

El Proyecto de Sistemas de Recuperación de Información consiste en el diseño,
implementación, evaluación y análisis de un Sistema de Recuperación de Información.
El sistema desarrollado comprende todas las etapas del proceso de recuperación de
información. Es decir, desde el procesamiento de la consulta hecha por un usuario, la representación de los documentos y la consulta, el funcionamiento del motor de búsqueda y la obtención de los resultados. Para la realización del proyecto se tomaron dos colecciones de datos
Cranfield y Cisi. Y se procesaron ambas como se describe en la metodología. Y se implementaron dos modelos para la recuperación de información, el modelo booleano y el modelo vectorial. 

## Methodology

1. Preprocesamiento de el texto en lenguaje natural del corpus
   - Se removieron todos los caracteres especiales
   - Se removieron los dígitos
   - Tokenize
   - Lowercasing
   - Stemming using `SnowballStemmer`


### Modelo Booleano

#### Consultas

##### Consultas Soportadas

- Término simple => `p`
- AND => `p & q`
- OR => `p | q & r`
- Paréntesis => `( p | q ) & r`
- NOT => `( ~p | q ) & r`

> Prioridad: NOT (~) > AND (&) > OR (|)

##### Consultas no soportadas

- Operador NOT a resultados intermedios para este caso primero es necesario aplicar leyes de Morgan => `~( p | q ) & r` se convertiría en `~p & ~q & r` 
- Espacios entre el operador NOT y el operando => `~ p`

### Modelo Vectorial

#### Consultas

Para este modelo las queries son introducidas en lenguaje natural y se le realiza el mismo procesamiento que al texto del corpus

## Implementación y Ejecución

### Implementación

El proyecto está implementado completamente en [python 3]((https://es.wikipedia.org/wiki/Python)). Python es un lenguaje de programación interpretado cuya filosofía hace hincapié en la legibilidad de su código. Se trata de un lenguaje de programación multiparadigma, ya que soporta parcialmente la orientación a objetos, programación imperativa y, en menor medida, programación funcional. Es un lenguaje interpretado, dinámico y multiplataforma. Nos apoyamos en varias librerías provistas por dicho lenguaje de programación para una mejor y mayor comprensión en el código. 

Para la instalación de las librerías ejecutamos el siguiente comando:

```bash
pip3 install -r requirements.txt
```

- Para descargar algunas librerias usadas para lemmatization en la terminal ingrese los siguientes comandos

```bash
$ python3
>>> import nltk
>>> nltk.download('stopwords')
>>> nltk.download('punkt')
>>> nltk.download('wordnet')
>>> nltk.download('omw-1.4')
```
### Ejecución

Para ejecutar nuestro proyecto es necesario escribir las siguientes líneas desde una terminal abierta en esta misma dirección:

```bash
streamlit run main.py
```
