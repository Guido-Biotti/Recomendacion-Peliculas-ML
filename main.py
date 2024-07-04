import pandas as pd
import Funciones_aux as fa
from fastapi import FastAPI
from ast import literal_eval 

#Una vez importadas las librerias a usar cargo el archivo .csv

ruta_movies_sample = 'data/movies_sample.csv'
movies = pd.read_csv(ruta_movies_sample)

#tamano_muestra = 8000
#movies = movies_full.sample(n=tamano_muestra, random_state=42)

app = FastAPI()

#Creo un diccionario de meses y dias para usar en las funciones
meses = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'setiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
dias = {'lunes':0,'martes':1,'miércoles':2,'jueves':3,'viernes':4,'sábado':5,'domingo':6}


@app.get('/cantidad_filmaciones_mes/')
def cantidad_filmaciones_mes(mes):
    mes = mes.lower()
    if mes in meses:
        num_mes = meses[mes]
    else:
        return f'Mes "{mes}" no válido.'
    
    cantidad_films = len(movies[movies['month'] == num_mes])
    
    return f"{cantidad_films} peliculas fueron estrenadas en el mes de {mes.title()}"

@app.get('/cantidad_filmaciones_dia/')
def cantidad_filmaciones_dia(dia):
    dia = dia.lower()
    if dia in dias:
        num_dia = dias[dia]
    else:
        return f'Dia "{dia}" no válido.'
    
    cantidad_films = len(movies[ movies['day_of_week'] == num_dia])
    
    return f"{cantidad_films} peliculas fueron estrenadas en el dia {dia.title()}."

@app.get('/score_titulo/')
def score_titulo(titulo):
    titulo = titulo.lower().strip()
    if movies['title'].str.lower().str.contains(titulo).any() or movies['original_title'].str.lower().str.contains(titulo).any():
        release_year = movies[movies['title'].str.lower() == titulo]['release_year'].iloc[0]
        popularity = movies[movies['title'].str.lower() == titulo]['popularity'].iloc[0]
        return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}" con un score/popularidad de "{popularity}".'
    else:
        return f'La pelicula "{titulo.title()}" no se encuentra en el dataset.'
    
@app.get('/votos_titulo/')
def votos_titulo(titulo):
    titulo = titulo.lower().strip()
    if movies['title'].str.lower().str.contains(titulo).any() or movies['original_title'].str.lower().str.contains(titulo).any():
        votos = movies[movies['title'].str.lower() == titulo]['vote_count'].iloc[0]
        release_year = movies[movies['title'].str.lower() == titulo]['release_year'].iloc[0]
        if votos > 2000:
            promedio = movies[movies['title'].str.lower() == titulo]['vote_average'].iloc[0]
            return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}". La misma cuenta con un total de "{votos.astype(int)}" valoraciones, con un promedio de "{promedio}".'
        else:
            return f'La pelicula "{titulo.title()}" fue estrenada en el anio "{release_year}". La misma cuenta con un total de "{votos.astype(int)}" valoraciones. Debido a que cuenta con menos de 2000 valoraciones no se toma en cuenta el promedio.'
    else:
        return f'La pelicula "{titulo.title()}" no se encuentra en el dataset.'
    
@app.get('/get_actor/')
def get_actor(actor):
    actor = actor.lower()
    
    # Filtro las películas donde el actor esta en el elenco pero no es director
    peliculas_con_actor_sin_dirigir = movies[
        movies['cast'].apply(fa.get_cast_list).apply(lambda x: actor in x) &
        ~movies['crew'].apply(fa.get_director_list).apply(lambda x: actor in x)
    ]
    
    sum_films = len(peliculas_con_actor_sin_dirigir)
    sum_return = peliculas_con_actor_sin_dirigir['return'].sum().round(2)
    
    avg_return = (sum_return / sum_films).round(2) if sum_films > 0 else 0

    genero = literal_eval(peliculas_con_actor_sin_dirigir['cast'].iloc[0])[0]['gender']

    if genero == 1:
        return f'La actriz "{actor.title()}" ha participado en "{sum_films}" peliculas donde no fue directora, con un retorno total de "{sum_return}" y un promedio de "{avg_return}" por pelicula.'
    return f'El actor "{actor.title()}" ha participado en "{sum_films}" peliculas donde no fue director, con un retorno total de "{sum_return}" y un promedio de "{avg_return}" por pelicula.'

@app.get('/get_director/')
def get_director(director):
    director = director.lower()
    sum_return =0
    peliculas_dirigidas = movies[movies['crew'].apply(fa.get_director_list).apply(lambda x: director in x)]
    lanzamientos = peliculas_dirigidas['release_date'].tolist()
    retorno = peliculas_dirigidas['return'].round(2).tolist()
    costo = peliculas_dirigidas['budget'].round(0).tolist()
    ganancia = peliculas_dirigidas['revenue'].round(0).tolist()
    sum_return = peliculas_dirigidas['return'].sum().round(2)

    genero = literal_eval(peliculas_dirigidas['crew'].iloc[0])[0]['gender']

    if genero ==1:
        resultado = (f'La directora "{director.title()}" ha tenido un exito de "{sum_return}".\n')
    else:
        resultado = (f'El director "{director.title()}" ha tenido un exito de "{sum_return}".\n')
    for i, pelicula in enumerate(peliculas_dirigidas['title']):
        resultado += (f'Dirigio la pelicula "{pelicula}" lanzada en "{lanzamientos[i]}" con un costo de "{costo[i]}", una ganancia de "{ganancia[i]}" y por lo tanto un retorno de "{retorno[i]}"\n')
    return resultado
