# 💰 Smart Expense Tracker

A modern, full-stack web application for intelligent personal finance management. Track expenses and income with AI-powered financial insights powered by Groq API.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Flask](https://img.shields.io/badge/Flask-3.1.3-brightgreen) ![SQLite](https://img.shields.io/badge/SQLite-Lightweight%20DB-lightblue) ![License](https://img.shields.io/badge/License-MIT-green)

Live Link :- https://smart-expense-tracker-1-rpyd.onrender.com/

## ✨ Features

- **📊 Dashboard** - Real-time financial overview with income, expenses, and savings
- **💳 Transaction Management** - Create, read, update, and delete transactions
- **🔍 Smart Search** - Filter transactions by category, description, and date
- **📈 Monthly Analytics** - Comprehensive spending breakdown by category
- **🤖 AI Insights** - AI-powered financial recommendations using Groq API (Llama 3.3)
- **📥 Data Export** - Export transactions to CSV format
- **💾 Persistent Storage** - SQLite database for reliable data persistence
- **🎨 Beautiful UI** - Modern gradient design with responsive layout
- **⚡ Real-time Updates** - Instant dashboard calculations

## 🛠️ Tech Stack

### Backend
- **Flask 3.1.3** - Lightweight web framework
- **SQLAlchemy 2.0.50** - ORM for database operations
- **Flask-CORS** - Cross-origin request handling
- **Groq API** - AI-powered financial analysis

### Frontend
- **HTML5 & CSS3** - Modern, responsive design
- **Vanilla JavaScript** - No build tools required
- **Fetch API** - Asynchronous API communication

### Database
- **SQLite** - Lightweight file-based database

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- Pip package manager
- Groq API key (free at https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd Expence_tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here
   GROQ_API_KEY=your-groq-api-key-here
   DATABASE_URL=sqlite:///expense_tracker.db
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Adding a Transaction
1. Fill in the amount (₹)
2. Select transaction type (Expense/Income)
3. Choose category
4. Add optional description
5. Click "Add Transaction"

### Viewing Analytics
- **Transactions Tab** - View all transactions with search
- **Summary Tab** - Monthly breakdown and category analysis
- **AI Insights Tab** - Get AI-powered financial recommendations

### Exporting Data
- Click "📥 Export to CSV" to download all transactions

## 🔌 API Endpoints

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/<id>` - Update transaction
- `DELETE /api/transactions/<id>` - Delete transaction
- `GET /api/transactions/<id>` - Get specific transaction

### Analytics
- `GET /api/summary?month=2026-06` - Monthly summary
- `GET /api/statistics` - Overall statistics with 6-month history
- `GET /api/insights?month=2026-06` - AI-powered financial insights

### Utilities
- `GET /api/categories` - Available categories
- `GET /api/export/csv` - Export transactions to CSV
- `GET /health` - API health check

## 📊 Database Schema

### Transaction Model
```json
{
  "id": "UUID",
  "amount": "float",
  "type": "expense|income",
  "category": "string",
  "description": "string",
  "date": "YYYY-MM-DD",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Categories
- **Expenses**: Food, Transport, Rent, Utilities, Entertainment, Healthcare, Shopping, Education, Other
- **Income**: Salary, Freelance, Investment, Bonus, Other

## 🚢 Deployment



## 🔐 Security Considerations

- Never commit `.env` file with sensitive keys
- Use strong `SECRET_KEY` in production
- Enable HTTPS in production
- Validate all user inputs on backend
- Use environment variables for configuration
- Keep dependencies updated

## 📝 Configuration

### Production Settings
```python
# .env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=production-secret-key-min-32-chars
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=sqlite:///expense_tracker.db
```

## 🐛 Troubleshooting

### Issue: "Groq API Key not found"
**Solution**: Ensure `.env` file is created with valid `GROQ_API_KEY`

### Issue: "Database locked"
**Solution**: Close other instances of the application and restart

### Issue: CORS errors
**Solution**: Ensure Flask-CORS is properly configured (already done in app.py)

### Issue: AI Insights not working
**Solution**: Verify Groq API key is valid and you have API quota

## 📁 Project Structure

```
Expence_tracker/
├── backend/
│   ├── __init__.py
│   ├── app.py              # Flask app factory & models
│   └── routes.py           # API endpoints
├── frontend/
│   └── index.html          # Single-page application
├── config.py               # Configuration
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 📦 Requirements

```
flask==3.1.3
flask-cors==6.0.5
flask-sqlalchemy==3.1.1
python-dotenv==1.2.2
requests==2.34.2
groq==1.4.0
sqlalchemy==2.0.50
```

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🎯 Roadmap

- [ ] User authentication & multi-user support
- [ ] Recurring transactions
- [ ] Budget limits with alerts
- [ ] Mobile app (React Native)
- [ ] Data visualization charts
- [ ] Multi-currency support
- [ ] Receipt scanning (OCR)
- [ ] Export to other formats (PDF, Excel)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@expensetracker.com
- Discord: https://discord.gg/expensetracker

## 🙏 Acknowledgments

- Groq API for AI-powered insights
- Flask community for excellent framework
- SQLAlchemy for ORM excellence

---

**Made with ❤️ for smarter financial management**

🚀 **[Visit Live Demo](https://expensetracker.herokuapp.com)** | 📚 **[Read Documentation](https://github.com/yourusername/expense-tracker/wiki)** | 💬 **[Join Community](https://discord.gg/expensetracker)**
    Food             ₹8,500.00   26.2%  █████
    Transport        ₹4,500.00   13.8%  ██
    Entertainment    ₹3,200.00    9.8%  █
    Utilities        ₹2,800.00    8.6%  █
```

### AI Insights Output
```
🧠 AI FINANCIAL INSIGHTS
==================================================
• Your finances look solid — you're saving ~35% of your income, which is excellent.
• Food spending at 26% of expenses is on the higher end. Consider meal prepping
  2-3 days a week to cut this by ₹1,500–₹2,000/month.
• Entertainment has crept up month-over-month. Setting a monthly cap of ₹2,500
  would give you an extra ₹700 in savings.
• You're building a healthy buffer — keep it up and consider an emergency fund
  of 3-6 months of expenses (around ₹1,00,000).
==================================================
```

---

## ⚙️ Configuration

Edit `config.py` to customise:

| Setting | Default | Description |
|---|---|---|
| `EXPENSE_CATEGORIES` | Food, Rent, etc. | Add/remove expense categories |
| `INCOME_CATEGORIES` | Salary, Freelance, etc. | Add/remove income categories |
| `CURRENCY_SYMBOL` | ₹ | Change to $, €, £, etc. |
| `AI_MODEL` | claude-sonnet-4-20250514 | Anthropic model to use |

---

## 🗄️ Data Storage

All transactions are stored locally in `data/expenses.json` as a simple JSON array.
No database, no cloud, no account required.

```json
[
  {
    "id": "a1b2c3d4",
    "amount": 450.00,
    "type": "expense",
    "category": "Food",
    "description": "Grocery shopping",
    "date": "2025-06-15"
  }
]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Storage | JSON (stdlib) |
| AI | Groq API — LLaMA 3 70B (urllib) |
| Export | csv (stdlib) |
| UI | Terminal / CLI |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built as part of a Python Development Internship assignment.*
