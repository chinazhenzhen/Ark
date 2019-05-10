from flask import Flask
from flask import jsonify
from flask import redirect, json, request, abort, g, render_template, url_for, flash
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import datetime


from .exts import db
from services.container import ContainerManager


from .model import User
from .model import Container

from .form import LoginForm
from .form import RegisterForm

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gengxiaojin@127.0.0.1:3306/ark'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = "12345678"
db.init_app(app)

auth = HTTPBasicAuth()

# 登陆管理器
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
login_manager.login_view = 'login'
login_manager.login_message = 'Unauthorized User'

# container 管理器
container_manager = ContainerManager()


@app.route('/')
def index():
    return render_template('index.html')
    # return jsonify({'value': "welcome ARK %s".format(g.user.username)}), 200


# @app.route('/register', methods=['POST'])
# def new_user():
#     # 注册新用户
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400)  # missing arguments
#     if User.query.filter_by(username=username).first() is not None:
#         abort(400)  # existing user
#
#     user = User(username=username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({ 'username': user.username })


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        next = request.args.get('next')
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            # login_user(user, form.remember_me.data)
            if next is None or not next.startswith('/'):
                next = url_for('index')
            flash('登陆成功')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经成功退出登陆')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User()
    if form.validate_on_submit():
        if user.query_one_user(form.name.data) is not None:
            flash("用户名已经存在")
        else:
            user = User(username=form.username.data,
                        password=form.password.data)
            flash("注册成功")
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/about')
def ark_about():
    return jsonify("Ark--Linux教学实践系统")

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/container/create')
@login_required
def container_create():
    container_name = container_manager.create_container("ark:latest")
    ports = container_manager.get_container_ports(container_name)
    webshell_port = ports['9000/tcp'] # 得到相关接口
    ip = 'http://{}:{}'.format('127.0.0.1', webshell_port)
    os_name = "ark:latest"
    username = current_user.username
    #create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container = Container(os_name=os_name, ip=ip, container_name=container_name, username=username)
    db.session.add(container)
    db.session.commit()

    return redirect(ip)

    #return jsonify({'url': 'http://{}:{}'.format('127.0.0.1', webshell_port)})

@app.route('/container/show')
@login_required
def container_show():
    containers = Container.query.filter_by(username=current_user.username).all()
    return render_template('show.html',containers=containers)