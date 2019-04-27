from flask import Flask
from flask import jsonify
from flask import redirect
from flask_cors import CORS


from back_server.services.container import ContainerManager

app = Flask(__name__)
CORS(app)

container_manager = ContainerManager()

@app.route('/')
def hello_world():
    return jsonify({'value': "welcome ARK"}), 200

@app.route('/about')
def ark_about():
    return jsonify("Ark--Linux教学实践系统")

@app.route('/container/create')
def container_create():
    container_name = container_manager.create_container("ark:latest")
    ports = container_manager.get_container_ports(container_name)
    webshell_port = ports['9000/tcp'] # 得到相关接口

    return jsonify({'url': 'http://{}:{}'.format('127.0.0.1', webshell_port)})

app.run(port=3000)