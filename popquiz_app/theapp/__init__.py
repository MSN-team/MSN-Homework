from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    Config = config_map.get(config_name)
    
    app.config.from_object(Config)
    # app.json.ensure_ascii = False
    db.init_app(app)
    #蓝图注册
    from theapp.user import user_bp
    app.register_blueprint(user_bp)

    return app
