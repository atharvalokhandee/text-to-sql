import os
import sqlite3
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def get_schema(db_path: str) -> str:
    """Extract table names, columns, and types from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    schema_parts = []
    for table in tables:
        cursor = conn.execute(f"PRAGMA table_info({table})")
        cols = cursor.fetchall()
        col_defs = ", ".join([f"{c[1]} {c[2]}" for c in cols])
        schema_parts.append(f"Table: {table} ({col_defs})")

    conn.close()
    return "\n".join(schema_parts)


def build_prompt(schema: str, user_question: str) -> str:
    """Construct the prompt injected with schema and rules."""
    return f"""You are an expert SQL assistant. Generate a single valid SQLite query for the question below.

Rules:
- Return ONLY the raw SQL query, no explanation, no markdown, no code blocks
- Use only SELECT statements — never INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE
- Use table and column names exactly as shown in the schema
- If the question cannot be answered with the given schema, return: ERROR: <reason>

Schema:
{schema}

Examples:
Q: How many customers are from India?
A: SELECT COUNT(*) FROM customers WHERE country = 'India';

Q: What is the total revenue?
A: SELECT SUM(amount) FROM orders;

Q: {user_question}
A:"""


def call_llm(prompt: str) -> str:
    """Send prompt to Groq and return the raw response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def text_to_sql_pipeline(question: str, db_path: str) -> dict:
    """
    Full pipeline: question → schema → prompt → SQL → validate → execute → explain.
    Returns a dict with keys: sql, result, explanation, error
    """
    schema = get_schema(db_path)
    prompt = build_prompt(schema, question)
    sql = call_llm(prompt)

    if sql.startswith("ERROR:"):
        return {"sql": None, "result": None, "explanation": None, "error": sql}

    from app.validator import validate_sql
    valid, message = validate_sql(sql)

    if not valid:
        return {"sql": sql, "result": None, "explanation": None, "error": message}

    from app.formatter import execute_and_explain
    result, explanation = execute_and_explain(sql, db_path, question)

    return {
        "sql": sql,
        "result": result,
        "explanation": explanation,
        "error": None
    }