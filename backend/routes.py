"""
API Routes for Expense Tracker
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, date as date_cls, timedelta
from sqlalchemy import func
import os
import sys
import csv
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import db, Transaction, MonthlyBudget
import config

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ========== Transactions API ==========

@api_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions with optional filtering"""
    try:
        category = request.args.get('category')
        month = request.args.get('month')
        txn_type = request.args.get('type')
        
        query = Transaction.query
        
        if category:
            query = query.filter_by(category=category)
        if txn_type:
            query = query.filter_by(transaction_type=txn_type)
        if month:
            query = query.filter(func.strftime('%Y-%m', Transaction.date) == month)
        
        transactions = query.order_by(Transaction.date.desc()).all()
        return jsonify([t.to_dict() for t in transactions]), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error: {str(e)}'}), 500

@api_bp.route('/transactions/<txn_id>', methods=['GET'])
def get_transaction(txn_id):
    """Get a specific transaction"""
    try:
        txn = Transaction.query.get(txn_id)
        if not txn:
            return jsonify({'error': 'Transaction not found'}), 404
        return jsonify(txn.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.json
        
        if not data.get('amount') or data['amount'] <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
        if data.get('type') not in ['expense', 'income']:
            return jsonify({'error': 'Invalid transaction type'}), 400
        if not data.get('category'):
            return jsonify({'error': 'Category is required'}), 400
        
        txn_date = data.get('date')
        if txn_date:
            try:
                txn_date = datetime.fromisoformat(txn_date).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        else:
            txn_date = date_cls.today()
        
        transaction = Transaction(
            amount=float(data['amount']),
            transaction_type=data['type'],
            category=data['category'],
            description=data.get('description', ''),
            date=txn_date
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/transactions/<txn_id>', methods=['PUT'])
def update_transaction(txn_id):
    """Update a transaction"""
    try:
        txn = Transaction.query.get(txn_id)
        if not txn:
            return jsonify({'error': 'Transaction not found'}), 404
        
        data = request.json
        
        if 'amount' in data and data['amount'] > 0:
            txn.amount = float(data['amount'])
        if 'category' in data:
            txn.category = data['category']
        if 'description' in data:
            txn.description = data['description']
        if 'date' in data:
            try:
                txn.date = datetime.fromisoformat(data['date']).date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        db.session.commit()
        return jsonify(txn.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/transactions/<txn_id>', methods=['DELETE'])
def delete_transaction(txn_id):
    """Delete a transaction"""
    try:
        txn = Transaction.query.get(txn_id)
        if not txn:
            return jsonify({'error': 'Transaction not found'}), 404
        
        db.session.delete(txn)
        db.session.commit()
        
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ========== Summary & Analytics API ==========

@api_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get monthly summary with totals"""
    try:
        month = request.args.get('month')
        if not month:
            now = date_cls.today()
            month = now.strftime('%Y-%m')
        
        income = db.session.query(func.sum(Transaction.amount)).filter(
            func.strftime('%Y-%m', Transaction.date) == month,
            Transaction.transaction_type == 'income'
        ).scalar() or 0
        
        expenses = db.session.query(func.sum(Transaction.amount)).filter(
            func.strftime('%Y-%m', Transaction.date) == month,
            Transaction.transaction_type == 'expense'
        ).scalar() or 0
        
        category_breakdown = db.session.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            func.strftime('%Y-%m', Transaction.date) == month,
            Transaction.transaction_type == 'expense'
        ).group_by(Transaction.category).all()
        
        return jsonify({
            'month': month,
            'total_income': round(income, 2),
            'total_expenses': round(expenses, 2),
            'net_savings': round(income - expenses, 2),
            'category_breakdown': [
                {'category': cat, 'amount': round(total, 2)}
                for cat, total in category_breakdown
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics"""
    try:
        all_income = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.transaction_type == 'income'
        ).scalar() or 0
        
        all_expenses = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.transaction_type == 'expense'
        ).scalar() or 0
        
        total_transactions = Transaction.query.count()
        
        months_data = []
        for i in range(6):
            date_obj = date_cls.today() - timedelta(days=30*i)
            month_str = date_obj.strftime('%Y-%m')
            
            month_income = db.session.query(func.sum(Transaction.amount)).filter(
                func.strftime('%Y-%m', Transaction.date) == month_str,
                Transaction.transaction_type == 'income'
            ).scalar() or 0
            
            month_expenses = db.session.query(func.sum(Transaction.amount)).filter(
                func.strftime('%Y-%m', Transaction.date) == month_str,
                Transaction.transaction_type == 'expense'
            ).scalar() or 0
            
            months_data.insert(0, {
                'month': month_str,
                'income': round(month_income, 2),
                'expenses': round(month_expenses, 2)
            })
        
        return jsonify({
            'total_income': round(all_income, 2),
            'total_expenses': round(all_expenses, 2),
            'total_saved': round(all_income - all_expenses, 2),
            'total_transactions': total_transactions,
            'last_6_months': months_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== AI Insights API ==========

@api_bp.route('/insights', methods=['GET'])
def get_insights():
    """Get AI-powered financial insights"""
    try:
        month = request.args.get('month')
        if not month:
            now = date_cls.today()
            month = now.strftime('%Y-%m')
        
        transactions = Transaction.query.filter(
            func.strftime('%Y-%m', Transaction.date) == month
        ).all()
        
        if not transactions:
            return jsonify({'insights': 'No transactions for this month yet.'}), 200
        
        # Generate AI insights
        try:
            from groq import Groq
            
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return jsonify({'insights': 'AI insights not available. Please set GROQ_API_KEY environment variable.'}), 200
            
            client = Groq(api_key=api_key)
            
            total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
            total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            
            category_spending = {}
            for t in transactions:
                if t.transaction_type == 'expense':
                    category_spending[t.category] = category_spending.get(t.category, 0) + t.amount
            
            category_list = '\n'.join(f"- {cat}: ₹{amt:.2f}" for cat, amt in sorted(category_spending.items(), key=lambda x: x[1], reverse=True))
            
            prompt = f"""Analyze the following monthly financial data and provide personalized insights:

Total Income: ₹{total_income:.2f}
Total Expenses: ₹{total_expenses:.2f}
Net Savings: ₹{total_income - total_expenses:.2f}

Spending by Category:
{category_list}

Please provide:
1. A brief analysis of the spending patterns
2. 2-3 specific recommendations for saving money
3. Any concerning spending categories
4. Positive observations

Keep the response concise and actionable."""

            message = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            insights = message.choices[0].message.content
        except Exception as e:
            insights = f"AI insights generation failed: {str(e)}"
        
        return jsonify({'insights': insights, 'month': month}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ========== Categories API ==========

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    return jsonify({
        'expense_categories': config.EXPENSE_CATEGORIES,
        'income_categories': config.INCOME_CATEGORIES
    }), 200

# ========== Export API ==========

@api_bp.route('/export/csv', methods=['GET'])
def export_csv():
    """Export transactions to CSV"""
    try:
        month = request.args.get('month')
        if month:
            transactions = Transaction.query.filter(
                func.strftime('%Y-%m', Transaction.date) == month
            ).all()
        else:
            transactions = Transaction.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
        
        for t in transactions:
            writer.writerow([
                t.date.isoformat(),
                t.transaction_type.upper(),
                t.category,
                f"₹{t.amount:.2f}",
                t.description
            ])
        
        csv_content = output.getvalue()
        return csv_content, 200, {'Content-Disposition': 'attachment; filename=expenses.csv'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500
