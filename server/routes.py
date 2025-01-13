from flask import Blueprint, request, jsonify
from server.services.omdb_service import OMDBService
from server.services.movie_info import MovieInfo
from server.utils.gpt_request import GPTClient, generate_crossed_movie
from server.utils.config import Config

api = Blueprint('api', __name__)

gpt_client = GPTClient(Config.OPENAI_API_KEY)
omdb_service = OMDBService(Config.OMDB_API_KEY)
movie_info = MovieInfo(omdb_service)

@api.route('/get-movie', methods=['POST'])
def create_crossed_movie():
    try:
        data = request.json
        user_input_movies = data.get('movies', [])
        if not user_input_movies:
            return jsonify({"error": "Список фильмов пуст"}), 400

        prompt = (
            "Подбери реально существующий фильм, который совмещает в себе элементы "
            f"вот этих фильмов, но НЕ входит в их список: {', '.join(user_input_movies)}. "
            "Назови такой фильм, который существует в реальности."
            "Также назови 10 фильмов, которые тоже совмещают в себе элементы фильмов"
            f"НО НЕ ВХОДЯТ в их список: {', '.join(user_input_movies)}."
            "Вся информация о фильме должна быть выведена на РУССКОМ языке, КРОМЕ английского названия."
        )
        gpt_response = generate_crossed_movie(prompt, gpt_client)
        raw_omdb = omdb_service.get_movie_info(gpt_response['english_movie_title'],gpt_response['main_movie_year'])
        if not raw_omdb or raw_omdb.get('Response') == 'False':
            raw_omdb = omdb_service.get_movie_info(gpt_response['english_movie_title'],None)

        mapped_data = movie_info.get_movie_details_from_raw(raw_omdb)
        mapped_data["title"] = gpt_response['main_movie_title']
        mapped_data["genres"] = gpt_response['movie_genres']
        mapped_data["country"] = gpt_response['movie_country']
        mapped_data["director"] = gpt_response['movie_director']
        mapped_data["actors"] = gpt_response['movie_actors']
        mapped_data["description"] = gpt_response['movie_description']
        mapped_data["reason"] = gpt_response['movie_reason']
        mapped_data["similar"] = gpt_response['ten_crossed_movies_list']
        print(mapped_data)
        return jsonify(mapped_data)

    except Exception as e:
        print(f"Ошибка в create_crossed_movie: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/favicon.ico')
def favicon():
    return '', 204