import sqlite3
import json


def check_symbol_exists(symbol):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM ARB WHERE TOKEN_SYMBOL = ?', (symbol,))
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


def data_symbol(symbol, data, token_contract):
    if check_symbol_exists(symbol):
        print(f"Symbol {symbol} already exists in the database. Skipping insertion.")
        return

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    data_to_db = {
        "TOKEN_SYMBOL": symbol,
        "ORDERS": data,
        "TOKEN_CONTRACT": token_contract
    }

    cursor.execute('''
        INSERT INTO ARB (TOKEN_SYMBOL, ORDERS, TOKEN_CONTRACT)
        VALUES (?, ?, ?)
    ''', (data_to_db["TOKEN_SYMBOL"], data_to_db["ORDERS"], data_to_db["TOKEN_CONTRACT"]))

    conn.commit()
    conn.close()


def update_token_contract(symbol, token_contract):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE ARB
        SET TOKEN_CONTRACT = ?
        WHERE TOKEN_SYMBOL = ?
    ''', (token_contract, symbol))

    conn.commit()
    conn.close()


def create_tables():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ARB (
            id INTEGER PRIMARY KEY,
            TOKEN_SYMBOL TEXT,
            ORDERS TEXT,
            TOKEN_CONTRACT TEXT DEFAULT NULL,
            CHANGE_5m REAL DEFAULT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Вызываем функцию для создания таблицы
# create_tables()

def fetch_all_data():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ARB')
    all_data = cursor.fetchall()

    conn.close()
    return all_data


all_data = fetch_all_data()


for row in all_data:
    token_symbol = row[1]
    orders = row[2]
    token_contract = row[3]
    change_5m = row[4]

    print("Token Symbol:", token_symbol)
    print("Orders:", orders)
    print("Token Contract:", token_contract)
    print("Change 5m:", change_5m)
    print("\n\n\n\n")
