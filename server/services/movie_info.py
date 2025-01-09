class MovieInfo:
    def __init__(self, omdb_service):
        self.omdb_service = omdb_service

    def get_movie_details_from_raw(self, raw_data):
        return {
            "title": raw_data.get("Title", "Нет информации"),
            "year": raw_data.get("Year", "Нет информации"),
            "rating": raw_data.get("Rating", "Нет информации"),
            "genres": raw_data.get("Genre", "Нет информации"),
            "director": raw_data.get("Director", "Нет информации"),
            "actors": raw_data.get("Actors", "Нет информации"),
            "description": raw_data.get("Plot", "Нет информации"),
            "poster": raw_data.get("Poster", "нет постера"),
            "imdb_rating": raw_data.get("imdbRating", "Нет информации"),
            "country": raw_data.get("Country", "Нет информации"),
            "age_restriction": self.format_age_rating(raw_data.get("Rated", "Нет информации"))
                }

    def get_movie_details(self, title, year=None):
        raw_data = self.omdb_service.get_movie_info(title, year)
        return self.get_movie_details_from_raw(raw_data)

    @staticmethod
    def format_age_rating(rating):
        """
        Преобразует возрастное ограничение из формата OMDB в локальный формат (например, 'PG-13' -> '16+').

        :param rating: Возрастное ограничение в формате OMDB (например, 'PG', 'R').
        :return: Преобразованное возрастное ограничение.
        """
        rating_map = {
            "G": "0+",
            "PG": "6+",
            "PG-13": "12+",
            "R": "16+",
            "NC-17": "18+"
        }
        return rating_map.get(rating, "Нет информации")