from flask import Flask, render_template
from simpledu.config import configs  # 传入configs字典
from simpledu.models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app(config):
    """APP工厂
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    from .handlers import front, course, admin, live
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(live)

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
