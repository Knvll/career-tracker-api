import json
from datetime import datetime
import shutil

welcome_message = """
Expense Tracker

    1. Add Expense
    2. Show Expenses
    3. Show total
    4. Exit"""

def save_expenses(expenses, file_path="expenses.json"):
    with open(file_path, "w") as file:
        json.dump(expenses, file, indent=4)

def create_backup(file_path="expenses.json"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_path = f"{file_path}.{timestamp}.bak"

    shutil.copy(file_path, backup_path)

def read_expenses(file_path="expenses.json"):
    try:
        with open(file_path, "r") as file:
            expenses = json.load(file)

        return validate_expenses_format(expenses)

    except FileNotFoundError:
        expenses = []
        save_expenses(expenses, file_path)
        return expenses
    
    except json.JSONDecodeError:
        print('Expenses file is corrupted.')
        create_backup(file_path)
        print('Backup created')

        expenses = []
        save_expenses(expenses, file_path)
        return expenses

def validate_expenses_format(expenses, file_path="expenses.json"):
    if not isinstance(expenses, list):
        create_backup(file_path)
        raise ValueError("Invalid expenses file structure.")

    for expense in expenses:
        if not isinstance(expense, dict):
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

        if "description" not in expense or "amount" not in expense:
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

        if not isinstance(expense['description'], str):
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

        if not expense["description"].strip():
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

        if not isinstance(expense['amount'], (float, int)):
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

        if expense["amount"] <= 0:
            create_backup(file_path)
            raise ValueError("Invalid expense structure.")

    return expenses


def show_menu():
    print(welcome_message)

def get_valid_amount():
    while True:
        amount = input("Amount: ")

        try:
            amount = float(amount)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")

def get_valid_description():
    while True:
        description = input("Description: ").strip()

        if not description:
            print("Enter a valid description.")
            continue

        return description

def add_expense(expenses, file_path="expenses.json"):
    expenses.append({
                'description': get_valid_description(),
                'amount': get_valid_amount()
            })
    save_expenses(expenses, file_path)
    

def show_expenses(expenses):
    if expenses:
        for index, expense in enumerate(expenses, start=1):
                print(f'{index}. {expense["description"]} - ${expense["amount"]:.2f}')
    else:
        print('No expenses registered.')

def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]

    return total

def expense_calculator():
    expenses = read_expenses()
    while True:
        show_menu()
        selection = input("Select an option: ")

        if selection == "1":
            add_expense(expenses)
            print("Expense added successfully.")
        elif selection == "2":
            show_expenses(expenses)
        elif selection == "3":
            if expenses:
                print(f'Total expenses: ${calculate_total(expenses):.2f}')
            else:
                print('No expenses registered.')
        elif selection == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    expense_calculator()