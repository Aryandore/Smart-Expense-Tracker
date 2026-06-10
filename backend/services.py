"""
Business logic services for Expense Tracker
"""

import os
import csv
from io import StringIO
from groq import Groq
from datetime import date

def get_ai_insights(transactions):
    """Generate AI-powered financial insights using Groq"""
    try:
        api_key = os.getenv('GROQ_API_KEY', '')
        if not api_key:
            return "AI insights not available. Please set GROQ_API_KEY environment variable."
        
        client = Client(api_key=api_key)
        
        # Prepare transaction summary for AI
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        
        category_spending = {}
        for t in transactions:
            if t.transaction_type == 'expense':
                category_spending[t.category] = category_spending.get(t.category, 0) + t.amount
        
        prompt = f"""Analyze the following monthly financial data and provide personalized insights:

Total Income: ₹{total_income:.2f}
Total Expenses: ₹{total_expenses:.2f}
Net Savings: ₹{total_income - total_expenses:.2f}

Spending by Category:
{chr(10).join(f"- {cat}: ₹{amt:.2f}" for cat, amt in sorted(category_spending.items(), key=lambda x: x[1], reverse=True))}

Please provide:
1. A brief analysis of the spending patterns
2. 2-3 specific recommendations for saving money
3. Any concerning spending categories
4. Positive observations

Keep the response concise and actionable."""

        message = client.messages.create(
            model="llama3-70b-8192",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        return f"Could not generate AI insights: {str(e)}"

def export_to_csv(transactions):
    """Export transactions to CSV format"""
    try:
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])
        
        # Write transactions
        for t in transactions:
            writer.writerow([
                t.date.isoformat(),
                t.transaction_type.upper(),
                t.category,
                f"₹{t.amount:.2f}",
                t.description
            ])
        
        return output.getvalue()
    except Exception as e:
        raise Exception(f"Error exporting to CSV: {str(e)}")

def get_monthly_stats(transactions):
    """Calculate monthly statistics"""
    income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    
    return {
        'total_income': round(income, 2),
        'total_expenses': round(expenses, 2),
        'net_savings': round(income - expenses, 2),
        'transaction_count': len(transactions)
    }
