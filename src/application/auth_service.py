import os
import json
import datetime
import requests
import traceback

from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from bson import ObjectId, json_util
from flask import jsonify, request, Flask
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from src.infrastructure.repositories.mongodb.log_repository import LogRepository
from src.infrastructure.repositories.mongodb.user_repository import UserRepository
from src.domain.auth_schema import (
    LoginSchema,
    ResetPasswordSchema
)

from src.infrastructure.utils.handler_error import (
    handle_general_error,
    handle_client_error
)

load_dotenv()
app = Flask(__name__)

bcrypt = Bcrypt(app)
log_repository = LogRepository()
user_repository = UserRepository()

class Auth:
    def __init__(self, app):
        self.app = app
        
    def login(self):
        origen = "Login"
        try:
            data = request.get_json()
            schema = LoginSchema()
            schema.load(data)
            
            user = user_repository.get(email=data.get("email", ""))
            
            if not user:
                return handle_client_error("Usuario no encontrado", origen, 404)

            if user.get("is_active") != True:
                return handle_client_error("Acceso denegado: usuario inactivo", origen, 403)
            
            if not bcrypt.check_password_hash(user.get("password"), data.get("password", None)):
                return handle_client_error("Contraseña incorrecta", origen, 401)
            
            additional_claims = {"roles": user.get("roles")}

            token = create_access_token(
                identity=user.get("email"),
                additional_claims=additional_claims,
                expires_delta=datetime.timedelta(hours=2)
            )
            
            user.pop("password", None)

            log_repository.create_log(origen, "Exitoso", 200, user_id=user.get("_id"))

            response = {
                "data": {"token": token, "user": user},
                "message": "Successfully logged in"
            }
            return json.loads(json_util.dumps(response)), 200
        
        except ValidationError as e:
            return json.loads(json_util.dumps({
                "message": "Datos inválidos",
                "errors": e.messages
            })), 400

        except ValueError as e:
            return json.loads(json_util.dumps({
                "message": str(e)
            })), 400

        except Exception as e:
            return handle_general_error(e, origen)
    
    def reset_password(self, user_id):
        origen = "Reset Password"
        try:
            data = request.get_json()
            schema = ResetPasswordSchema()
            schema.load(data)

            password_hash = bcrypt.generate_password_hash(data.get("password", "")).decode("utf-8")

            result = user_repository.update(
                ObjectId(user_id),
                {"$set": {"password": password_hash}}
            )
            
            log_repository.create_log(origen, "Exitoso", 200, user_id=ObjectId(user_id))

            response = {
                "message": "Contraseña actualizada correctamente"
            }
            return json.loads(json_util.dumps(response)), 200

        except ValidationError as e:
            return json.loads(json_util.dumps({
                "message": "Datos inválidos",
                "errors": e.messages
            })), 400

        except ValueError as e:
            return json.loads(json_util.dumps({
                "message": str(e)
            })), 400

        except Exception as e:
            return handle_general_error(e, origen)