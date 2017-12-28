from flask import Flask, render_template
from simpledu.config import configs  # 传入configs字典
from simpledu.models import db, Course
from flask_migrate import Migrate


def create_app(config):
    """APP工厂
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # SQLAlchemy 的初始化方式改为使用 init_app
    db.init_app(app)
    register_blueprints(app)
    Migrate(app, db)

    return app


def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
