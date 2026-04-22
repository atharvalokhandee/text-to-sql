import sqlite3
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def execute_and_explain(sql: str, db_path: str, question: str) -> tuple:
    """Execute SQL and generate a plain English explanation of the result."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description] if cursor.description else []
        conn.close()

        result = {"columns": columns, "rows": rows[:20]}  # cap at 20 rows

        # Ask Groq to narrate the result
        explanation_prompt = f"""
The user asked: "{question}"
The SQL query used was: {sql}
The result columns are: {columns}
The result rows are: {rows[:10]}

Write a clear, friendly 1-2 sentence answer summarising the data result.
Do not mention SQL. Just answer the question naturally.
"""
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": explanation_prompt}],
            temperature=0.3,
            max_tokens=150,
        )
        explanation = response.choices[0].message.content.strip()
        return result, explanation

    except Exception as e:
        return None, f"Query execution failed: {e}"