import json
from datetime import datetime
import shutil
from database.connector import insert_expense, initialize_database, get_all_expenses, calculate_total

welcome_message = """
Expense Tracker

    1. Add Expense
    2. Show Expenses
    3. Show total
    4. Exit"""

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

def get_valid_value(value_name):
    while True:
        value = input(f"{value_name}: ").strip()

        if not value:
            print("Enter a valid {value_name}.")
            continue

        return value

def add_expense():
    insert_expense('expenses.db', get_valid_value('Description'), get_valid_amount(), get_valid_value('Date'), get_valid_value('Category'))
    

def show_expenses(expenses):
    for expense in expenses:
        print(f'{expense[0]}. {expense[1]} - ${expense[2]:.2f} - {expense[3]} - {expense[4]}')

def expense_calculator():
    initialize_database('expenses.db')

    while True:
        show_menu()
        selection = input("Select an option: ")

        if selection == "1":
            add_expense()
            print("Expense added successfully.")
        elif selection == "2":
            expenses = get_all_expenses('expenses.db')
            if expenses:
                show_expenses(expenses)
            else:
                print('No expenses registered.')
        elif selection == "3":
            expense_total = calculate_total('expenses.db')[0]
            if expense_total:
                print(f'Total expenses: ${expense_total:.2f}')
            else:
                print('No expenses registered.')
        elif selection == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    expense_calculator()