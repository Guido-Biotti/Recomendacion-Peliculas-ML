# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

Este es mi primer proyecto individual de Henry.  
En este proyecto tuve que extraer, transformar y limpiar datos de un archivo .csv, generar graficos con informes sobre los datos resultantes y luego genere un modelo de ML que dado un titulo de una pelicula dentro del dataset te devuelve una recomendacion de 5 peliculas similares.

## Funciones Auxiliares

Cree un total de 7 funciones auxiliares que me ayudaron a poder hacer de una forma mas sencilla las transformaciones.

**get_collection_name(row)**  
Toma una fila y me retorna solo el nombre de la coleccion (si hay uno) o None.

**get_genre_names(genres_list)**  
Toma una lista de diccionarios (en este caso de generos) y me devuelve una lista con solamente los nombres de los generos

**get_companies_names(companies_list)**  
Toma una lista y me devuelve una lista con solo los nombres de las companias que producen

**get_country_iso(countries_list)** y **get_language_iso(languages_list)**  
Estas dos funciones hacen algo parecido. Ambas toma una lista y retornan solamente los iso (una abreviacion del pais o lenguaje).

**get_cast_list(row)**  
Toma una fila del df y devuelve una lista con solo los nombres de los actores que participaron de la pelicula.

**get_director_list(row)**  
Estas toma una fila y devuelve una lista con solamente los nombres de los directores de esta ya que el resto de la crew no nos interesaba para este proyecto.

## Transformaciones

Lo primero que hice fue importar pandas y Funciones_aux que son las librerias que voy a usar.  
Despues cargue los archivos csv y los concateno en un solo df para poder trabajar de forma mas sencilla con todos los datos y no tener problemas despues a la hora de transformarlos.  
Y ahora empiezo con las transformaciones pedidas:  
  
**1_** Elimino los NA de las columnas **'revenue'** y **'budget'**  
**2_** Elimino las filas con valores NA en **'release_date'** y lo paso a datetime para que todo tenga el mismo formato. Vuelvo a eliminar los NA en caso de que algo halla quedado en formato erroneo.  
**3_** Creo las columnas **'day_of_week'** y **'month'** para que despues se me haga mas sencillo completar las cosas pedidas.  
**4_** Genero la columan **'release_year'** con el año de salida de las peliculas  
**5_** Elimino las columnas que no son necesarias en el dataframe como: **'video'**, **'imdb_id'**, **'adult'**, **'original_title'**, **'poster_path'** y **'homepage'**  
**6_** Creo la columna **'return'** con el valor de la division entre **'revenue'** y **'budget'** y en caso de no ser posbile lo lleno con **0**  
**7_** Y por ultimo desanido las columnas anidadas usando unas funciones que cree en un archivo auxiliar. Estas me facilitan la transformacion ya que solo me devuelven lo que creo es mas importante de cada una de las columnas anidadas.  

Y para terminar genero un sample del 20% del dataframe total de forma random y lo guardo en un archivo .csv nuevo  

## EDA

Primero importo las librerias pandas, seaborn, matplotlib y wordcloud  
  
Despues hago un chequeo de nulos con el que consigo este grafico  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/210306b1-13e4-4396-93d4-6264253e122f)  
  
No tengo valores duplicados asi que sigo por chequear los valores faltantes obteniendo esto  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/9772c470-13f3-49a3-a2eb-e54a060edbda)  
  
Chequeo la distribucion de los diferentes tipos de datos en los que podemos ver que la mayoria de datos son strings  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/c5ab3e4d-777b-4f1c-b35f-5cd8a221cd82)  
  
Luego hago un analisis estadistico en el que obtengo esto (Dentro del notebook de EDA se pueden ver graficos mas especificos)  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/b8f293f2-92ea-4814-870c-469e0b93301c)  
  
Sigo por hacer un analisis de correlaciones donde podemos ver una alta correlacion entre **'budget'** con **'revenue'** y **'vote_count'**  
Ademas podemos ver una alta correlacion tambien entre las ultimas dos. (En el notebook se puede ver ademas el grafico de analisis multivariado)  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/a6058ee9-2dfa-4cdc-b9ee-4cc6ff4d2211)  
  
Y por ultimo hago un grafico de WordCloud en donde podemos ver que las palabras mas usadas en los titulos de las peliculas del sample que tome son **Love** y **Man** con varias apariciones de **Girl**, **Last**, **Life** y **Day**.  
![image](https://github.com/Guido-Biotti/Proyecto-Individual-1/assets/129626971/2ec0bc16-8205-48f2-b2f7-96b65ab9fb18)  
