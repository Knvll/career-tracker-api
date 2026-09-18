from expense_tracker.database.connector import (initialize_database, get_connection, validate_initialization, insert_expense, 
                                                get_expense_by_id, get_all_expenses, update_expense_by_id, delete_expense_by_id,
                                                calculate_total)
import pytest
import sqlite3

def test_database_creation(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    assert db_path.exists()


def test_database_initialization(tmp_path):
    db_path = tmp_path / "test_expenses.db"

    initialize_database(db_path)
    #VALIDATE  IT NOT EXIST 
    initialize_database(db_path)
    cursor = get_connection(db_path).cursor()
    valid_initialization = validate_initialization(cursor, 'expenses')
    assert valid_initialization == True

def test_insert_expense(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    inserted_id = insert_expense(db_path, 'Coffee', 1.9, '09/16', 'Breakfast')
    assert inserted_id is not None

    inserted_expense = get_expense_by_id(db_path, inserted_id)

    assert inserted_expense is not None
    assert inserted_expense[1] == 'Coffee'

def test_get_expense_by_id_returns_none_when_id_does_not_exist(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    expense = get_expense_by_id(db_path, 2)
    
    assert expense is None

def test_get_all_expenses(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    insert_expense(db_path, 'Coffee', 1.9, '09/16', 'Breakfast')
    insert_expense(db_path, 'Donut', 4.9, '09/16', 'Breakfast')
    insert_expense(db_path, 'Milk', 6.9, '09/16', 'Grocery')

    inserted_expenses = get_all_expenses(db_path)

    assert inserted_expenses is not []
    assert len(inserted_expenses) == 3
    assert inserted_expenses[0][0] == 1
    assert inserted_expenses[1][0] == 2
    assert inserted_expenses[2][0] == 3

def test_update_expense(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    insert_expense(db_path, 'Coffee', 1.9, '09/16', 'Breakfast')
    donut_id = insert_expense(db_path, 'Donut', 4.9, '09/16', 'Breakfast')

    updated_success = update_expense_by_id(db_path, donut_id, 'Beagle', 3.99, '9/16', 'Breakfast')
    updated_expenses = get_all_expenses(db_path)

    assert updated_success
    assert updated_expenses[0][1] == 'Coffee'
    assert updated_expenses[1][1] == 'Beagle'

def test_update_expense_not_found_id(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    was_updated = update_expense_by_id(db_path, 12, 'Beagle', 3.99, '9/16', 'Breakfast')

    assert was_updated is False

def test_delete_expense_by_id(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    expense_id = insert_expense(db_path, 'Coffee', 1.9, '09/16', 'Breakfast')

    was_deleted = delete_expense_by_id(db_path, expense_id)
    expense_not_found = delete_expense_by_id(db_path, 10)
    get_deleted_expense = get_expense_by_id(db_path, expense_id)

    assert was_deleted
    assert expense_not_found is False
    assert get_deleted_expense is None


def test_calculate_total(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    total_no_expenses = calculate_total(db_path)

    assert total_no_expenses == 0

    insert_expense(db_path, 'Coffee', 1, '09/16', 'Breakfast')
    insert_expense(db_path, 'Donut', 4, '09/16', 'Breakfast')
    insert_expense(db_path, 'Milk', 6, '09/16', 'Grocery')

    total_with_expenses = calculate_total(db_path)
    assert total_with_expenses == 11

def test_validate_data_integrity(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)
    insert_expense(db_path, 'Coffee', 1, '09/16', 'Breakfast')

    before = get_all_expenses(db_path)

    with pytest.raises(sqlite3.IntegrityError):
        insert_expense(db_path, 
                       description=None, 
                       amount=1, 
                       date='09/16', 
                       category='Breakfast')

    after = get_all_expenses(db_path)

    assert before == after

def test_insert_expense_none_category(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    inserted_expense_id = insert_expense(db_path, 'Coffee', 1, '09/16', category=None)
    inserted_expense = get_expense_by_id(db_path, inserted_expense_id)

    assert inserted_expense[4] is None

def test_defensive_description_insertion(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    sql_injection_attempt = "Coffee'); DROP TABLE expenses; --"
    inserted_expense_id = insert_expense(db_path, description=sql_injection_attempt, amount=1, date='09/16', category='Breakfast')
    inserted_expense = get_expense_by_id(db_path, inserted_expense_id)

    assert inserted_expense[1] == sql_injection_attempt

def test_insert_expenses_with_same_content(tmp_path):
    db_path = tmp_path / "test_expenses.db"
    initialize_database(db_path)

    id_1 = insert_expense(db_path, 'Coffee', 1, '09/16', category='Breakfast')
    id_2 = insert_expense(db_path, 'Coffee', 1, '09/16', category='Breakfast')

    assert id_1 != id_2