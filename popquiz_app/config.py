import os
from urllib.parse import quote_plus
from datetime import  datetime

class Config:
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'zmtxzs2004@'  # 移除转义字符
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'MSN'
    MYSQL_CHARSET = 'utf8mb4'

    # 连接数据库
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'
    # 数据盐
    SECRET_KEY = os.urandom(16)

    #设置json数据不适应ascii编码
    JSON_AS_ASCII = False

    # JSONIFY_PRETTYPRINT_REGULAR = False
    # JSON_SORT_KEYS = False
    RESETFUL_JSON = {
        'ensure_ascii': False
    }
    # # 连接 MongoDB
    # MONGO_URI = "mongodb://localhost:27017/"
    # client = MongoClient(MONGO_URI)
    # db = client["popquiz"]
    # print("? MongoDB 连接成功："+MONGO_URI+" /"+db.name)

class DevelopmentConfig(Config):
    #开发环境
    # 开启调试模式
    DEBUG = True

class ProductionConfig(Config):
    # 生产环境
    # 关闭调试模式
    DEBUG = False

class TestingConfig(Config):
    # 测试环境
    pass

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}