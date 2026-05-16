# Integrates with Google Gemini 2.5 Flash to convert natural language questions into SQL queries.
# Handles prompt construction, API calls, and defensive parsing of the returned SQL output.

from google import genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, USER_PROMPT
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_sql(question: str, schema: str) -> str:
    system = SYSTEM_PROMPT.format(schema=schema)
    user = USER_PROMPT.format(question=question)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={"system_instruction": system},
        contents=user
    )

    sql = response.text.strip()

    # Strip markdown code fences
    if "```" in sql:
        sql = sql.split("```")[1]  # get content between first pair of backticks
        # Remove language identifier like 'sql' if present
        if sql.lower().startswith("sql"):
            sql = sql[3:]
    
    return sql.strip()

# if __name__ == "__main__":
#     from db import get_schema
#     schema = get_schema()
#     question = "How many customers are there per country?"
#     sql = generate_sql(question, schema)
#     print(sql)