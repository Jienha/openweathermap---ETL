
import sqlite3


def load_to_sqlite(db_path="db/flow_openweathermap.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    query = "SELECT * FROM meteo_table"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    load_to_sqlite()

