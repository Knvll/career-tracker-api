import sqlite3
import json


def get_connection(db_path):
    conecction = sqlite3.connect(db_path)

    return conecction

def validate_initialization(cursor):
    res = cursor.execute("SELECT name FROM sqlite_master")
    if res.fetchone():
        print('Database initialized')


def initialize_database(db_path):
    try: 
        connection = get_connection(db_path)
        cursor = connection.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT
        );''')

        validate_initialization(cursor)

        connection.close()
    
    except Exception:
        print('Error initializing the databse', Exception)

def insert_expense(db_path, description, amount, date, category):
    connection = get_connection(db_path)
    cursor = connection.cursor()

    cursor.execute(f"""
        INSERT INTO expenses (description, amount, date, category)
        VALUES ('{description}', {amount}, '{date}', '{category}')
    """)

    connection.commit()

    connection.close()

def get_all_expenses(db_path, order):
    connection = get_connection(db_path)
    cursor = connection.cursor()

    result = cursor.execute(f'SELECT id, description, amount, date, category FROM expenses ORDER BY Id {order}').fetchall()
    response = json.loads(json.dumps(result))

    connection.close()

    return response

def get_expense_by_id(db_path, id):
    connection = get_connection(db_path)
    cursor = connection.cursor()

    result = cursor.execute(f'SELECT id, description, amount, date, category FROM expenses WHERE id = {id}').fetchall()
    response = json.loads(json.dumps(result))

    connection.close()

    return response

def update_expense_by_id(db_path, id, new_description, new_amount, new_date, new_category):
    connection = get_connection(db_path)

    updated_item = connection.execute(f'''
        UPDATE expenses
        SET description = '{new_description}', amount = {new_amount}, date = '{new_date}', category = '{new_category}'
        WHERE id = {id}
    ''').rowcount

    if updated_item > 0:
        print(f'Id {id} updated succesfully')
    else:
        print(f'Id {id} not found')


    result = connection.execute(f'SELECT id, description, amount, date, category FROM expenses WHERE id = {id}').fetchall()
    response = json.loads(json.dumps(result))

    connection.close()

    return response

def delete_expense_by_id(db_path, id):
    connection = get_connection(db_path)
    
    deleted_item = connection.execute(f'''
            DELETE FROM expenses
            WHERE id = {id}
        ''').rowcount

    if deleted_item == 0:
        print(f'Id {id} not found')
    else:
        print(f'Id {id} deleted succesfully')

    connection.close()
    


initialize_database('expenses.db')

delete_expense_by_id('expenses.db', 2)

for expense in get_all_expenses('expenses.db', 'DESC'):
    print(expense)

