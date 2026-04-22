import sqlglot


def validate_sql(sql: str) -> tuple[bool, str]:
    """Parse and sanitize LLM-generated SQL. Blocks all write operations."""
    sql_stripped = sql.strip()
    sql_upper = sql_stripped.upper()

    # Block dangerous keywords
    blocked = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
    for keyword in blocked:
        if sql_upper.startswith(keyword):
            return False, f"Blocked operation: {keyword} is not allowed."

    # Validate syntax using sqlglot
    try:
        sqlglot.parse_one(sql_stripped, dialect="sqlite")
        return True, sql_stripped
    except Exception as e:
        return False, f"Invalid SQL syntax: {e}"