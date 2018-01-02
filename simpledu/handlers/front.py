from flask import Blueprint, render_template
from simpledu.models import Course, User
from simpledu.forms import LoginForm, RegisterForm
from flask import flash
from flask_login import login_user, login_required, logout_user
from flask import redirect, url_for
from flask import request, current_app

# 省略了 url_prefix参数，那么默认就是 '/'
front = Blueprint('front', __name__)


# 此处url: '/' 代表 url:'/admin'
@front.route('/')
def index():
    # 获取参数中传递过来的页数
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('index.html', pagination=pagination)


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # 第一个参数是 User 对象，第二个参数是个布尔值，告诉 flask-login 是否需要记住该用户。
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    # flash第一个参数表示信息，第二个参数表示分类，不指定分类默认分类为message
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))


@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # validate_on_submit 是 flask-wtf 提供的 FlaskForm
    # 中封装的一个方法，返回值是一个布尔值。如果表单提交了并且我们在对应的 form
    # 中声明的表单数据验证器对用户提交的表单数据验证通过，那么该方法返回 True，否则返回 False。
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        # .login 是 front.login 的简写，如果重定向到当前 Blueprint 下的某个路由就可以这样简写。
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
