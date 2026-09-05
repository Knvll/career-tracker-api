from expense_tracker.expense_tracker import calculate_total
import pytest

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