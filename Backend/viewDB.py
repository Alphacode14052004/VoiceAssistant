import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            cart_details TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == '__main__':
    init_db()
