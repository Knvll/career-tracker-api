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
    try:
        connection.execute(f"""
            INSERT INTO expenses (description, amount, date, category)
            VALUES ('{description}', {amount}, '{date}', '{category}')
        """)

        connection.commit()
        
    except Exception:
        connection.rollback()

    connection.close()

def get_all_expenses(db_path, order):
    connection = get_connection(db_path)
    cursor = connection.cursor()

    all_expenses = cursor.execute(f'SELECT id, description, amount, date, category FROM expenses ORDER BY {order}').fetchall()

    connection.close()

    return json.loads(json.dumps(all_expenses))

def get_expense_by_id(db_path, id):
    connection = get_connection(db_path)
    cursor = connection.cursor()

    expense_by_id = cursor.execute(f'SELECT id, description, amount, date, category FROM expenses WHERE id = {id}').fetchall()

    connection.close()

    return json.loads(json.dumps(expense_by_id))

def update_expense_by_id(db_path, id, new_description, new_amount, new_date, new_category):
    connection = get_connection(db_path)

    updated_item = connection.execute(f'''
        UPDATE expenses
        SET description = '{new_description}', amount = {new_amount}, date = '{new_date}', category = '{new_category}'
        WHERE id = {id}
    ''').rowcount

    connection.close()

    if updated_item > 0:
        return True
    else:
        return False

def delete_expense_by_id(db_path, id):
    connection = get_connection(db_path)
    
    deleted_item = connection.execute(f'''
            DELETE FROM expenses
            WHERE id = {id}
        ''').rowcount

    connection.close()

    if deleted_item == 0:
        return False
    else:
        return True

def calculate_total(db_path, group):
    connection = get_connection(db_path)

    total = connection.execute(f'''
        SELECT SUM(amount)
        FROM expenses
        GROUP BY {group}   
    ''').fetchall()

    connection.close()

    return [row[0] for row in total]

def get_all_categories(db_path):
    connection = get_connection(db_path)
    
    categories = connection.execute('''
        SELECT category
        FROM expenses
        GROUP BY category   
    ''').fetchall()

    connection.close()

    return [row[0] for row in categories]

def calculate_total_by_category(db_path):
    totals_by_category = []
    categories = get_all_categories(db_path)
    totals = calculate_total(db_path, 'category')
    total = 0

    for x in range(len(categories)):
        totals_by_category.append({
            categories[x]: totals[x]
        })
        total += totals[x]

    totals_by_category.append({'Total':total})

    return totals_by_category


