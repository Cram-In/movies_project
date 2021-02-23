from flask import make_response, jsonify
from config import app


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found", "status_code": 404, "error": error}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request", "status_code": 400, "error": error}), 400)
