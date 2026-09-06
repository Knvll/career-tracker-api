from expense_tracker.expense_tracker import save_expenses,calculate_total,read_expenses
import pytest
import json

def test_calculate_total():
    expenses =[
        {"description": "Coffee", "amount": 5.0},
        {"description": "Gas", "amount": 40.0},
        {"description": "Lunch", "amount": 12.5},
    ]

    result = calculate_total(expenses)

    assert result == 57.5


def test_calculate_total_single():
    expenses = [
        {"description": "Coffee", "amount": 5.25}
    ]

    result = calculate_total(expenses)

    assert result == 5.25

def test_calculate_total_no_total():
    expenses = []

    result = calculate_total(expenses)

    assert result == 0

def test_calculate_total_decimal_values():
    expenses = [
        {"description": "Coffee", "amount": 2.50},
        {"description": "Snack", "amount": 3.75},
    ]

    result = calculate_total(expenses)

    assert result == 6.25

def test_calculate_total_equal_values():
    expenses = [
        {"description": "Item A", "amount": 10.0},
        {"description": "Item B", "amount": 10.0},
        {"description": "Item C", "amount": 10.0},
    ]

    result = calculate_total(expenses)

    assert result == 30.0

def test_calculate_total_big_values():
    expenses = [
        {"description": "Laptop", "amount": 2500.0},
        {"description": "Monitor", "amount": 700.0},
    ]

    result = calculate_total(expenses)
    
    assert result == 3200.0

#Decimal test
def test_calculate_total_small_values():
    expenses = [
        {"description": "A", "amount": 0.1},
        {"description": "B", "amount": 0.2},
    ]

    result = calculate_total(expenses)
    
    assert result == pytest.approx(0.3)

def test_save_expenses(tmp_path):
    file_path = tmp_path / "expenses.json"

    expenses = [
        {"description": "Coffee", "amount": 5.5},
        {"description": "Gas", "amount": 40.0},
    ]

    save_expenses(expenses, file_path)

    assert file_path.exists()

    with open(file_path, "r") as file:
        saved_expenses = json.load(file)

    assert saved_expenses == expenses


def test_read_expenses_valid_file(tmp_path):
    file_path = tmp_path / "expenses.json"

    expenses = [
        {"description": "Coffee", "amount": 5.5},
        {"description": "Gas", "amount": 40.0},
    ]

    with open(file_path, "w") as file:
        json.dump(expenses, file)

    result = read_expenses(file_path)

    assert result == expenses

def test_read_expenses_missing_file(tmp_path):
    file_path = tmp_path / "no_expense.json"

    result = read_expenses(file_path)

    assert result == []
    assert file_path.exists()

    with open(file_path, "r") as file:
        saved_data = json.load(file)

    assert saved_data == []

def test_read_expenses_invalid_content(tmp_path):
    file_path = tmp_path / "expenses.json"


    with open(file_path, "w") as file:
        file.write('{invalid json')

    result = read_expenses(file_path)

    assert result == []
    assert file_path.exists()

    with open(file_path, "r") as file:
        saved_data = json.load(file)

    assert saved_data == []

def test_read_expenses_invalid_structure(tmp_path):
    file_path = tmp_path / "expenses.json"

    expenses = [
        {"descriptioytrtyn": "Coffee", "amount": 5.5},
        {"description": "Gas", "amount": 40.0},
    ]
    
    with open(file_path, "w") as file:
        json.dump(expenses, file)

    with pytest.raises(ValueError):
        read_expenses(file_path)

def test_save_expenses_overwrites_existing_file(tmp_path):
    file_path = tmp_path / "expenses.json"

    original_expenses = [
        {"description": "Coffee", "amount": 5.5}
    ]

    new_expenses = [
        {"description": "Coffee", "amount": 5.5},
        {"description": "Nuts", "amount": 10.11}
    ]

    with open(file_path, "w") as file:
        json.dump(original_expenses, file)

    save_expenses(new_expenses, file_path)

    with open(file_path, "r") as file:
        saved_expenses = json.load(file)

    assert saved_expenses == new_expenses