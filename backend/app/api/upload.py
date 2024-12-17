from flask import Blueprint, request, jsonify
from app.core.vector_store import VectorStore
from app.core.llm_pipeline import process_query
import os

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_document():
    """
    Upload a document and process it into the vector store.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file temporarily
    file_path = os.path.join('temp', file.filename)
    file.save(file_path)

    # Process the file into the vector store
    vector_store = VectorStore()
    vector_store.add_document(file_path)

    # Clean up the temporary file
    os.remove(file_path)

    return jsonify({'message': 'File uploaded and processed successfully'}), 200
