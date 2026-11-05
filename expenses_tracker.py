import json
import os
from datetime import date

DATA_FILE = "expenses.json"


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    category = input("Category (food/transport/fun/other): ").strip().lower() or "other"
    note = input("Note (optional): ").strip()
    expenses.append({
        "date": str(date.today()),
        "amount": amount,
        "category": category,
        "note": note,
    })
    save(expenses)
    print("Saved.")


def list_expenses(expenses):
    if not expenses:
        print("No expenses yet.")
        return
    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['category']:<10} | {e['amount']:>8.2f} | {e['note']}")


def summary(expenses):
    if not expenses:
        print("Nothing to summarize.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    for cat, total in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"{cat:<12}{total:>10.2f}")
    print("-" * 22)
    print(f"{'TOTAL':<12}{sum(totals.values()):>10.2f}")


def delete_expense(expenses):
    list_expenses(expenses)
    try:
        idx = int(input("Number to delete: ")) - 1
        removed = expenses.pop(idx)
        save(expenses)
        print(f"Deleted {removed['amount']:.2f} ({removed['category']})")
    except (ValueError, IndexError):
        print("Invalid choice.")


def main():
    expenses = load()
    while True:
        print("""
1) Add expense
2) List expenses
3) Summary by category
4) Delete expense
5) Quit""")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Pick 1-5.")


if __name__ == "__main__":
    main()