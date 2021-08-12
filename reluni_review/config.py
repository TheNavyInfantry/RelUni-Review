from reluni_review import timedelta, os
import yaml

class Config(object):
    stream = open(os.getcwd() + "/config.yml", 'r')
    config = yaml.load(stream, Loader=yaml.FullLoader)

    SECRET_KEY = config["secret_key"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config["database"]["db"]}'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
