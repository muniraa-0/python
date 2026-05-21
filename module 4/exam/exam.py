
grade_book = {
    "Munira": 100,
    "Farisa": 92,
    "Rifah": 75,
    "Taskeen": 96,
    "Namira": 81
}


total = 0
for grade in grade_book.values():
    total += grade
average = total / len(grade_book)
print(f"Class Average: {average}")

top = max(grade_book, key=grade_book.get)
bottom = min(grade_book, key=grade_book.get)
print(f"Top student: {top} with {grade_book[top]}")
print(f"Bottom student: {bottom} with {grade_book[bottom]}")

name = input("Enter a name to look up: ")
score = grade_book.get(name)
if score:
    print(f"{name} scored {score}")
else:
    print(f"{name} not found")