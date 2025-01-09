import requests

class OMDBService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.omdbapi.com/"

    def get_movie_info(self, title, year=None):
        params = {
            "t": title,
            "y": year,
            "apikey": self.api_key,
            "plot": "full"
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                return data
            else:
                raise Exception(data.get("Error", "Ошибка при запросе фильма"))
        else:
            raise Exception("Ошибка при запросе к OMDB API")
