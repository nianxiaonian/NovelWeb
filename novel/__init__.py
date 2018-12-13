import logging
from logging.handlers import RotatingFileHandler
from flask_pymongo import PyMongo

from flask import Flask

from flask_wtf.csrf import CSRFProtect
from flask_session import Session

from config import config

# 数据库
from novel.utils.commons import index_filter

mongo = PyMongo()


def create_app(config_name):
    """通过传入不同的配置名字，初始化其对应配置的应用实例"""
    setup_log(config_name)
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    mongo.init_app(app)

    CSRFProtect(app)
    Session(app)
    # 注册蓝图
    from novel.modules.index import index_blu
    app.register_blueprint(index_blu)

    # 导入自定义的过滤器
    app.add_template_filter(index_filter, 'index_filter')
    return app


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

