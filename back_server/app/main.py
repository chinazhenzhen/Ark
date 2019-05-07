from flask import Flask
from flask import jsonify
from flask import redirect, json, request, abort, g, render_template
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
import datetime


from .exts import db
from services.container import ContainerManager


from .model import User
from .model import Container

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gengxiaojin@127.0.0.1:3306/ark'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

auth = HTTPBasicAuth()

# container 管理器
container_manager = ContainerManager()


@app.route('/')
#@auth.login_required
def hello_world():
    return render_template('index.html')
    # return jsonify({'value': "welcome ARK %s".format(g.user.username)}), 200


@app.route('/register', methods=['POST'])
def new_user():
    # 注册新用户
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username })


@auth.verify_password
def verify_password(username_or_token, password):
    if request.path == "/login":
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    else:
        user = User.verify_auth_token(username_or_token)
        if not user:
            return False
    g.user = user
    return True


@app.route('/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify(str(token, encoding='utf-8'))


@app.route('/about')
def ark_about():
    return jsonify("Ark--Linux教学实践系统")

@app.route('/container/create')
def container_create():
    container_name = container_manager.create_container("ark:latest")
    ports = container_manager.get_container_ports(container_name)
    webshell_port = ports['9000/tcp'] # 得到相关接口
    ip = 'http://{}:{}'.format('127.0.0.1', webshell_port)
    os_name = "ark:latest"
    #create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container = Container(os_name=os_name, ip=ip, container_name=container_name)
    db.session.add(container)
    db.session.commit()

    return redirect(ip)

    #return jsonify({'url': 'http://{}:{}'.format('127.0.0.1', webshell_port)})

@app.route('/container/show')
def container_show():
    containers = Container.query.all()
    return render_template('show.html',containers=containers)