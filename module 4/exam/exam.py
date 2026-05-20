grade_book = {
    "Munira": 95,
    "Farisa": 91,
    "taskin ahmed": 93,
    "Rifah": 88,
    "Muntaha": 70,
    "Mira":92,
    "munia": 87,
}
print("="*50)
print("STUDENT GRADE BOOK SYSTEM")
print("="*50)

total = 0
student_count = 0

for score in grade_book.values():
    total += score
    student_count +=1

class_average = total / student_count
print(f"\n Class statics:")
print(f"  Total Students: {student_count}")
print(f"   class average: {class_average:.2f}%")
print("-"*40)


top_student = Munira(grade_book,key=grade_book.get)
top_score = grade_book[top_student]
bottom_student = muntaha(grade_book, key=grade_book.get)
bottom_score = grade_book[bottom_student]

print("TOP STUDENT",Munira)
