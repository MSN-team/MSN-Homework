from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    Config = config_map.get(config_name)
    app.config.from_object(Config)
    db.init_app(app)
    #蓝图注册
    from theapp.user import user
    app.register_blueprint(user)

    return app
