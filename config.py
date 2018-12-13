import logging

class Config(object):
    '''配置信息'''

    MONGO_URI = 'mongodb://localhost:27017/baby'  # 设置连接参数


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR

# 定义配置字典
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}