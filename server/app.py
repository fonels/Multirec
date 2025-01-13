from flask import Flask, render_template
from flask_cors import CORS
from .routes import api
from .utils.config import Config
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'client')
STATIC_FOLDER = os.path.join(BASE_DIR, 'client/static')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER,static_folder=STATIC_FOLDER)
CORS(app)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host=Config.FLASK_HOST, port=Config.FLASK_PORT)
