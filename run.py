from flask import Flask

from app import create_app
from app.config import FlaskConfig

if __name__ == "__main__":
    app = create_app(FlaskConfig)

    app.run()
