import pandas as pd
import Funciones_aux as fa
from fastapi import FastAPI
from ast import literal_eval 
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

#Una vez importadas las librerias a usar cargo el archivo .csv

ruta_movies_sample = 'data/movies_sample.csv'
movies = pd.read_csv(ruta_movies_sample)

app = FastAPI()

#Creo un diccionario de meses y dias para usar en las funciones
meses = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'setiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
dias = {'lunes':0,'martes':1,'miércoles':2,'jueves':3,'viernes':4,'sábado':5,'domingo':6}

@app.get('/cantidad_filmaciones_mes/')
def cantidad_filmaciones_mes(mes):
    #Paso el nombre del mes a minuscula
    mes = mes.lower()

    #Si se encuentra en el diccionario entonces tomo el numero
    if mes in meses:
        num_mes = meses[mes]
    else: #Si no retorno invalido
        return f'Mes "{mes}" no válido.'
    
    cantidad_films = len(movies[movies['month'] == num_mes]) #Tomo la cantidad de peliculas que se filmaron en ese mes y retorno
    
    return f"{cantidad_films} peliculas fueron estrenadas en el mes de {mes.title()}"

@app.get('/cantidad_filmaciones_dia/')
def cantidad_filmaciones_dia(dia):
    dia = dia.lower() #Tomo el input en minuscula
    if dia in dias:
        num_dia = dias[dia] #Si forma parte del diccionario tomo el numero correspondiente
    else:
        return f'Dia "{dia}" no válido.' #Si no hago el retorno invalido
    
    cantidad_films = len(movies[ movies['day_of_week'] == num_dia]) #Tomo la cantidad de peliculas estrenadas en ese dia y retorno
    
    return f"{cantidad_films} peliculas fueron estrenadas en el dia {dia.title()}."

@app.get('/score_titulo/')
def score_titulo(titulo):
    titulo = titulo.lower() #Tomo el input en minuscula
    if movies['title'].str.lower().str.contains(titulo).any() or movies['original_title'].str.lower().str.contains(titulo).any(): #Si alguna columna de titulos contiene
        # un nombre como el ingresado 
        release_year = movies[movies['title'].str.lower() == titulo]['release_year'].iloc[0] #Tomo de esa pelicula el año de lanzamiento
        popularity = movies[movies['title'].str.lower() == titulo]['popularity'].iloc[0] #Y la popularidad y lo retorno
        return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}" con un score/popularidad de "{popularity}".'
    else:
        return f'La pelicula "{titulo.title()}" no se encuentra en el dataset.' #Si ninguna cumple retorno invalido
    
@app.get('/votos_titulo/')
def votos_titulo(titulo):
    titulo = titulo.lower() #Tomo el input en minuscula
    if movies['title'].str.lower().str.contains(titulo).any() or movies['original_title'].str.lower().str.contains(titulo).any(): #Si alguna columna de titulos contiene
        # un nombre como el ingresado 
        votos = movies[movies['title'].str.lower() == titulo]['vote_count'].iloc[0] #Tomo la cantidad de votos
        release_year = movies[movies['title'].str.lower() == titulo]['release_year'].iloc[0] # y el año de lanzamiento
        if votos > 2000:
            promedio = movies[movies['title'].str.lower() == titulo]['vote_average'].iloc[0] #Si tiene mas de 2000 votos tomo el promedio y retorno
            return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}". La misma cuenta con un total de "{votos.astype(int)}" valoraciones, con un promedio de "{promedio}".'
        else: # Y si no retorno diciendo que no se toma en cuenta el promedio
            return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}". La misma cuenta con un total de "{votos.astype(int)}" valoraciones. Debido a que cuenta con menos de 2000 valoraciones no se toma en cuenta el promedio.'
    else:
        return f'La pelicula "{titulo.title()}" no se encuentra en el dataset.' #Si ninguna cumple retorno invalido
    
@app.get('/get_actor/')
def get_actor(actor):
    actor = actor.lower()
    
    # Filtro las películas donde el actor esta en el elenco pero no es director
    peliculas_con_actor_sin_dirigir = movies[
        movies['cast'].apply(fa.get_cast_list).apply(lambda x: actor in x) &
        ~movies['crew'].apply(fa.get_director_list).apply(lambda x: actor in x)
    ]
    
    sum_films = len(peliculas_con_actor_sin_dirigir) #Tomo la cantidad de peliculas
    sum_return = peliculas_con_actor_sin_dirigir['return'].sum().round(2) #Y la suma de los retornos
    
    avg_return = (sum_return / sum_films).round(2) if sum_films > 0 else 0 #Tomo el promedio de retorno si se puede

    genero = literal_eval(peliculas_con_actor_sin_dirigir['cast'].iloc[0])[0]['gender'] #Y tomo el genero del actor y retorno

    if genero == 1:
        return f'La actriz "{actor.title()}" ha participado en "{sum_films}" peliculas donde no fue directora, con un retorno total de "{sum_return}" y un promedio de "{avg_return}" por pelicula.'
    return f'El actor "{actor.title()}" ha participado en "{sum_films}" peliculas donde no fue director, con un retorno total de "{sum_return}" y un promedio de "{avg_return}" por pelicula.'

@app.get('/get_director/')
def get_director(director):
    director = director.lower()
    sum_return =0
    peliculas_dirigidas = movies[movies['crew'].apply(fa.get_director_list).apply(lambda x: director in x)] #Tomo todas las peliculas que cumplen con el input como director
    lanzamientos = peliculas_dirigidas['release_date'].tolist() #Tomo el año de lanzamiento
    retorno = peliculas_dirigidas['return'].round(2).tolist() # el retorno
    costo = peliculas_dirigidas['budget'].round(0).tolist() # el costo
    ganancia = peliculas_dirigidas['revenue'].round(0).tolist() # y la ganancia y transformo todo a lista para trabajar mas comodo
    sum_return = peliculas_dirigidas['return'].sum().round(2) # Despues sumo los retornos y redondeo en 2 decimales

    genero = literal_eval(peliculas_dirigidas['crew'].iloc[0])[0]['gender'] #Tomo el genero del director

    if genero ==1:
        resultado = (f'La directora "{director.title()}" ha tenido un exito de "{sum_return}".\n') 
    else:
        resultado = (f'El director "{director.title()}" ha tenido un exito de "{sum_return}".\n')
    for i, pelicula in enumerate(peliculas_dirigidas['title']): #Hago un for para poder tomar todas las peliculas en las que dirigio dando un retorno mas completo
        resultado += (f'Dirigio la pelicula "{pelicula}" lanzada en "{lanzamientos[i]}" con un costo de "{costo[i]}", una ganancia de "{ganancia[i]}" y por lo tanto un retorno de "{retorno[i]}"\n')
    return resultado

#Tomo un df menor para hacer la funcion mas eficiente
recomendaciones = movies[['title', 'genres']].copy()

#Creo la matriz TF-IDF con los valores de los generos 
tfidf_vectorizer = TfidfVectorizer()
genres_matrix = tfidf_vectorizer.fit_transform(recomendaciones['genres'])

@app.get('/recomendacion/')
def recomendacion(titulo):
    #Tomo el vector de caracteristicas del titulo dado
    titulo = titulo.lower()
    movie_vector = tfidf_vectorizer.transform([titulo])

    #Calcular la similitud con el resto de peliculas
    similarity_matrix = cosine_similarity(movie_vector, genres_matrix)

    #Agrego similitud al df
    recomendaciones['similarity'] = similarity_matrix.flatten()
    #Y ordeno segun esta
    recomendaciones.sort_values(by='similarity', ascending=False)

    # Recomendar las 5 películas más similares
    recommended_movies = recomendaciones['title'].tolist()[1:6] #Del 1 al 6 ya que el 0 es la pelicula dada
    return f'Si te gusto {titulo.title()} creemos que te podria gustar alguna de las siguientes: {", ".join(f"'{movie}'" for movie in recommended_movies)}'