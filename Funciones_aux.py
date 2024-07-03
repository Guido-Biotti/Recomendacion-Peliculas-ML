from ast import literal_eval
import pandas as pd

#Estas funciones me retornan los valores que voy a usar de las columnas anidadas del df

def get_collection_name(row):
    if pd.isna(row):
        return None
    try:
        return literal_eval(row)['name']
    except:
        return None
    
def get_genre_names(genres_list):

    genres_list = literal_eval(genres_list)
    genre_names = []
    if genres_list != [] or genres_list != None:
        for genre in genres_list:
            genre_names.append(genre['name'])
    return genre_names

def get_companies_names(companies_list):
    try:
        companies_list = literal_eval(companies_list)
        companies_names = []
        if companies_list != []:
            for company in companies_list:
                companies_names.append(company['name'])
        return companies_names
    except:
        return []
    
def get_country_iso(countries_list):
    try:
        countries_list = literal_eval(countries_list)
        countries_iso = []
        if countries_list != []:
            for country in countries_list:
                countries_iso.append(country['iso_3166_1'])
        return countries_iso
    except:
        return []
    
def get_language_iso(languages_list):
    try:
        languages_list = literal_eval(languages_list)
        languages_iso = []
        if languages_list != []:
            for language in languages_list:
                languages_iso.append(language['iso_639_1'])
        return languages_iso
    except:
        return []
    
def get_cast_list(row):
    cast_names = []
    cast_data = literal_eval(row)
    for actor in cast_data:
        cast_names.append(actor['name'].lower())
    return cast_names

def get_director_list(row):
    crew_data = literal_eval(row)
    director_names = []
    for director in crew_data:
        if director['job'].lower() == 'director':
            director_names.append(director['name'].lower())
    return director_names
