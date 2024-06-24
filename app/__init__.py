import json
import os
from importlib import import_module

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from web3 import Web3

from app.config import FlaskConfig

blockchain_address = os.getenv("BLOCKCHAIN_ADDRESS")
web3 = Web3(Web3.HTTPProvider(blockchain_address))

with open(os.getenv("COMPILED_CONTRACT_FILE"), "r") as file:
    contract_json = json.load(file)
    abi = contract_json["abi"]  # fetch contract's abi
    address = contract_json["networks"]["5777"]["address"]

# Fetch deployed contract reference
contract = web3.eth.contract(address=address, abi=abi)

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def init_flask_extensions(app):
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "authentication.login"

    bcrypt.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'election', 'vote'):
        module = import_module(f'app.{module_name}.routes')
        app.register_blueprint(module.blueprint)


def create_app(config_class=FlaskConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_flask_extensions(app)

    register_blueprints(app)

    # @app.route('/test/')
    # def test_page():
    #     return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
