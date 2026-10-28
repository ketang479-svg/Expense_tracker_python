"""
Expense Tracker - Python PBL Project
Features:
1. Add an expense with date, category, amount and description
2. View all saved expenses
3. View category-wise and total spending summary
4. Delete an expense by ID
5. Export expenses to CSV
6. Store data locally in a JSON file
Run: python expense_tracker.py
"""
 
import csv
import json
from datetime import date, datetime
from pathlib import Path
 
DATA_FILE = Path("expenses.json")
CSV_FILE = Path("expenses_export.csv")
CATEGORIES = [
    "Food", "Travel", "Education", "Shopping",
    "Bills", "Health", "Entertainment", "Other"
]
 
 
def load_expenses():
    """Load saved expenses; return an empty list if no data exists yet."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read the data file. Starting with an empty list.")
        return []
 
 
def save_expenses(expenses):
    """Save expenses as readable JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)
 
 

def ask_amount():
    """Ask for a positive numeric amount and validate the input."""
    while True:
        raw = input("Amount (INR): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number, e.g. 125.50.")

 
 
def ask_date():
    """Accept a date in YYYY-MM-DD format; default to today."""
    while True:
        raw = input(f"Date (YYYY-MM-DD, Enter for {date.today()}): ").strip()
        if not raw:
            return date.today().isoformat()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
 
 
def add_expense(expenses):
    """Collect and save one expense."""
    print("\n--- Add Expense ---")
    amount = ask_amount()
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    if category not in CATEGORIES:
        print("Unknown category; saved under Other.")
        category = "Other"
    description = input("Description: ").strip() or "No description"
    expense_date = ask_date()
    next_id = max((item["id"] for item in expenses), default=0) + 1
    expenses.append({
        "id": next_id,
        "date": expense_date,
        "category": category,
        "amount": amount,
        "description": description
    })
    save_expenses(expenses)
    print(f"Expense #{next_id} saved successfully.")
 
 
def view_expenses(expenses):
    """Display all saved expenses in a simple table."""
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return
    print(f"{'ID':<4} {'Date':<12} {'Category':<16} {'Amount (INR)':>13}  Description")
    print("-" * 72)
    for item in sorted(expenses, key=lambda row: (row["date"], row["id"])):
        print(f"{item['id']:<4} {item['date']:<12} {item['category']:<16} "
              f"{item['amount']:>13.2f}  {item['description']}")
    print("-" * 72)
    print(f"Total recorded: INR {sum(x['amount'] for x in expenses):.2f}")
 
 
def show_summary(expenses):
    """Calculate total and category-wise expenditure."""
    print("\n--- Spending Summary ---")
    if not expenses:
        print("No expenses available to summarize.")
        return
    totals = {}
    for item in expenses:
        totals[item["category"]] = totals.get(item["category"], 0) + item["amount"]
    overall = sum(item["amount"] for item in expenses)
    print(f"Total expenses: {len(expenses)}")
    print(f"Total spent: INR {overall:.2f}")
    print("Category-wise spending:")
    for category, amount in sorted(totals.items(), key=lambda pair: pair[1], reverse=True):
        share = amount / overall * 100 if overall else 0
        print(f"  {category:<16} INR {amount:>9.2f} ({share:5.1f}%)")
 
 
def delete_expense(expenses):
    """Delete an expense using its unique ID."""
    print("\n--- Delete Expense ---")
    if not expenses:
        print("No expenses to delete.")
        return
    view_expenses(expenses)
    raw = input("Enter expense ID to delete: ").strip()
    try:
        expense_id = int(raw)
    except ValueError:
        print("ID must be a whole number.")
        return
    for index, item in enumerate(expenses):
        if item["id"] == expense_id:
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"Deleted expense #{expense_id}: {removed['description']}")
            return
    print("No expense found with that ID.")
 
 
def export_csv(expenses):
    """Export current records to a CSV spreadsheet."""
    if not expenses:
        print("No expenses available to export.")
        return
    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "date", "category", "amount", "description"]
        )
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Export complete: {CSV_FILE.resolve()}")
 
 
def main():
    expenses = load_expenses()
    actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: view_expenses(expenses),
        "3": lambda: show_summary(expenses),
        "4": lambda: delete_expense(expenses),
        "5": lambda: export_csv(expenses),
    }
    while True:
        print("\n" + "=" * 38)
        print("        PYTHON EXPENSE TRACKER")
        print("=" * 38)
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Spending summary")
        print("4. Delete expense")
        print("5. Export to CSV")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Thank you for using Expense Tracker.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Select an option from 0 to 5.")
if __name__ == "__main__":
    main()
