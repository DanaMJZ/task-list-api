from flask import abort, make_response
from app.db import db
# Wave1
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = db.session.get(cls, model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model
