from flask import Flask
from flask_cors import CORS
from app.routes import init_routes

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Initialize routes, database, and AI service
    init_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    from app.config import Config
    app.run(host='0.0.0.0', port=Config.PORT, debug=True)
