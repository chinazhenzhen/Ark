from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired


# 登陆表单
class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    # remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('登陆')


# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('注册')


class OsSelectForm(FlaskForm):
    limit = SelectField(label='操作系统',
                        choices=[('Centos7', 'Centos'),
                                 ('Ubuntu14.04', 'Ubuntu'),
                                 ('Ark', 'Ark')],
                        default='Centos7')  # 权限
    submit = SubmitField('创建')
