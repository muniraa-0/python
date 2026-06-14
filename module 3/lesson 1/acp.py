def calculate_due_amount(bill_amount, paid_amount):
    return bill_amount - paid_amount

bill = float(input("Enter bill amount: "))
paid = float(input("Enter paid amount: "))

due = calculate_due_amount(bill, paid)

print("Due Amount:", due)