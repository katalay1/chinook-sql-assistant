# 🎵 Chinook SQL Assistant

A natural language to SQL interface powered by **Google Gemini** and **PostgreSQL**. Ask questions about the Chinook music store database in plain English — get back SQL queries and results instantly.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?logo=google)

---

## 📌 Overview

This app translates natural language questions into valid PostgreSQL queries using Google Gemini 2.5 Flash. It dynamically extracts the live database schema and injects it into the prompt — so the LLM always has accurate, up-to-date context about the data it's querying.

**Example questions you can ask:**
- *"Who are the top 5 artists by number of tracks?"*
- *"What are total sales by genre?"*
- *"Which customers have spent the most money?"*
- *"List all albums by aerosmith"*

---

## 🏗️ Architecture

```
User Question (natural language)
        ↓
[Streamlit UI]
        ↓
[Schema Extractor] ← queries information_schema from PostgreSQL
        ↓
[Prompt Builder]  ← injects schema + question into system prompt
        ↓
[Gemini 2.5 Flash] ← returns a clean SQL query
        ↓
[SQL Executor]    ← runs query safely (SELECT only)
        ↓
[Streamlit UI]    ← displays generated SQL + results table
```

---

## 📁 Project Structure

```
chinook-sql-assistant/
├── app.py           # Streamlit UI — ties everything together
├── db.py            # PostgreSQL connection, schema extractor, query runner
├── llm.py           # Gemini API integration and SQL generation
├── prompts.py       # System and user prompt templates
├── requirements.txt
├── .env.example     # Environment variable template
└── .gitignore
```

---

## ⚙️ Key Design Decisions

**Dynamic schema injection** — Rather than hardcoding table definitions, the app queries `information_schema` at runtime to pull the live schema. This makes it portable to any PostgreSQL database, not just Chinook.

**Read-only safety guard** — The query executor rejects any statement that doesn't begin with `SELECT`, preventing accidental data modification even if the LLM hallucinates a destructive query.

**Schema caching** — The schema is fetched once per session using `@st.cache_resource`, avoiding redundant database round-trips on every interaction.

**Prompt engineering** — The system prompt explicitly instructs Gemini to return raw SQL only (no markdown, no explanation), with a defensive stripping step in case it doesn't comply.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL with the [Chinook database](https://github.com/lerocha/chinook-database) loaded
- A [Google Gemini API key](https://aistudio.google.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/katalay1/chinook-sql-assistant.git
cd chinook-sql-assistant

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env` with your credentials:

```
GEMINI_API_KEY=your_gemini_api_key_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=chinook
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🗄️ About the Chinook Database

Chinook is an open-source sample database modeled after a digital music store (think iTunes). It contains 11 tables including artists, albums, tracks, customers, invoices, and employees — rich enough to support complex multi-table queries.

| Table | Description |
|---|---|
| Artist | Music artists |
| Album | Albums per artist |
| Track | Individual tracks per album |
| Genre | Music genres |
| Customer | Store customers |
| Invoice | Customer purchases |
| InvoiceLine | Line items per invoice |
| Employee | Store employees |
| Playlist | User playlists |
| MediaType | Audio formats |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| Backend | Python |
| Database | PostgreSQL |
| UI | Streamlit |
| DB Driver | psycopg2 |
| Sample Data | Chinook Database |

---

## 📄 License

This project uses the [Chinook Database](https://github.com/lerocha/chinook-database), which is released under the MIT License.

---

## 👤 Author

**Kerem Atalay**  
[GitHub](https://github.com/katalay1)
