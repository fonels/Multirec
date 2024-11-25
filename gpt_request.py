import openai
import os
import json
import config

os.environ['https_proxy'] = config.http_proxy_data
openai.api_key = config.open_ai_api_key

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
                },
            },
        },
    ]
    request_prompt = f'Найди фильм еще один существующий в реальности фильм, который совмещает в себе элементы фильмов из списка {', '.join(user_input_movies)}, но не находится в этом списке фильмов'
    params_dict = make_gpt_request(crossed_movie_generation_function,request_prompt)
    print(f'Вам подходит фильм под названием "{params_dict['main_movie_title']}"({params_dict['main_movie_year']})')
    movie_info(user_input_movies,f'{params_dict['main_movie_title']}({params_dict['main_movie_year']})')
    print(f"""Также вы можете посмотреть информацию о других похожих фильмах из списка:
    {', '.join([f'{movie_name}({movie_year})' for movie_name,movie_year in zip(params_dict['ten_crossed_movies_list'].split('/'),params_dict['ten_crossed_movies_years_list'].split('/'))])}
    """)
    while True:
        user_choise_movie = input()
        if user_choise_movie not in params_dict['ten_crossed_movies_list'].split('/'):
            break
        else:
            movie_info(user_input_movies,user_choise_movie)

def movie_info(user_input_movies,movie_title):
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
                        'description':'Возрастное ограничение этого фильма для страны Россия (в формате,например, 16+)',
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
                        'description':'Опиши фильм своими словами'
                    }
                }
            }
        }
    ]
    request_prompt = (f"""Найди информацию о фильме {movie_title}, в которой должен быть год выпуска, возрастные ограничения, жанры этого фильма, страны, режиссёры, IMDb-рейтинг, знаменитые актеры и почему этот фильм является комбинацией {user_input_movies}.
    Также дай подробное описание фильма своими словами, понятным языком
    Если информацию по какому-либо пункту получить невозможно выводи, в этом пункте "Нет информации".
    Приведенную информацию перевести на русский.
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
create_crossed_movie(['Один дома','Барби','Тупой и еще тупее'])