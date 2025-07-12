from flask import jsonify
import traceback
from src.infrastructure.repositories.mongodb.log_repository import LogRepository

log_repository = LogRepository()

def handle_client_error(e, origen, status_code):
    print(traceback.format_exc())
    log_repository.create_log(
        origen=origen,
        type_log="Advertencia",
        status_code=status_code,
        details=str(e)
    )

    return (
        jsonify({"message": f"{e}"}),
        400,
    )


def handle_general_error(e, origen, status_code=500):
    print(traceback.format_exc())

    log_repository.create_log(
        origen=origen,
        type_log="Error no controlado",
        details=str(e),
        status_code=status_code,
    )

    return (
        jsonify({
            "message": f"Ha ocurrido un error inesperado al {origen}. Por favor, contacta al administrador"
        }),
        500,
    )
