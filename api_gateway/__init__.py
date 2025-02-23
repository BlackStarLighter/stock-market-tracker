import os
from flask import Flask
from .routes import init_routes

def create_app():
    """Initialize and configure the Flask app for the API Gateway."""
    app = Flask(__name__)

    # Load configurations (if any)
    app.config.from_object(os.getenv("FLASK_CONFIG", "config.default"))

    # Initialize routes
    init_routes(app)

    return app

# If running directly, create and run the app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
