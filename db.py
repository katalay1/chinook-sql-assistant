# Handles all PostgreSQL interactions including connection management and query execution.
# Dynamically extracts the live database schema from information_schema to feed into the LLM prompt.

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def get_schema() -> str:
    """
    Dynamically pulls all table/column/type info from the Chinook DB
    and formats it as a readable string for the LLM prompt.
    """
    query = """
        SELECT 
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
    """
    
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group columns by table and format as readable text for the LLM
    schema_dict = {}
    for row in rows:
        table = row["table_name"]
        column = row["column_name"]
        dtype = row["data_type"]
        if table not in schema_dict:
            schema_dict[table] = []
        schema_dict[table].append(f"  {column} ({dtype})")

    schema_str = ""
    for table, columns in schema_dict.items():
        schema_str += f"Table: {table}\n"
        schema_str += "\n".join(columns)
        schema_str += "\n\n"

    return schema_str.strip()


def run_query(sql: str) -> tuple[list[dict], list[str]]:
    #print(f"DEBUG SQL: '{sql}'")
    cleaned = sql.strip().lower()
    cleaned = " ".join(cleaned.split())
    if not cleaned.startswith("select") and not cleaned.startswith("with"):
        raise ValueError("Only SELECT queries are allowed.")

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    col_names = [desc.name for desc in cursor.description]
    cursor.close()
    conn.close()

    # Convert RealDictRow objects to plain dicts
    return [dict(row) for row in rows], col_names

# if __name__ == "__main__":
#     print(get_schema())