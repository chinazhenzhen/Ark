from datetime import datetime
from flask_login import UserMixin
from .exts import db
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class Container(db.Model):
    __tablename__ = 'containers'
    id = db.Column(db.Integer, primary_key=True)
    os_name = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())
    ip = db.Column(db.String(64))
    container_name = db.Column(db.String(64))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 外键，外键关联users表的id，我们还需要在User做关系关联


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))

    containers = db.relationship("Container", backref='users') # containers表外键关系关联，Container 类名，backref='users' 声明关联users表

    # 密码加密
    def hash_password(self, password):
        self.password = custom_app_context.encrypt(password)

    # 密码解析
    def verify_password(self, password):
        if self.password == password:
            return True
        return False

    # 获取token，有效时间100min
    def generate_auth_token(self, expiration=6000):
        s = Serializer('jklklsadhfjkhwbii9/sdf\sdf', expires_in=expiration)
        return s.dumps({'id': self.id})

    # 解析token，确认登录的用户身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer('jklklsadhfjkhwbii9/sdf\sdf')  # jklklsadhfjkhwbii9/sdf\sdf  ==> SECRET_KEY
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])

        return user
