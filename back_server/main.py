from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify({'value':"welcome ARK"}), 200

@app.route('/about')
def ark_about():
    return jsonify("Ark--Linux教学实践系统")

app.run(port=3000)