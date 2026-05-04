# 🗄️ Text-to-SQL Engine

Convert plain English questions into SQL queries instantly — powered by **Groq (LLaMA 3.3 70B)**, with automatic SQL validation and natural language result explanation.

> "Who are the top 5 customers by revenue?" → generates SQL → runs it → explains the answer in plain English.

---

## 🎯 Features

- **Natural language to SQL** — Ask any question about your database in plain English
- **Groq-powered inference** — Ultra-fast LLaMA 3.3 70B for accurate SQL generation
- **Schema-aware** — Automatically reads your database structure and injects it into the prompt
- **SQL validation & safety** — Blocks all write operations (DROP, DELETE, UPDATE, INSERT) before execution
- **Plain English answers** — Results are explained naturally, not just shown as raw data
- **Clean Streamlit UI** — Simple web interface, no technical knowledge needed to use

---

## 🖥️ Demo

![App Screenshot](screenshot.png)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq API (LLaMA 3.3 70B) |
| SQL Validation | sqlglot |
| Frontend | Streamlit |
| Database | SQLite |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
text-to-sql/
│
├── app/
│   ├── __init__.py
│   ├── pipeline.py       # Core pipeline: schema → prompt → LLM → SQL
│   ├── validator.py      # SQL parsing and safety checks
│   └── formatter.py      # Query execution and result explanation
│
├── data/
│   └── sample.db         # SQLite sample database (auto-generated)
│
├── scripts/
│   └── seed_db.py        # Creates and seeds the sample database
│
├── ui/
│   └── streamlit_app.py  # Streamlit frontend
│
├── tests/
│   └── test_pipeline.py  # Unit tests for validator
│
├── .env.example          # Environment variable template
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/atharvalokhandee/text-to-sql.git
cd text-to-sql
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Groq API key
```bash
cp .env.example .env
```
Open `.env` and add your key:
```
GROQ_API_KEY=gsk_your_key_here
```
Get a free API key at [console.groq.com](https://console.groq.com)

### 5. Seed the sample database
```bash
python scripts/seed_db.py
```

### 6. Run the app
```bash
streamlit run ui/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💬 Example Questions to Try

```
Who are the top 3 customers by total order value?
How many orders were placed in April 2024?
Which country has the most customers?
What is the average order amount?
List all customers who have placed more than one order.
```

---

## 🔒 Safety

All LLM-generated SQL is validated before execution:
- ✅ Only `SELECT` statements are allowed
- ❌ `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE` are all blocked
- ✅ SQL syntax is parsed with `sqlglot` before running

---

## 🚀 How It Works

```
User Question
     ↓
Schema Extraction    ← reads table/column structure from DB
     ↓
Prompt Construction  ← injects schema + rules + few-shot examples
     ↓
Groq LLM (LLaMA 3.3) ← generates SQL
     ↓
SQL Validation       ← blocks unsafe queries, checks syntax
     ↓
Execute on Database  ← runs read-only query
     ↓
Plain English Answer ← LLM narrates the result
```

---

## 📄 License

MIT License — feel free to use and modify for your own projects.

---

## 👤 Author

**Atharva Lokhande**
