from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from backend.models import db

def create_app():
    app = Flask(__name__)
    
    # Use absolute path for database
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'expense_tracker.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Register routes
        from backend import routes
        app.register_blueprint(routes.api_bp)
    
    # Serve static files (frontend)
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    
    @app.route('/')
    def index():
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory(frontend_path, path)
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'message': 'Backend is running'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)