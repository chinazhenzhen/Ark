import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "mysql://root:gengxiaojin@127.0.0.1/rest"
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
BASEDIR = basedir
# 安全配置
CSRF_ENABLED = False
SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'

