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

def get_valid_description():
    while True:
        description = input("Description: ").strip()

        if not description:
            print("Enter a valid description.")
            continue

        return description

def add_expense(expenses):
    expenses.append({
                'description': get_valid_description(),
                'amount': get_valid_amount()
            })
    

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
    expenses = []
    while True:

        show_menu()
        selection = input("Select and option: ")

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