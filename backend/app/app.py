from flask import Flask
from app.api.upload import upload_bp
from app.api.endpoints import chat_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
