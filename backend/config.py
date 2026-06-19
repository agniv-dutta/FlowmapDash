import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    VERSION = os.environ.get("APP_VERSION", "1.0.0")

    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "flowmapdash")
    MONGO_POOL_SIZE = int(os.environ.get("MONGO_POOL_SIZE", "50"))

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    RATELIMIT_CAPACITY = int(os.environ.get("RATELIMIT_CAPACITY", "200"))
    RATELIMIT_REFILL_RATE = float(os.environ.get("RATELIMIT_REFILL_RATE", "20.0"))

    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    TESTING = True
    MONGO_DB_NAME = "flowmapdash_test"
    LOG_LEVEL = "DEBUG"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def load_config():
    env = os.environ.get("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
