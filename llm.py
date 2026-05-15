from google import genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT, USER_PROMPT
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_sql(question: str, schema: str) -> str:
    """
    Takes a natural language question and the DB schema,
    sends them to Gemini, and returns a SQL query string.
    """
    system = SYSTEM_PROMPT.format(schema=schema)
    user = USER_PROMPT.format(question=question)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={"system_instruction": system},
        contents=user
    )

    sql = response.text.strip()

    # Strip markdown code fences if Gemini returns them despite instructions
    if sql.startswith("```"):
        sql = sql.split("\n", 1)[-1]
        sql = sql.rsplit("```", 1)[0].strip()

    return sql

# if __name__ == "__main__":
#     from db import get_schema
#     schema = get_schema()
#     question = "How many customers are there per country?"
#     sql = generate_sql(question, schema)
#     print(sql)