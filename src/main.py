import os
import datetime

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import jwt_required, JWTManager
from src.application.auth_service import Auth
from src.middleware.hasRole import has_role

app = Flask(__name__)
app.config["CHARSET"] = "UTF-8"
configurations = os.environ

app.config["JWT_SECRET_KEY"] = configurations.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=6)

jwt = JWTManager(app)
auth = Auth(app)


CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "True"}})

@app.route("/")
def index():
    return "Testing, Flask!"

@app.route("/auth/login", methods=["POST"])
def login():
    return auth.login()

@app.route("/auth/change-user-password/<user_id>", methods=["PUT"])
@jwt_required()
@has_role(["Superadmin"])
def reset_password(user_id):
    return auth.reset_password(user_id)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)