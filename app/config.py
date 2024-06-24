import os
import string
from random import random

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class FlaskConfig:
    SECRET_KEY = os.getenv('SECRET_KEY') or ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = os.getenv("DEBUG")
