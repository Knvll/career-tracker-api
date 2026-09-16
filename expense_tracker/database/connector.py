import sqlite3
import json


def get_connection(db_path):
    conecction = sqlite3.connect(db_path)

    return conecction

def validate_initialization(cursor, table_name):
    query = "SELECT name FROM sqlite_master WHERE type = 'table' AND Name = ?"
    params = (table_name,)
    result = cursor.execute(query, params).fetchone()

    return result is not None


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

        validate_initialization(cursor, 'expenses')

        connection.close()
    
    except Exception:
        print('Error initializing the databse', Exception)

def insert_expense(db_path, description, amount, date, category):
    connection = get_connection(db_path)
    cursor = connection.cursor()
    query = "INSERT INTO expenses (description, amount, date, category) VALUES(?, ?, ?, ?)"
    params = (description, amount, date, category)
    inserted_id = None

    try:
        cursor.execute(query, params)
        inserted_id = cursor.lastrowid
        connection.commit()
        
    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
    return inserted_id

def get_all_expenses(db_path):
    connection = get_connection(db_path)
    cursor = connection.cursor()
    query = """
        SELECT id, description, amount, date, category
        FROM expenses
        ORDER BY id ASC
    """

    all_expenses = cursor.execute(query).fetchall()

    connection.close()

    return all_expenses

def get_expense_by_id(db_path, expense_id):
    connection = get_connection(db_path)
    cursor = connection.cursor()
    query = "SELECT id, description, amount, date, category FROM expenses WHERE id = ?"
    params = (expense_id,)

    expense_by_id = cursor.execute(query, params).fetchone()

    connection.close()

    return expense_by_id

def update_expense_by_id(db_path, expense_id, new_description, new_amount, new_date, new_category):
    connection = get_connection(db_path)
    query = '''
        UPDATE expenses
        SET description = ?, amount = ?, date = ?, category = ?
        WHERE id = ?
    '''
    params = (new_description, new_amount, new_date, new_category, expense_id)

    try:
        updated_item = connection.execute(query, params).rowcount
        connection.commit()
        return updated_item > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def delete_expense_by_id(db_path, expense_id):
    connection = get_connection(db_path)
    query = """
        DELETE FROM expenses
        WHERE id = ?
    """
    params = (expense_id,)

    try:
        deleted_item = connection.execute(query, params).rowcount
        connection.commit()
        return deleted_item > 0

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def calculate_total_by_group(db_path, group):
    connection = get_connection(db_path)

    total = connection.execute(f'''
        SELECT SUM(amount)
        FROM expenses
        GROUP BY {group}   
    ''').fetchall()

    connection.close()

    return [row[0] for row in total]

def calculate_total(db_path):
    connection = get_connection(db_path)

    total = connection.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
    """).fetchone()

    connection.close()

    return total[0]

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
    totals = calculate_total_by_group(db_path, 'category')
    total = 0

    for x in range(len(categories)):
        totals_by_category.append({
            categories[x]: totals[x]
        })
        total += totals[x]

    totals_by_category.append({'Total':total})

    return totals_by_category
