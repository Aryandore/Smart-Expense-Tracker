"""
Database models for Expense Tracker
"""

from datetime import datetime, date
from enum import Enum
import uuid

# db will be imported from app.py
db = None

def init_models(database):
    global db
    db = database
    
    # Define models inside the function to avoid db.Model being None at import time
    class TransactionType(Enum):
        EXPENSE = "expense"
        INCOME = "income"

    class Transaction(db.Model):
        __tablename__ = 'transactions'
        
        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        amount = db.Column(db.Float, nullable=False)
        transaction_type = db.Column(db.String(10), nullable=False)  # 'expense' or 'income'
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
        month = db.Column(db.String(7), nullable=False)  # YYYY-MM format
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
    
    # Store them globally so they can be imported
    globals()['Transaction'] = Transaction
    globals()['MonthlyBudget'] = MonthlyBudget
    globals()['TransactionType'] = TransactionType

# Create dummy classes that will be replaced
Transaction = None
MonthlyBudget = None
TransactionType = None
