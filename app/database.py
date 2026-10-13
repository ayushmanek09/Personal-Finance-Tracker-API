
import sqlite3

DATABASE = "finance.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount > 0),
            category TEXT NOT NULL,
            transaction_type TEXT NOT NULL
                CHECK (transaction_type IN ('income', 'expense')),
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
