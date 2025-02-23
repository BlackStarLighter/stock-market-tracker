from flask import Blueprint, jsonify

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "API Gateway is running"}), 200

def init_routes(app):
    """Register routes with the Flask app."""
    app.register_blueprint(api, url_prefix="/api")
