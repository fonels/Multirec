from flask import Blueprint, request, jsonify, render_template
from server.services.omdb_service import OMDBService
from server.utils.gpt_request import GPTClient, generate_crossed_movie
from server.utils.config import Config

api = Blueprint('api', __name__)

gpt_client = GPTClient(Config.OPENAI_API_KEY)
omdb_service = OMDBService(Config.OMDB_API_KEY)

@api.route('/get-movie', methods=['POST'])
def create_crossed_movie():
    """Эндпоинт для получения фильма на основе пользовательского ввода."""
    data = request.json
    user_input_movies = data.get('movies', [])

    if not user_input_movies:
        return jsonify({"error": "Список фильмов пуст"}), 400

    prompt = f"Найди фильм, который совмещает в себе элементы фильмов: {', '.join(user_input_movies)}."
    try:
        gpt_response = generate_crossed_movie(prompt, gpt_client)
        movie_data = omdb_service.get_movie_info(
            gpt_response['main_movie_title'], gpt_response['main_movie_year']
        )
        return jsonify(movie_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500