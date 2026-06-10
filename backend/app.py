"""
Flask Backend for Expense Tracker Web Application
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import sys
from datetime import datetime, date
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

db = SQLAlchemy()

# Define models at module level so they can be imported
class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': round(self.amount, 2),
            'type': self.transaction_type,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

class MonthlyBudget(db.Model):
    __tablename__ = 'monthly_budgets'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    month = db.Column(db.String(7), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    limit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'month': self.month,
            'category': self.category,
            'limit': round(self.limit, 2),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

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
    print("🚀 Starting Flask backend on http://localhost:5000")
    print("📁 Database: expense_tracker.db")
    app.run(debug=True, host='0.0.0.0', port=5000)
