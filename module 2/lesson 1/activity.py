medical_cause = input("Do you have any medical cause? (YN): ")
if medical_cause == 'Y':
    print("You are allowed for exam")
else:
    attendance = int(input("Enter your attendance: "))
if attendance == 75:
    print("You are allowed for the exam.")
else:
    print("You are not allowed")