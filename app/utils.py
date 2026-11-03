"""SQLite database paths, connection helpers, and SQL script operations."""

import sqlite3
from contextlib import closing
from pathlib import Path

# --- Database files and paths ---

BASE_DIR = Path(__file__).parent / "db"

DATABASE_PATH = BASE_DIR / "db.sqlite"
SCHEMA_PATH   = BASE_DIR / "schema.sql"
SEED_PATH     = BASE_DIR / "seed.sql"


# --- Database helper functions ---

def get_connection():
    """Open a database connection that returns rows addressable by column name."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def execute(sql, *params):
    """Runs an INSERT, UPDATE or DELETE and saves the change."""
    with closing(get_connection()) as connection:
        with connection:
            connection.execute(sql, params)


def fetch_one(sql, *params):
    """Runs a SELECT and returns the first row, or None if nothing matched."""
    with closing(get_connection()) as connection:
        return connection.execute(sql, params).fetchone()


def fetch_all(sql, *params):
    """Runs a SELECT and returns a list of all matching rows."""
    with closing(get_connection()) as connection:
        return connection.execute(sql, params).fetchall()


def run_sql_file(path):
    """Execute the SQL script stored at path within a database transaction."""
    script = path.read_text(encoding="utf-8")   # utf-8 stops Windows from guessing the wrong encoding
    with closing(get_connection()) as connection:
        with connection:
            connection.executescript(script)


def create_database():
    """Recreate the database using the schema SQL file."""
    DATABASE_PATH.unlink(missing_ok=True)
    run_sql_file(SCHEMA_PATH)


def seed_database():
    """Reset the database and populate using the seed SQL file."""
    create_database()
    run_sql_file(SEED_PATH)
