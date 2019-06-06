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

    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 外键，外键关联users表的id，我们还需要在User做关系关联


class Permission:
    READ = 0x01  # 查看权限
    CONTAINER = 0x02  # 容器操作权限
    ADMIN = 0x04  # 管理员权限

# 权限管理学习文档 https://blog.csdn.net/bird333/article/details/80919635
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)

    # 声明外键
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_role():
        roles = {
            'BLACK_USER': (Permission.READ, True),
            'USER': (Permission.READ |
                     Permission.CONTAINER, False),
            'ADMIN': (Permission.READ |
                      Permission.CONTAINER |
                      Permission.ADMIN, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                # 如果用户角色没有创建: 创建用户角色
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())
    # 外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 表明外键关系
    containers = db.relationship("Container", backref='users') # containers表外键关系关联，Container 类名，backref='users' 声明关联users表

    def __init__(self, **kwargs):
        '''构造函数：首先调用基类构造函数，如果创建基类对象后没定义角色，则根据email地址决定其角色'''
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == "admin":
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        # 检查permissions要求的权限角色是否允许
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        # 检查是否管理员
        return self.can(Permission.ADMIN)

    def query_one_user(self, username):
        return self.query.filter_by(username=username).first()


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
