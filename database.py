import sqlite3
from datetime import datetime


from datetime import date

DB_PATH = 'caltrack.db'

def get_db():
    connect = sqlite3.connect(DB_PATH)
    connect.row_factory = sqlite3.Row
    return connect

def init_db():
    con = get_db()
    con.execute('''
    CREATE TABLE IF NOT EXISTS diet_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        food_name TEXT NOT NULL,
        calories REAL NOT NULL,
        protein REAL NOT NULL,
        fat REAL NOT NULL,
        carbs REAL NOT NULL,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    con.commit()
    con.close()

def insert_item(cals, protein, fat, carbs, name, date):
    con = get_db()
    con.execute('''
    INSERT INTO diet_history (date, food_name, calories, protein, fat, carbs)
    VALUES (?, ?, ?, ?, ?, ?)''', (date, name, cals, protein, fat, carbs))
    con.commit()
    con.close()

def get_daily_entries(date):
    con = get_db()
    cursor = con.execute('''
    SELECT id, date, food_name, calories, protein, fat, carbs, logged_at
    FROM diet_history
    WHERE date = ?
    ORDER BY logged_at ASC''', (date,))
    entries = cursor.fetchall()
    con.close()
    return entries

def get_daily_totals(date):
    con = get_db()
    cursor = con.execute('''
    SELECT COALESCE(SUM(calories), 0) AS total_calories,
           COALESCE(SUM(protein), 0) AS total_protein,
           COALESCE(SUM(fat), 0) AS total_fat,
           COALESCE(SUM(carbs), 0) AS total_carbs
    FROM diet_history
    WHERE date = ?''', (date,))
    totals = cursor.fetchone()
    con.close()
    return totals

if __name__ == '__main__':
    init_db()
    print(dict(get_daily_totals(date.today().isoformat())))
