"""
config.py - App-wide constants and settings.
Edit this file to customise categories, file paths, currency, etc.
"""

import os

# ── Storage ──────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "expenses.json")

# ── Categories ───────────────────────────────────────────
EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Rent",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Other",
]

INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Investment",
    "Gift",
    "Other Income",
]

# ── Groq AI (FREE) ────────────────────────────────────────
# Get your free key at https://console.groq.com (no credit card needed)
# Then run:  export GROQ_API_KEY="gsk_..."
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# LLaMA 3 70B — fast and free on Groq
AI_MODEL = "llama3-70b-8192"

# ── Currency ──────────────────────────────────────────────
CURRENCY_SYMBOL = "₹"
CURRENCY_CODE = "INR"
