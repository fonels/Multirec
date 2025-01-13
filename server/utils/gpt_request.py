import openai
import json
import os
from server.utils.config import Config

os.environ["https_proxy"] = Config.HTTP_PROXY

class GPTClient:
    def __init__(self, api_key, model="gpt-4o"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def make_request(self, functions, prompt):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful assistant. The user wants you to generate a new movie "
                            "based on two films. You have a function `get_crossed_movie`. "
                            "You MUST call this function (and only this function) with valid JSON."
                            "You MUST display information about movies that are not included in the list provided in the prompt."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt}],
                functions=functions or [],
                function_call={"name": "get_crossed_movie"},
            )
            return response.choices[0].message
        except Exception as e:
            raise Exception(f"Ошибка при запросе к OpenAI API: {e}")

def generate_crossed_movie(prompt, gpt_client):
    functions = [
        {
            "name": "get_crossed_movie",
            "description": "Генерация похожего, НЕ находящегося в списке, фильма на основе введённых пользователем фильмов.",
            "parameters": {
                "type": "object",
                "properties": {
                    "main_movie_title": {"type": "string", "description": "Название похожего фильма, которого НЕТ в списке"},
                    "main_movie_year": {"type": "integer", "description": "Год выпуска"},
                    "ten_crossed_movies_list": {"type": "string", "description": "Список из 10 фильмов"},
                    "english_movie_title": {"type": "string", "description": "Название этого фильма на английском языке"},
                    "movie_reason": {"type": "string", "description": "Чем эти фильмы похожи? Составь объемное описание"},

                    "movie_genres": {"type": "string","description": "Напиши все жанры этого фильма"},
                    "movie_country": {"type": "string", "description": "Напиши все страны, в которых снимался фильм"},
                    "movie_director": {"type": "string", "description": "Напиши полное имя режиссёра"},
                    "movie_actors": {"type": "string", "description": "Напиши имена актёров, снявшихся в этом фильме"},
                    "movie_description": {"type": "string", "description": "Напиши полное описание фильма"},
                },
                "required": ["main_movie_title", "main_movie_year", "ten_crossed_movies_list", "english_movie_title", "movie_reason", "movie_genres","movie_country",
                             "movie_director", "movie_actors", "movie_description"],
            },
        }
    ]
    try:
        response_message = gpt_client.make_request(functions, prompt)
        function_call = response_message.function_call
        if function_call:
            arguments = json.loads(function_call.arguments)
            return arguments
        else:
            raise Exception("Ошибка: функция не вызвана.")
    except Exception as e:
        raise Exception(f"Ошибка при выполнении generate_crossed_movie: {e}")