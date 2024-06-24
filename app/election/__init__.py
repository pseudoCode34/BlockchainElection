from flask import Blueprint

blueprint = Blueprint('election', __name__)
from app.election import routes
