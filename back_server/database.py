# flask 数据库迁移文档 https://www.jianshu.com/p/c465228e30ae

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import app, db

# 引入数据库表
from app.model import User

manager = Manager(app)

#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app,db)

#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
