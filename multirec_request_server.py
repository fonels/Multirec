import openai
import os
import json
import config
import requests as rq
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['https_proxy'] = config.http_proxy_data
openai.api_key = config.open_ai_api_key

def get_request_omdb(eng_movie_title, movie_year):
    omdb_request = rq.get(f'https://www.omdbapi.com/?t={eng_movie_title}&y={movie_year}&plot=full&apikey={config.omdb_api_key}')
    omdb_movie_info = json.loads(str(BeautifulSoup(omdb_request.content,'html.parser')))
    
    return omdb_movie_info

@app.route('/api/get-movie', methods=['POST'])
def create_crossed_movie():
    print("Получен запрос:", request.json)
    data = request.json  # Получение данных от клиента
    user_input_movies = data.get('movies', [])

    if not user_input_movies:
        return jsonify({"error": "Список фильмов пуст"}), 400

    crossed_movie_generation_function = [
        {
            'name': 'get_crossed_movie',
            'description': 'Получить информацию о существующем в реальности фильме, который может стать комбинацией приведенных в списке фильмов, объединяя элементы из них',
            'parameters': {
                'type': 'object',
                'properties':{
                    'main_movie_title':{
                        'type':'string',
                        'description':'Название наиболее подходящего существующего в реальности фильма, который получился в результате скрещивания фильмов приведенных пользователем (например, на основе жанра, сюжета, актеров, режиссера и т.д.), но не совпадающее с ними',
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
    request_prompt = f"""Найди еще один существующий в реальности фильм, который совмещает в себе элементы фильмов из списка {', '.join(user_input_movies)}. Этот фильм не должен быть одним из тех, что находятся в списке!
Выведи информацию о названии этого фильма на русском и английском языке, год выпуска этого фильма, список из названий на русском и английском 10 разных фильмов, которые тоже подходят, как комбинации этих фильмов (но не находятся в списке) и их годы выпуска"""
    params_dict = make_gpt_request(crossed_movie_generation_function, request_prompt)

    omdb_movie_info = get_request_omdb(params_dict['eng_movie_title'], params_dict['main_movie_year'])
    if omdb_movie_info.get('Response') == 'False':
        return jsonify({"error": "Фильм не найден"}), 404
    
    movie_info_dict = movie_info(user_input_movies, params_dict['main_movie_title'], params_dict['eng_movie_title'], params_dict['main_movie_year'])

    response_data = {
        "title": params_dict['main_movie_title'],
        "year": params_dict['main_movie_year'],
        "age_restriction" : movie_info_dict['movie_age_restriction'],
        "country": movie_info_dict['movie_countries'],
        "director": movie_info_dict['movie_directors'],
        "actors": movie_info_dict['movie_star_actors'],
        "poster": movie_info_dict['movie_poster_link'],
        "genres": movie_info_dict['movie_genres'],
        "rating": movie_info_dict['movie_imdb_rating'],
        "description": movie_info_dict['movie_description'],
        "reason": movie_info_dict['movie_cross_info'],
        "similarMovies": params_dict['ten_crossed_movies_list'].split('/')
    }

    return jsonify(response_data)

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
    params_dict = make_gpt_request(get_movie_info_function, request_prompt)
    return params_dict

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

