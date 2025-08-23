from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import blueprints
from src.routes.ai_agent import ai_agent_bp

app = Flask(__name__, static_folder=\"./static\")

CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(ai_agent_bp, url_prefix=\"/api\")

@app.route(\"/\")
@app.route(\"/<path:path>\")
def serve_frontend(path=\"index.html\"):
    return send_from_directory(app.static_folder, path)

if __name__ == \"__main__\":
    app.run(debug=True, host=\"0.0.0.0\", port=5000)


