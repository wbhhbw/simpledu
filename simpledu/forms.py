from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange
from simpledu.models import db, User, Course, Live
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
        # 使用用户表单数据填充 user对象
        self.populate_obj(user)
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
    username = StringField(
        '用户名', validators=[Required(message='用户名不能为空')])
    password = PasswordField(
        '密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户未注册')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(), Length(5, 32)])
    description = TextAreaField(
        '课程简介', validators=[Required(), Length(20, 256)])
    image_url = StringField('封面图片', validators=[Required(), URL()])
    author_id = IntegerField(
        '作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(self.author_id.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充 course对象
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class UserForm(RegisterForm):
    role = IntegerField('角色', validators=[Required()])
    submit = SubmitField('提交')

    def validate_role(self, field):
        if self.role.data not in (10, 20, 30):
            raise ValidationError('数值不正确，请输入10,20或30')

    def validate_username(self, field):
        pass

    def validate_email(self, field):
        pass

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LiveForm(FlaskForm):
    name = StringField('直播名称', validators=[Required(), Length(5, 32)])
    user_id = IntegerField(
        '主播ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_user_id(self, field):
        if not User.query.get(self.user_id.data):
            raise ValidationError('用户不存在')

    def create_live(self):
        live = Live()
        # 使用课程表单数据填充live对象
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live
