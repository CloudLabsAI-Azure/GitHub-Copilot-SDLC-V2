"""Jobs blueprint."""
from flask import Blueprint

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

from app.blueprints.jobs import routes
