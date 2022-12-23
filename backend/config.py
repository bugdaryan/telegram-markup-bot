import os
from dotenv import load_dotenv
from abc import ABC

dotenv_path = '.env'
load_dotenv(dotenv_path)


class Config(ABC):
    ENV = os.getenv('ENV')
    PORT = os.getenv('PORT')

    if ENV == 'development':
        DEBUG = True
        DATABASE_URL = os.getenv('LOCAL_DB')

    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    SECRET_KEY = os.getenv('BCRYPT_SECRET_KEY')