from flask import Flask
from flask_cors import CORS
from server.routes import api
from server.utils.config import Config

app = Flask(__name__)
CORS(app)

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host=Config.FLASK_HOST, port=Config.FLASK_PORT)
