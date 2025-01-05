import openai
import os
import json
import requests as rq
from bs4 import BeautifulSoup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

os.environ['https_proxy'] = os.getenv('http_proxy_data')
openai.api_key = os.getenv('open_ai_api_key')

def get_request_omdb(eng_movie_title,movie_year):
    omdb_request = rq.get(f'https://www.omdbapi.com/?t={eng_movie_title}&y={movie_year}&plot=full&apikey={os.getenv('omdb_api_key')}')
    omdb_movie_info = json.loads(str(BeautifulSoup(omdb_request.content,'html.parser')))
    return omdb_movie_info

def create_crossed_movie(user_input_movies):
    crossed_movie_generation_function = [
        {
            'name': 'get_crossed_movie',
            'description': 'Получить информацию о существующем в реальности фильме, который может стать комбинацией приведенных в списке фильмов, объединяя элементы из них',
            'parameters': {
                'type': 'object',
                'properties':{
                    'main_movie_title':{
                        'type':'string',
                        'description':'Название наиболее подходящего существующего в реальности фильма, который получился в результате скрещивания фильмов приведенных пользователем (например, на основе жанра, сюжета, актеров, режиссера и т.д.)',
                    },
                    'main_movie_year':{
                        'type':'integer',
                        'description': 'Год выпуска этого фильма',
                    },
                    'ten_crossed_movies_list':{
                        'type':'string',
                        'description':'Список из 10 фильмов, которые так же могли бы стать отличной комбинацией фильмов из списка пользователя (но не являются самими этими фильмами) (через "/")',
                    },
                    'ten_crossed_movies_years_list':{
                        'type':'string',
                        'description': 'Список годов выпуска для 10 фильмов из полученного ранее списка (через "/")',
                    },
                    'eng_movie_title':{
                        'type':'string',
                        'description':'Оригинальное название этого фильма на английском языке'
                    },
                    'eng_ten_crossed_movies_list':{
                        'type':'string',
                        'description':'Список названий этих 10 скрещенных фильмов на английском языке (через "/")'
                    },
                },
            },
        },
    ]
    request_prompt = f"""Найди фильм еще один существующий в реальности фильм, который совмещает в себе элементы фильмов из списка {', '.join(user_input_movies)}, но не находится в этом списке фильмов.
Выведи информацию о названии этого фильма на русском и английском языке, год выпуска этого фильма, список из названий на русском и английском 10 разных фильмов, которые тоже подходят, как комбинации этих фильмов и их годы выпуска"""
    while True:
        params_dict = make_gpt_request(crossed_movie_generation_function,request_prompt)
        omdb_movie_info = get_request_omdb(params_dict['eng_movie_title'], params_dict['main_movie_year'])
        if omdb_movie_info['Response'] != 'False' and params_dict['main_movie_title'].lower() not in [movie.lower() for movie in user_input_movies]:
            break

    print(f'Вам подходит фильм под названием "{params_dict['main_movie_title']}"({params_dict['main_movie_year']})')
    movie_info(user_input_movies,f'{params_dict['main_movie_title']}({params_dict['main_movie_year']})',params_dict['eng_movie_title'],params_dict['main_movie_year'])
    crossed_movies_info_list = {movie_title:[movie_eng_title,movie_year] for movie_title,movie_eng_title,movie_year in zip(params_dict['ten_crossed_movies_list'].split('/'),params_dict['eng_ten_crossed_movies_list'].split('/'),params_dict['ten_crossed_movies_years_list'].split('/'))}
    print(f"""Также вы можете посмотреть информацию о других похожих фильмах из списка:
    {', '.join(f'{ru_movie_title}({crossed_movies_info_list[ru_movie_title][1]})' for ru_movie_title in crossed_movies_info_list)}
    """)
    while True:
        user_choise_movie = input()
        if user_choise_movie not in params_dict['ten_crossed_movies_list'].split('/'):
            break
        else:
            movie_info(user_input_movies,user_choise_movie,crossed_movies_info_list[user_choise_movie][0],crossed_movies_info_list[user_input_movies][1])

def movie_info(user_input_movies,movie_title,eng_movie_title,movie_year):
    omdb_movie_info = get_request_omdb(eng_movie_title,movie_year)
    get_movie_info_function = [
        {
            'name':'get_movie_info',
            'description':'Получение определенной информация об определенном фильме',
            'parameters':{
                'type':'object',
                'properties':{
                    'movie_year':{
                        'type':'integer',
                        'description':'Год выпуска данного фильма',
                    },
                    'movie_age_restriction':{
                        'type':'string',
                        'description':f'Возрастное ограничение этого фильма для страны Россия (в формате,например, 16+). Формат ограничения {omdb_movie_info['Rated']} переведи в вид по типу "16+"',
                    },
                    'movie_genres':{
                        'type':'string',
                        'description':'Список из жанров этого фильма (через "/")',
                    },
                    'movie_countries':{
                        'type':'string',
                        'description':'Список названий стран, снимавших данный фильм (через "/")',
                    },
                    'movie_directors':{
                        'type':'string',
                        'description':'Список имен режиссёров данного фильма (через "/")',
                    },
                    'movie_star_actors':{
                        'type':'string',
                        'description':'Список имен знаменитых актеров, игравших в этом фильме (через "/")',
                    },
                    'movie_cross_info':{
                        'type':'string',
                        'description': f'Полное описание чем этот фильм похож на фильм(-ы) из списка  ({user_input_movies})'
                    },
                    'movie_imdb_rating':{
                        'type':'string',
                        'description':'IMDb-рейтинг этого фильма'
                    },
                    'movie_description':{
                        'type':'string',
                        'description':f'Переведенное описание из {omdb_movie_info['Plot']}'
                    },
                    'movie_poster_link':{
                        'type':'string',
                        'description':f'Ссылка на постер к фильму из {omdb_movie_info['Poster']} (если его нет, то выведи "нет постера")'

                    }
                }
            }
        }
    ]
    request_prompt = (f"""Найди информацию о фильме {movie_title}, в которой должен быть год выпуска, возрастные ограничения, жанры этого фильма, страны, режиссёры, IMDb-рейтинг, знаменитые актеры и почему этот фильм является комбинацией {user_input_movies}.
    Также дай подробное описание фильма своими словами, понятным языком
    Если информацию по какому-либо пункту получить невозможно выводи, в этом пункте "Нет информации".
    Используй информацию из этого словаря: {omdb_movie_info}, переводи ее на русский язык!
""")
    params_dict = make_gpt_request(get_movie_info_function,request_prompt)
    country_info_format = 'Страны' if len(params_dict['movie_countries'].split('/')) > 1 else 'Страна'
    director_info_format = 'Режиссёры' if len(params_dict['movie_directors'].split('/')) > 1 else 'Режиссёр'
    print()
    print(f"""Информация о фильме:
    Год выпуска: {params_dict['movie_year']}
    Возрастное ограничение: {params_dict['movie_age_restriction']}
    Жанры: {', '.join(params_dict['movie_genres'].split('/'))}
    IMDb-рейтинг: {params_dict['movie_imdb_rating']}
    {country_info_format}: {', '.join(params_dict['movie_countries'].split('/'))}
    {director_info_format}: {', '.join(params_dict['movie_directors'].split('/'))}
    Знаменитые актёры: {', '.join(params_dict['movie_star_actors'].split('/'))}
    Описание: {params_dict['movie_description']}
    Ссылка на постер к фильму: {params_dict['movie_poster_link']}
    Почему этот фильм подходит?
    {params_dict['movie_cross_info']}
    """)

def make_gpt_request(function,request_prompt):
    response_completion = openai.chat.completions.create(
        model = 'gpt-4o-mini-2024-07-18',
        messages = [{'role':'user','content':request_prompt}],
        functions = function,
        function_call = 'auto',
    )
    response_output = response_completion.choices[0].message
    response_params = json.loads(response_output.function_call.arguments)
    return response_params