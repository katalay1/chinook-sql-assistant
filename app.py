# Streamlit UI with schema browser, example questions, and results display

import streamlit as st
from db import get_schema, run_query
from llm import generate_sql

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Chinook SQL Assistant",
    page_icon="🎵",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────────────
st.title("🎵 Chinook SQL Assistant")
st.markdown("Ask questions about the Chinook music store database in plain English.")

# ── Load schema once and cache it ─────────────────────────────
@st.cache_resource
def load_schema():
    return get_schema()

schema = load_schema()

# ── Sidebar — schema browser ───────────────────────────────────
with st.sidebar:
    st.header("📋 Database Schema")
    st.markdown("Expand a table to see its columns:")
    for block in schema.split("\n\n"):
        lines = block.strip().split("\n")
        if lines:
            table_name = lines[0].replace("Table: ", "")
            with st.expander(table_name):
                for col in lines[1:]:
                    st.markdown(f"`{col.strip()}`")

# ── Example questions ──────────────────────────────────────────
st.markdown("### 💡 Try an example")
examples = [
    "How many customers are there per country?",
    "Who are the top 5 artists by number of tracks?",
    "What are the total sales by genre?",
    "Which customers have spent the most money?",
    "List all albums by AC/DC",
]

cols = st.columns(len(examples))
for i, example in enumerate(examples):
    if cols[i].button(example, use_container_width=True):
        st.session_state.question = example

# ── Question input ─────────────────────────────────────────────
st.markdown("### 🔍 Ask your question")
question = st.text_input(
    label="Question",
    placeholder="e.g. What are the top 10 selling tracks?",
    key="question",
    label_visibility="collapsed"
)

# ── Main logic ─────────────────────────────────────────────────
if question:
    with st.spinner("Generating SQL..."):
        try:
            sql = generate_sql(question, schema)
        except Exception as e:
            st.error(f"Gemini error: {e}")
            st.stop()

    st.markdown("### 🧠 Generated SQL")
    st.code(sql, language="sql")

    with st.spinner("Running query..."):
        try:
            rows, columns = run_query(sql)
        except ValueError as e:
            st.error(f"Safety block: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Database error: {e}")
            st.stop()

    st.markdown(f"### 📊 Results — {len(rows)} rows returned")
    if rows:
        st.dataframe(rows, use_container_width=True)
    else:
        st.info("Query ran successfully but returned no results.")