import awsgi
from src.main import app  # Import your Flask app


def handler(event, context):
    return awsgi.response(app, event, context)