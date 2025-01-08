import openai
import json

class GPTClient:
    def __init__(self, api_key, model = "gpt-4o-mini-2024-07-18"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def make_request(self, prompt, functions = None, function_call = "auto"):
        try:
            response = openai.ChatCompletion.create(
                model = self.model,
                messages = [{"role": "user", "content": prompt}],
                functions = functions or [],
                function_call = function_call,
            )
            return response.choices[0].message
        except openai.OpenAIError as e:
            raise Exception(f"Ошибка при запросе к OpenAI API: {e}")

def generate_crossed_movie(prompt, gpt_client):
    functions = [
        {
            "name": "get_crossed_movie",
            "description": "Генерация фильма на основе введённых пользователем фильмов.",
            "parameters": {
                "type": "object",
                "properties": {
                    "main_movie_title": {"type": "string", "description": "Название фильма"},
                    "main_movie_year": {"type": "integer", "description": "Год выпуска"},
                    "ten_crossed_movies_list": {"type": "string", "description": "Список из 10 фильмов"},
                },
            },
        }
    ]
    response_message = gpt_client.make_request(prompt, functions = functions)
    if "function_call" in response_message:
        return json.loads(response_message["function_call"]["arguments"])
    else:
        raise Exception("Ошибка: функция не вызвана.")