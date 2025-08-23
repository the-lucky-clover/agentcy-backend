from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../agentcy-one/build', static_url_path='/')
CORS(app)

# API routes
from ai_agent import ai_bp
app.register_blueprint(ai_bp, url_prefix='/api')

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and (app.static_folder / path).exists():
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
