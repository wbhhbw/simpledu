from flask import Flask, render_template
from simpledu.config import configs  # 传入configs字典
from simpledu.models import db, Course

def create_app(config):
    """可以根据传入的config名称，加载不同的配置
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # SQLAlchemy 的初始化方式改为使用 init_app
    db.init_app(app)

    @app.route('/')
    def index():
        courses = Course.query.all()
        return render_template('index.html', courses=courses)

    @app.route('/admin')
    def admin_index():
        return 'admin'

    return app
