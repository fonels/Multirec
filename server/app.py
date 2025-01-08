from flask import Flask, render_template
from flask_cors import CORS
from server.routes import api
from server.utils.config import Config

app = Flask(__name__, template_folder='/Users/a1111/Desktop/Multirec/client',static_folder='/Users/a1111/Desktop/Multirec/client/static')
CORS(app)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=Config.FLASK_DEBUG, host=Config.FLASK_HOST, port=Config.FLASK_PORT)
