# Text-to-SQL Engine

Ask questions about your database in plain English. Powered by **Groq** (LLaMA 3.3 70B) + SQLite + Streamlit.

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/text-to-sql.git
cd text-to-sql

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env            # add your Groq API key inside .env

python scripts/seed_db.py
```

## Run

```bash
streamlit run ui/streamlit_app.py
```

## Stack
- [Groq](https://console.groq.com) — LLaMA 3.3 70B inference
- sqlglot — SQL parsing & validation
- Streamlit — frontend UI
- SQLite — sample database
