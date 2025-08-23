from flask import Blueprint, jsonify, request

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    question = data.get('question')
    # Replace with your AI logic
    response = {"answer": f"Received: {question}"}
    return jsonify(response)
