from database.connection import get_connection


def init_db() -> None:
    """Create all tables if they don't exist."""
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                telegram_id   INTEGER PRIMARY KEY,
                username      TEXT,
                first_name    TEXT,
                country       TEXT,
                money         INTEGER  DEFAULT 5000000,
                gold          INTEGER  DEFAULT 1000,
                oil           INTEGER  DEFAULT 5000,
                food          INTEGER  DEFAULT 5000,
                population    INTEGER  DEFAULT 1000000,
                army_power    INTEGER  DEFAULT 100,
                technology    INTEGER  DEFAULT 1,
                diplomacy     TEXT     DEFAULT 'Neutral',
                join_date     TEXT,
                is_registered INTEGER  DEFAULT 0
            )
        """)
    conn.close()
