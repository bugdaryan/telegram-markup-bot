import os
from dotenv import load_dotenv
from abc import ABC

dotenv_path = '.env'
load_dotenv(dotenv_path)


class Config(ABC):
    TELEGRAM_SECRET_KEY = os.getenv('TELEGRAM_SECRET_KEY')
    APP_BASE_URL = os.getenv('APP_BASE_URL')