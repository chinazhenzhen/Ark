from flask import Flask
from flask import jsonify
from flask import redirect
from flask_cors import CORS


from back_server.services.container import create_container

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify({'value':"welcome ARK"}), 200

@app.route('/about')
def ark_about():
    return jsonify("Ark--Linux教学实践系统")

@app.route('/container/create')
def container_create():
    create_container(9999)
    return redirect("http://localhost:9999")

app.run(port=3000)