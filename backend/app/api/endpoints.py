from flask import Blueprint, request, jsonify
from app.core.llm_pipeline import process_query

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Process a chat query and return a response.
    """
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    response = process_query(query)
    return jsonify({'response': response}), 200
