from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from simpledu.models import db, User
from wtforms import ValidationError


class RegisterForm(FlaskForm):
    username = StringField(
        '用户名', validators=[Required(message='用户名不能为空'), Length(3, 24, message='用户名长度要在6~24个字符之间')])
    email = StringField(
        '邮箱', validators=[Required(message='邮箱不能为空'), Email(message='请输入合法的email地址')])
    password = PasswordField(
        '密码', validators=[Required(message='密码不能为空'), Length(6, 24, message='密码长度要在6~24个字符之间')])
    repeat_password = PasswordField(
        '重复密码', validators=[Required(message='请再次输入密码'), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):
    email = StringField(
        '邮箱', validators=[Required(), Email(message='请输入合法的email地址')])
    password = PasswordField(
        '密码', validators=[Required(), Length(6, 24, message='密码长度要在6~24个字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
