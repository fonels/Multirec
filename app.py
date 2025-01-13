from flask import Flask, render_template
from flask_cors import CORS
from server.routes import api
import os

app = Flask(__name__, template_folder="client",static_folder="client/static")
CORS(app)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)