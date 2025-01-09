import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    HTTP_PROXY = os.getenv('HTTP_PROXY')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', 'localhost')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))