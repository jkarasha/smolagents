import sqlite3
from pathlib import Path

def init_db(db_path: str = 'data/history.db'):
    '''Initialize the SQLite database and create the stock_rankings table.'''
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_rankings (
                date TEXT,
                ticker TEXT,
                earnings_yield REAL,
                roc REAL,
                rank INTEGER
            );
        ''')
        conn.commit()
